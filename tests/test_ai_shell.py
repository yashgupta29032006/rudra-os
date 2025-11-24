import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
from rudra_shell.rudra_sh import RudraShell
from rudra_ai.planner import DeepPlanner

class TestAIShell(unittest.TestCase):
    def setUp(self):
        self.shell = RudraShell()
        # Mock LLM to avoid real API calls during basic tests
        self.shell.llm.ask = MagicMock()
        
    def test_plugin_registration(self):
        """Verify that plugins are registered as tools in the planner."""
        from rudra_ai.planner import TOOL_REGISTRY
        tools = TOOL_REGISTRY.list_tools()
        self.assertIn("create_file", tools)
        self.assertIn("folder", tools)
        self.assertIn("read_file", tools)
        
    def test_create_file_execution(self):
        """Verify create_file plugin execution via tool registry."""
        from rudra_ai.planner import TOOL_REGISTRY
        tool = TOOL_REGISTRY.get("create_file")
        test_file = "test_ai_file.txt"
        result = tool.func(path=test_file, content="AI Content")
        self.assertIn("Created file", result)
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "AI Content")
        os.remove(test_file)

    def test_folder_execution(self):
        """Verify folder plugin execution via tool registry."""
        from rudra_ai.planner import TOOL_REGISTRY
        tool = TOOL_REGISTRY.get("folder")
        test_folder = "test_ai_folder"
        result = tool.func(path=test_folder)
        self.assertIn("Created folder", result)
        self.assertTrue(os.path.isdir(test_folder))
        shutil.rmtree(test_folder)

if __name__ == "__main__":
    unittest.main()
