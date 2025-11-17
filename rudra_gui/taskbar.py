from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class Taskbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #202020;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)

        start_btn = QPushButton("Rudra")
        start_btn.setStyleSheet("background-color: #3a3cff; color: white; padding: 8px;")
        layout.addWidget(start_btn)

        self.setLayout(layout)
