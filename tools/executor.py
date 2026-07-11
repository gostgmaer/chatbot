from tools.registry import ToolRegistry


class ToolExecuter:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, **kwargs):
        tool = self.registry.get(tool_name)
        if tool is None:
            raise ValueError(f"Tool with name '{tool_name}' is not registered.")
        return tool.execute(**kwargs)
