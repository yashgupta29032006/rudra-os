from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from rudra_gui.start_menu import StartMenu
import subprocess

class Taskbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #202020;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)

        self.start_menu = None

        start_btn = QPushButton("Rudra")
        start_btn.setStyleSheet(
            "background-color: #3a3cff; color: white; padding: 8px; font-weight: bold;"
        )
        start_btn.clicked.connect(self.toggle_start_menu)

        layout.addWidget(start_btn)
        layout.addStretch(1)

        self.setLayout(layout)

    def launch_app(self, app_name):
        if app_name == "shutdown":
            self.window().close()
            return

        if app_name == "rudra_ai":
            subprocess.Popen(["python3", "-c", "print('AI Console coming soon')"])
            return

        subprocess.Popen([app_name])

    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.isVisible():
            self.start_menu.hide()
        else:
            self.start_menu = StartMenu(self.launch_app)
            self.start_menu.move(20, self.window().height() - 450)
            self.start_menu.show()
