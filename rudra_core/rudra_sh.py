from rudra_shell.llm_interface import LLMInterface
from rudra_plugins.plugin_loader import PluginLoader
from rudra_core.tool_registry import ToolRegistry
from rudra_core.dispatcher import Dispatcher
from rudra_core.reasoning_engine import ReasoningEngine

class RudraShell:
    def __init__(self):
        print("RudraShell initialized.")

        self.plugins = PluginLoader()
        self.plugins.load_plugins()

        self.tools = ToolRegistry()
        self.dispatcher = Dispatcher(self.tools)
        self.reasoner = ReasoningEngine()

        for name, plugin in self.plugins.plugins.items():
            if hasattr(plugin, "run"):
                self.tools.register(
                    name=plugin.name,
                    description=plugin.__doc__ or "",
                    func=lambda command, p=plugin: p.run(command)
                )

    def start(self):
        print("Welcome to Rudra OS.")
        while True:
            cmd = input("rudra> ")
            if cmd in ["exit", "quit"]:
                print("Shutting down Rudra OS...")
                break

            action = self.reasoner.think(cmd)
            result = self.dispatcher.dispatch(action)

            print(result)
