from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

class AIConsole(QWidget):
    def __init__(self, llm_callback):
        super().__init__()
        self.setWindowTitle("Rudra AI Console")
        self.resize(600, 500)

        self.llm_callback = llm_callback

        layout = QVBoxLayout()

        self.input = QTextEdit()
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        send_btn = QPushButton("Ask")
        send_btn.clicked.connect(self.send_prompt)

        layout.addWidget(self.input)
        layout.addWidget(send_btn)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def send_prompt(self):
        text = self.input.toPlainText()
        response = self.llm_callback(text)
        self.output.append(f"User: {text}")
        self.output.append(f"Rudra: {response}")
        self.input.clear()
