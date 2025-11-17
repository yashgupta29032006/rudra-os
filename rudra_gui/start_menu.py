from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class StartMenu(QWidget):
    def __init__(self, launcher_callback):
        super().__init__()
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1f1f1f; border: 1px solid #444;")

        self.launcher_callback = launcher_callback

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        btn_terminal = QPushButton("Open Terminal")
        btn_terminal.clicked.connect(lambda: self.launcher_callback("gnome-terminal"))
        layout.addWidget(btn_terminal)

        btn_ai = QPushButton("Rudra AI Console")
        btn_ai.clicked.connect(lambda: self.launcher_callback("rudra_ai"))
        layout.addWidget(btn_ai)

        btn_firefox = QPushButton("Open Firefox")
        btn_firefox.clicked.connect(lambda: self.launcher_callback("firefox"))
        layout.addWidget(btn_firefox)

        btn_shutdown = QPushButton("Shutdown Rudra Desktop")
        btn_shutdown.clicked.connect(lambda: self.launcher_callback("shutdown"))
        layout.addWidget(btn_shutdown)

        layout.addStretch(1)

        self.setLayout(layout)
        
