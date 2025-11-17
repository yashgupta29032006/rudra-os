class ReasoningEngine:
    def __init__(self):
        print("Reasoning Engine ready.")

    def think(self, prompt: str):
        if "folder" in prompt:
            parts = prompt.split()
            folder = parts[-1]
            return {
                "tool": "create_folder",
                "args": { "name": folder }
            }

        return {
            "tool": "None",
            "args": {}
        }
