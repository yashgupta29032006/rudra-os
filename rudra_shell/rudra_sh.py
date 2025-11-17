from rudra_shell.llm_interface import LLMInterface
from rudra_plugins.plugin_loader import PluginLoader

from rudra_core.tool_registry import ToolRegistry
from rudra_core.dispatcher import Dispatcher
from rudra_core.agent_planner import AgentPlanner


class RudraShell:
    def __init__(self):
        print("RudraShell initialized.")

        self.llm = LLMInterface()
        self.plugins = PluginLoader()
        self.plugins.load_plugins()
        self.registry = ToolRegistry()
        self.dispatcher = Dispatcher(self.registry)
        self.planner = AgentPlanner()

        for name, plugin in self.plugins.plugins.items():
            self.registry.register(
                name=plugin.name,
                description=(plugin.__doc__ or ""),
                func=lambda command, p=plugin: p.run(command)
            )


    def start(self):
        print("Welcome to Rudra OS.")
        while True:
            cmd = input("rudra> ")

            if cmd in ["exit", "quit"]:
                print("Shutting down Rudra OS...")
                break

            steps = self.planner.plan(cmd)

            for action in steps:
                result = self.dispatcher.dispatch(action)
                print(result)
