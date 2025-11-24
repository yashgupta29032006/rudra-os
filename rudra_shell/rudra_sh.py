from rudra_shell.llm_interface import LLMInterface
from rudra_plugins.plugin_loader import PluginLoader

from rudra_ai.planner import DeepPlanner, TOOL_REGISTRY
import json


class RudraShell:
    def __init__(self):
        print("RudraShell initialized.")

        self.llm = LLMInterface()
        self.plugins = PluginLoader()
        self.plugins.load_plugins()
        self.planner = DeepPlanner(llm=self.llm)

        for name, plugin in self.plugins.plugins.items():
            # Register plugin as a tool in the global registry
            try:
                if hasattr(plugin, "execute"):
                    TOOL_REGISTRY.register(
                        name=plugin.name,
                        func=plugin.execute,
                        schema=getattr(plugin, "schema", {})
                    )
                else:
                     # Fallback for plugins without execute/schema (legacy)
                    TOOL_REGISTRY.register(
                        name=plugin.name,
                        func=lambda command, p=plugin: p.run(command),
                        schema={"command": str}
                    )
            except ValueError:
                # Tool already registered, skip
                pass


    def start(self):
        print("Welcome to Rudra OS (AI Mode).")
        while True:
            cmd = input("rudra> ")

            if cmd in ["exit", "quit"]:
                print("Shutting down Rudra OS...")
                break

            try:
                report = self.planner.run(cmd)
                print(json.dumps(report, indent=2, default=str))
            except Exception as e:
                print(f"Error: {e}")
