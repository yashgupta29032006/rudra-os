class Plugin:
    name = "template"

    def match(self, command: str) -> bool:
        return False

    def run(self, command: str) -> str:
        return "Template plugin executed."
