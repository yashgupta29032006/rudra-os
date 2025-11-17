from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

class AppLauncher(QWidget):
    def __init__(self, launch_callback, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background: #181818;")
        self.resize(600, 500)

        self.launch_callback = launch_callback

        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        apps = {
            "Terminal": "gnome-terminal",
            "Browser": "firefox",
            "AI Console": "rudra_ai",
            "Files": "nautilus",
            "Settings": "gnome-control-center",
            "Shutdown": "shutdown",
        }

        row = 0
        col = 0

        for name, command in apps.items():
            btn = QPushButton(name)
            btn.setFixedSize(150, 80)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    color: white;
                    border-radius: 8px;
                    font-size: 15px;
                }
                QPushButton::hover {
                    background-color: #3d3d3d;
                }
            """)
            btn.clicked.connect(lambda _, cmd=command: self.launch(cmd))

            layout.addWidget(btn, row, col)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        self.setLayout(layout)

    def launch(self, command):
        self.hide()
        self.launch_callback(command)
