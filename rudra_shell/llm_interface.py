class LLMInterface:
    def __init__(self):
        print("LLM Interface initialized.")

    def ask(self, prompt: str) -> str:
        return f"[AI] I understood your command: {prompt}"
