import importlib
import os

class PluginLoader:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        plugin_folder = os.path.dirname(__file__)
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename not in ["__init__.py", "plugin_template.py"]:
                module_name = f"rudra_plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "Plugin"):
                        plugin_instance = module.Plugin()
                        self.plugins[plugin_instance.name] = plugin_instance
                        print(f"Loaded plugin: {plugin_instance.name}")
                except Exception as e:
                    print(f"Failed to load plugin {filename}: {e}")

    def execute(self, command):
        for name, plugin in self.plugins.items():
            if plugin.match(command):
                return plugin.run(command)
        return "[Plugin] No plugin matched this command."
