from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class StartMenu(QWidget):
    def __init__(self, launcher_callback, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #1f1f1f; border: 1px solid #444;")

        self.launcher_callback = launcher_callback

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        btn_terminal = QPushButton("Open Terminal")
        btn_terminal.clicked.connect(lambda: self._launch_and_hide("gnome-terminal"))
        layout.addWidget(btn_terminal)

        btn_ai = QPushButton("Rudra AI Console")
        btn_ai.clicked.connect(lambda: self._launch_and_hide("rudra_ai"))
        layout.addWidget(btn_ai)

        btn_firefox = QPushButton("Open Firefox")
        btn_firefox.clicked.connect(lambda: self._launch_and_hide("firefox"))
        layout.addWidget(btn_firefox)

        btn_shutdown = QPushButton("Shutdown Rudra Desktop")
        btn_shutdown.clicked.connect(lambda: self._launch_and_hide("shutdown"))
        layout.addWidget(btn_shutdown)

        layout.addStretch(1)
        self.setLayout(layout)

    def _launch_and_hide(self, app_name):
        self.hide()
        self.launcher_callback(app_name)
