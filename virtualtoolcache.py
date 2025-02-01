import json
from typing import List, Dict, Any, Tuple

class VirtualToolCache:
    def __init__(self, cache_file: str = "virtual_tools.json"):
        self.cache_file = cache_file
        self.tools: Dict[str, List[Dict[str, Any]]] = self.load_cache()
    
    def load_cache(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            with open(self.cache_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.tools, f, indent=4)
    
    def get_virtual_tool(self, problem: str) -> List[Dict[str, Any]]:
        return self.tools.get(problem, [])
    
    def add_virtual_tool(self, problem: str, tool_sequence: List[Dict[str, Any]]):
        if problem not in self.tools:
            self.tools[problem] = tool_sequence
            self.save_cache()
    
    def exists(self, problem: str) -> bool:
        return problem in self.tools
