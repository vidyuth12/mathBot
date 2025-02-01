# MathBot: A Multi-Agent System for Mathematical Problem Solving

## Overview
MathBot is a multi-agent system designed to solve mathematical problems using a combination of AI planning, execution, and validation. The system leverages a toolbox of mathematical operations, a virtual tool cache for storing successful solutions, and error correction mechanisms to handle unexpected failures. The project is implemented in Python and uses OpenAI's GPT models for planning and error correction.

---

## What is Implemented
1. **Multi-Agent System**:
   - **PlannerAgent**: Breaks down a mathematical problem into a sequence of tool calls using OpenAI's GPT models.
   - **ExecutorAgent**: Executes the planned tool calls using a predefined toolbox of mathematical operations.
   - **ValidatorAgent**: Validates the computed result against the expected result provided by the user.
   - **ErrorCorrectionAgent**: Attempts to correct errors during execution by suggesting alternative tool calls.
   - **VirtualToolCache**: Caches successful tool sequences for future reuse, improving efficiency.

2. **Mathematical Toolbox**:
   - Includes basic operations such as `SUM`, `PRODUCT`, `QUOTIENT`, `POWER`, `SQRT`, `AVG`, `ROUND`, `MODULO`, and `ABS`.
   - Also includes unreliable tools (`UNRELIABLE_SUM`, `UNRELIABLE_PRODUCT`) for testing error handling.

3. **Virtual Tool Cache**:
   - Stores successful tool sequences in a JSON file (`virtual_tools.json`) for persistence across sessions.
   - Reuses cached solutions for previously solved problems, reducing computation time.

4. **Error Handling**:
   - Detects and handles errors during execution (e.g., division by zero, negative square roots).
   - Uses AI to suggest corrected tool calls when errors occur.

5. **Testing Framework**:
   - Comprehensive unit tests for all components using Python's `unittest` framework.
   - Tests cover basic operations, caching behavior, error handling, and cache persistence.

---

## Requirements
To run this project, you need the following:

1. **Python 3.8 or higher**.
2. **OpenAI API Key**:
   - Obtain an API key from [OpenAI](https://platform.openai.com/).
   - Store the key in a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
3. **Python Libraries**:
   - Install the required libraries using `pip`:
     ```bash
     pip install openai python-dotenv
     ```

---

## How to Reproduce
Follow these steps to set up and run the project:

### 1. Clone the Repository
    ```bash
    git clone https://github.com/vidyuth12/mathBot.git
    cd mathBot
    ```

### 2. Set Up the Environment
1. **Create a `.env` File**:
   - In the root directory of the project, create a file named `.env`.
   - Add your OpenAI API key to the file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

2. **Install Required Python Libraries**:
   - Run the following command to install the necessary dependencies:
     ```bash
     pip install openai python-dotenv
     ```
   - Alternatively, if you have a `requirements.txt` file, use:
     ```bash
     pip install -r requirements.txt
     ```
3. **Run the system**:
    - Execute the main script to solve a mathematical problem:
    ```bash
    python main2.py
    ```
    - Run the test suite to verify all components:
    ```bash
    python test2.py
    ```

## Example Problems
Here are some example problems you can test with MathBot:

### Basic Operations
- "What is the sum of 5 and 3?"
- "What is the product of 4 and 6?"
- "What is the square root of 16?"

### Error Handling
- "What is 10 divided by 0?" (Division by zero)
- "What is the square root of -16?" (Negative square root)

### Caching
Solve a problem twice to see the cache in action:

```python
system = MultiAgentSystem()
print(system.solve("What is the sum of 100 and 200?", 300))  # First execution
print(system.solve("What is the sum of 100 and 200?", 300))  # Second execution (uses cache)
