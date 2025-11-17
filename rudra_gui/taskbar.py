from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint
from rudra_gui.start_menu import StartMenu
from rudra_gui.ai_console import AIConsole
import subprocess
import os

class Taskbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #202020;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)

        self.start_menu = None
        self.ai_console = None

        start_btn = QPushButton("Rudra")
        start_btn.setStyleSheet(
            "background-color: #3a3cff; color: white; padding: 8px; font-weight: bold;"
        )
        start_btn.clicked.connect(self.toggle_start_menu)

        layout.addWidget(start_btn)
        layout.addStretch(1)

        self.setLayout(layout)

    def launch_app(self, app_name):
        """Launch apps. special names: 'shutdown', 'rudra_ai'"""
        if app_name == "shutdown":
            win = self.window()
            if win:
                win.close()
            return

        if app_name == "rudra_ai":
            self.open_ai_console()
            return
        try:
            subprocess.Popen([app_name])
        except Exception:
            try:
                os.system(f"{app_name} &")
            except Exception as e:
                print("Launcher error:", e)

    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.isVisible():
            self.start_menu.hide()
            return

        if not self.start_menu:
            self.start_menu = StartMenu(self.launch_app, parent=self.window())

        main_win = self.window()
        if main_win:
            x = 10
            y = main_win.height() - self.start_menu.height() - self.height() - 10
            self.start_menu.move(QPoint(x, y))
        self.start_menu.show()

    def open_ai_console(self):
        if self.ai_console and self.ai_console.isVisible():
            self.ai_console.raise_()
            return
        self.ai_console = AIConsole(parent=self.window())
        main_win = self.window()
        if main_win:
            center_x = (main_win.width() - self.ai_console.width()) // 2
            center_y = (main_win.height() - self.ai_console.height()) // 2
            self.ai_console.move(center_x, center_y)
        self.ai_console.show()
