class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, description, func):
        self.tools[name] = {
            "description": description,
            "func": func
        }

    def get_tools(self):
        return self.tools

    def execute(self, tool_name, args):
        if tool_name in self.tools:
            return self.tools[tool_name]["func"](**args)
        return f"[Tool] Unknown tool: {tool_name}"
