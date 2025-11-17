from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
# Use your local LLMInterface if you want immediate responses
try:
    from rudra_shell.llm_interface import LLMInterface
except Exception:
    LLMInterface = None

class AIConsole(QWidget):
    def __init__(self, llm_callback):
        super().__init__()
        self.setWindowTitle("Rudra AI Console")
        self.resize(600, 500)

        self.llm = LLMInterface() if LLMInterface else None

        layout = QVBoxLayout()

        self.input = QTextEdit()
        self.input.setPlaceholderText("Type your query here...")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        send_btn = QPushButton("Ask Rudra")
        send_btn.clicked.connect(self.send_prompt)

        layout.addWidget(self.input)
        layout.addWidget(send_btn)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def send_prompt(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        # If you have an LLMInterface it will be used; otherwise echo fallback
        if self.llm:
            try:
                resp = self.llm.ask(text)
            except Exception as e:
                resp = f"[LLM Error] {e}"
        else:
            resp = f"[AI fallback] I understood: {text}"
        self.output.append(f"User: {text}\nRudra: {resp}\n")
        self.input.clear()
