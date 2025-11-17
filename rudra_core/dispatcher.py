class Dispatcher:
    def __init__(self, tool_registry):
        self.registry = tool_registry

    def dispatch(self, action):
        tool = action.get("tool")
        args = action.get("args", {})

        try:
            return self.registry.execute(tool, args)
        except Exception as e:
            return f"[Dispatcher Error] {e}"
