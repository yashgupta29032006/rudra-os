from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QPoint
from rudra_gui.start_menu import StartMenu
from rudra_gui.ai_console import AIConsole
from rudra_gui.app_launcher import AppLauncher
from rudra_gui.system_tray import SystemTray
from rudra_gui.notification_panel import NotificationPanel
from PyQt6.QtCore import Qt
import subprocess
import os

class Taskbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("RUDRA_TASKBAR")

        self.setFixedHeight(50)
        self.setStyleSheet("background-color:#202020;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10,2,10,2)

        start_btn = QPushButton("RUDRA")
        start_btn.setStyleSheet("""
            QPushButton {
                background:#3a3cff;
                color:white;
                padding:8px;
                font-weight:bold;
                border-radius:4px;
            }
            QPushButton:hover { background:#5757ff; }
        """)
        start_btn.clicked.connect(self.toggle_start_menu)

        apps_btn = QPushButton("Apps")
        apps_btn.setStyleSheet("""
            QPushButton {
                background:#444;
                color:white;
                padding:6px;
                border-radius:4px;
            }
            QPushButton:hover { background:#555; }
        """)
        apps_btn.clicked.connect(self.toggle_app_launcher)

        layout.addWidget(start_btn)
        layout.addWidget(apps_btn)
        layout.addStretch(1)
        self.system_tray = SystemTray(self)
        layout.addWidget(self.system_tray)
        self.setLayout(layout)

        self.bell = QLabel("🔔")
        self.bell.setStyleSheet("color: white; font-size: 18px;")
        self.bell.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bell.mousePressEvent = self.toggle_notifications
        layout.insertWidget(layout.count()-1, self.bell)  

        self.notification_panel = None
        self.notifications_open = False

        self.start_menu = None
        self.ai_console = None
        self.app_launcher = None
        self.menu_open = False

    def launch_app(self, app):
        if app == "shutdown":
            win = self.window()
            if win: win.close()
            return

        if app == "rudra_ai":
            self.open_ai_console()
            return

        try:
            subprocess.Popen([app])
        except:
            os.system(f"{app} &")

    def toggle_notifications(self, event=None):
        if event and hasattr(event, 'accept'):
            event.accept()
        if not self.notification_panel:
            self.notification_panel = NotificationPanel(self.window())

        if self.notifications_open:
            self.notification_panel.animate_hide()
            self.notifications_open = False
            return

        parent = self.window()
        if parent:
            x = parent.width() - self.notification_panel.width() - 12
            y = 80  
            self.notification_panel.animate_show(x, y)
            self.notifications_open = True

    def toggle_start_menu(self):
        if self.start_menu and self.menu_open:
            self.start_menu.animate_hide()
            return

        if not self.start_menu:
            self.start_menu = StartMenu(self.launch_app, self)

        win = self.window()
        x = 10
        y = win.height() - self.start_menu.height() - self.height() - 10
        self.start_menu.animate_show(x, y)

        self.menu_open = True

    def toggle_app_launcher(self):
        if self.app_launcher and self.app_launcher.isVisible():
            self.app_launcher.hide()
            return

        if not self.app_launcher:
            self.app_launcher = AppLauncher(self.launch_app, parent=self.window())

        win = self.window()
        x = (win.width() - self.app_launcher.width()) // 2
        y = (win.height() - self.app_launcher.height()) // 2
        self.app_launcher.move(x, y)
        self.app_launcher.show()

    def open_ai_console(self):
        if self.ai_console and self.ai_console.isVisible():
            self.ai_console.raise_()
            return

        self.ai_console = AIConsole(parent=self.window())
        win = self.window()
        x = (win.width() - self.ai_console.width()) // 2
        y = (win.height() - self.ai_console.height()) // 2
        self.ai_console.move(x, y)
        self.ai_console.show()
