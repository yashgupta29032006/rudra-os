from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint
from rudra_gui.start_menu import StartMenu
from rudra_gui.ai_console import AIConsole
from rudra_gui.app_launcher import AppLauncher
import subprocess
import os


class Taskbar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #202020;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(10)

        start_btn = QPushButton("RUDRA")
        start_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3a3cff;
                color: white;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5757ff;
            }
            """
        )
        start_btn.clicked.connect(self.toggle_start_menu)

        apps_btn = QPushButton("Apps")
        apps_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            """
        )
        apps_btn.clicked.connect(self.toggle_app_launcher)

        layout.addWidget(start_btn)
        layout.addWidget(apps_btn)
        layout.addStretch(1)

        self.setLayout(layout)

        self.start_menu = None
        self.ai_console = None
        self.app_launcher = None
        self.menu_open = False    

    def launch_app(self, app_name):

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
            return
        except Exception:
            pass

        try:
            os.system(f"{app_name} &")
        except Exception as e:
            print("Launcher error:", e)

    def toggle_start_menu(self):
        if self.start_menu and self.menu_open:
            self.start_menu.animate_hide()
            self.menu_open = False
            return

        if not self.start_menu:
            self.start_menu = StartMenu(self.launch_app, parent=self.window())

        main_win = self.window()
        if main_win:
            x = 10
            y = main_win.height() - self.start_menu.height() - self.height() - 10
            self.start_menu.animate_show(x, y)

        self.menu_open = True

    def toggle_app_launcher(self):
        if self.app_launcher and self.app_launcher.isVisible():
            self.app_launcher.hide()
            return

        if not self.app_launcher:
            self.app_launcher = AppLauncher(self.launch_app, parent=self.window())

        main_win = self.window()
        if main_win:
            x = (main_win.width() - self.app_launcher.width()) // 2
            y = (main_win.height() - self.app_launcher.height()) // 2
            self.app_launcher.move(x, y)

        self.app_launcher.show()

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
