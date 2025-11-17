from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
try:
    from rudra_shell.llm_interface import LLMInterface
except Exception:
    LLMInterface = None

class AIConsole(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rudra AI Console")
        self.resize(700, 500)
        self.setStyleSheet("background-color: #111; color: #ddd;")

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
        if self.llm:
            try:
                resp = self.llm.ask(text)
            except Exception as e:
                resp = f"[LLM Error] {e}"
        else:
            resp = f"[AI fallback] I understood: {text}"
        self.output.append(f"User: {text}\nRudra: {resp}\n")
        self.input.clear()
