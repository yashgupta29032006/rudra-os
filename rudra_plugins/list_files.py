import os

class Plugin:
    name = "list_files"

    def match(self, command: str) -> bool:
        keywords = ["list files", "show files", "ls"]
        return any(k in command.lower() for k in keywords)

    def run(self, command: str) -> str:
        files = os.listdir(".")
        return "[Files]\n" + "\n".join(files)
