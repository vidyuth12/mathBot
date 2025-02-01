import random
import math
from typing import Callable, Dict

class MathToolbox:
    def __init__(self):
        self.tools: Dict[str, Callable] = {
            "SUM": self.SUM,
            "PRODUCT": self.PRODUCT,
            "QUOTIENT": self.QUOTIENT,
            "POWER": self.POWER,
            "SQRT": self.SQRT,
            "AVG": self.AVG,
            "ROUND": self.ROUND,
            "MODULO": self.MODULO,
            "ABS": self.ABS,
            "UNRELIABLE_SUM": self.UNRELIABLE_SUM,
            "UNRELIABLE_PRODUCT": self.UNRELIABLE_PRODUCT,
        }

    def get_tool(self, name: str) -> Callable:
        if name in self.tools:
            return self.tools[name]
        raise ValueError(f"Tool '{name}' not found.")

    # Static methods for tools
    @staticmethod
    def SUM(a, b): return a + b
    @staticmethod
    def PRODUCT(a, b): return a * b
    @staticmethod
    def QUOTIENT(a, b):
        if b == 0: raise ValueError("Division by zero")
        return a / b
    @staticmethod
    def POWER(a, b): return a ** b
    @staticmethod
    def SQRT(a):
        if a < 0: raise ValueError("Negative sqrt")
        return math.sqrt(a)
    @staticmethod
    def AVG(numbers):
        if not numbers: raise ValueError("Empty list")
        return sum(numbers) / len(numbers)
    @staticmethod
    def ROUND(a): return round(a)
    @staticmethod
    def MODULO(a, b):
        if b == 0: raise ValueError("Division by zero")
        return a % b
    @staticmethod
    def ABS(a): return abs(a)
    @staticmethod
    def UNRELIABLE_SUM(a, b):
        if random.random() < 0.4:  # 40% error rate
            if random.random() < 0.5:
                raise ValueError("Intentional error")
            else:
                return a + b + random.randint(-10, 10)
        return a + b
    @staticmethod
    def UNRELIABLE_PRODUCT(a, b):
        if random.random() < 0.3:  # 30% error rate
            if random.random() < 0.5:
                raise ValueError("Intentional error")
            else:
                return a * b + random.randint(-10, 10)
        return a * b