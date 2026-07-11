from typing import Literal

from tools.base import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self):
        return "calculator"

    @property
    def description(self):
        return "A simple calculator tool for performing basic arithmetic operations."

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }

    def execute(self, operation: Literal["add", "subtract", "multiply", "divide"], a: float, b: float) -> float:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Denominator cannot be zero.")
            return a / b