from tools.calculator import CalculatorTool
from tools.base import BaseTool
from google.genai import types


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self.register(CalculatorTool())

    def register(self, tool: BaseTool):
        if tool.name in self.tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        self.tools[tool.name] = tool

    def get(self, name: str):
        return self.tools.get(name)

    def unregister(self, name: str):
        if name in self.tools:
            self.tools.pop(name, None)

    def list(self):
        return list(self.tools.values())

    def exists(self, name: str):
        return name in self.tools

    def gemini_tools(self):
        return [
            types.Tool(function_declarations=[tool.declaration])
            for tool in self.list()
        ]
