import os
import json
from openai import OpenAI
import openai
from typing import List, Dict, Any
from toolbox import MathToolbox
from virtualtoolcache import VirtualToolCache
from dotenv import load_dotenv


def setup_api_key():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    os.environ["OPENAI_API_KEY"] = api_key

class LLMAgent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def generate_response(self, prompt: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        return response.choices[0].message.content

class PlannerAgent(LLMAgent):
    def plan(self, problem: str) -> List[Dict[str, Any]]:
        prompt = f"""
        You are a tool selection assistant. Your job is to break down the given math problem into calls to predefined mathematical tools.

        **Rules:**
        1. Only use the following tools: SUM, PRODUCT, QUOTIENT, POWER, SQRT, AVG, ROUND, MODULO, ABS.
        2. Always map the problem correctly to the most appropriate tool(s).
        3. Ensure the JSON format follows: 
           [{{"tool": "TOOL_NAME", "args": [arg1, arg2, ...]}}]

        **Examples:**
        - Problem: "What is the square root of 9?"  
          Output: [{{"tool": "SQRT", "args": [9]}}]

        - Problem: "What is the product of 5 and 3?"  
          Output: [{{"tool": "PRODUCT", "args": [5, 3]}}]

        - Problem: "Find the sum of 10 and 20."  
          Output: [{{"tool": "SUM", "args": [10, 20]}}]

        - Problem: "What is the remainder when 15 is divided by 4?"  
          Output: [{{"tool": "MODULO", "args": [15, 4]}}]

        **Your Turn:**  
        Problem: {problem}  
        Provide only the JSON output without any explanations.
        """
        response = self.generate_response(prompt)
        try:
            return json.loads(response)  # Safe JSON parsing
        except:
            raise ValueError("Failed to parse plan")

class ValidatorAgent:
    def validate(self, computed_result: Any, expected_result: Any) -> bool:
        """Compares the computed result with the expected user-provided result."""
        return computed_result == expected_result

class ErrorCorrectionAgent(LLMAgent):
    def correct_execution(self, tool_name: str, args: List[Any], error_message: str) -> Dict[str, Any]:
        """
        Uses AI to suggest an alternative tool call when execution fails.
        """
        prompt = f"""
        The execution of the tool {tool_name} with arguments {args} failed with error: "{error_message}".
        Suggest a corrected tool call in JSON format like:
        [{{"tool": "NEW_TOOL_NAME", "args": [arg1, arg2, ...]}}]
        """
        response = self.generate_response(prompt)
        try:
            return json.loads(response)[0]  # Extract single corrected tool call
        except:
            raise ValueError("Failed to parse error correction response")

class ExecutorAgent:
    def __init__(self, toolbox: MathToolbox, error_corrector: ErrorCorrectionAgent):
        self.toolbox = toolbox
        self.error_corrector = error_corrector

    def execute(self, tool_name: str, args: List[Any]):
        try:
            tool = self.toolbox.get_tool(tool_name)
            return tool(*args)
        except Exception as e:
            print(f"Execution failed for {tool_name}({args}): {e}")
            # Attempt error correction using AI
            try:
                correction = self.error_corrector.correct_execution(tool_name, args, str(e))
                corrected_tool = correction["tool"]
                corrected_args = correction["args"]
                print(f"Trying corrected tool: {corrected_tool}({corrected_args})")
                return self.toolbox.get_tool(corrected_tool)(*corrected_args)
            except Exception as correction_error:
                print(f"Error correction also failed: {correction_error}")
                return None

class MultiAgentSystem:
    def __init__(self):
        self.toolbox = MathToolbox()
        self.planner = PlannerAgent()
        self.error_corrector = ErrorCorrectionAgent()
        self.executor = ExecutorAgent(self.toolbox, self.error_corrector)
        self.validator = ValidatorAgent()
        self.virtual_tool_cache = VirtualToolCache()

    def solve(self, problem: str, expected_output) -> Dict[str, Any]:
        # Step 1: Check for a virtual tool
        if self.virtual_tool_cache.exists(problem):
            print(f"Using cached virtual tool for: {problem}")
            plan = self.virtual_tool_cache.get_virtual_tool(problem)
        else:
            plan = self.planner.plan(problem)

        results = []
        for step in plan:
            result = self.executor.execute(step["tool"], step["args"])
            if result is None: 
                return {"error": "Execution failed"}
            results.append(result)

        # Validate computed result against expected result
        if self.validator.validate(results[-1], expected_output):
            # Cache successful tool sequence
            if not self.virtual_tool_cache.exists(problem):
                self.virtual_tool_cache.add_virtual_tool(problem, plan)
            return {"result": results[-1]}
        else:
            return {"error": "Validation failed"}

if __name__ == "__main__":
    setup_api_key()  # Replace with your key
    system = MultiAgentSystem()
    print(system.solve("What is the product of 3 and 5?", 15))  # Output: {"result": 8}
