from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class StartMenu(QWidget):
    def __init__(self, launch_app, parent=None):
        super().__init__(parent)
        self.launch_app = launch_app

        self.setFixedSize(420, 520)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #303030;
                border-radius: 8px;
            }
            QLineEdit {
                background-color: #2a2a2a;
                padding: 8px;
                color: white;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search apps, tools...")
        self.search.textChanged.connect(self.filter_apps)  
        layout.addWidget(self.search)

        pinned_label = QLabel("Pinned")
        pinned_label.setStyleSheet("color: #bbbbbb; padding-left: 4px;")
        layout.addWidget(pinned_label)

        pinned_layout = QHBoxLayout()
        pinned_apps = ["terminal", "files", "browser", "settings"]

        for app in pinned_apps:
            btn = QPushButton(app.capitalize())
            btn.clicked.connect(lambda _, name=app: self.launch_app(name))
            pinned_layout.addWidget(btn)

        layout.addLayout(pinned_layout)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #444;")
        layout.addWidget(divider)

        apps_label = QLabel("All Apps")
        apps_label.setStyleSheet("color: #bbbbbb; padding-left: 4px;")
        layout.addWidget(apps_label)

        self.apps_list = QListWidget()

        self.all_apps = [
            "terminal", "files", "browser", "editor", 
            "rudra_ai", "settings", "shutdown"
        ]

        self.load_apps(self.all_apps)

        self.apps_list.itemClicked.connect(self.handle_item_click)
        layout.addWidget(self.apps_list)

        self.setLayout(layout)

    def load_apps(self, apps):
        self.apps_list.clear()
        for app in apps:
            item = QListWidgetItem(f"  {app}")
            self.apps_list.addItem(item)

    def filter_apps(self, text):
        text = text.lower().strip()
        if text == "":
            self.load_apps(self.all_apps)
            return

        filtered = [app for app in self.all_apps if text in app.lower()]
        self.load_apps(filtered)

    def handle_item_click(self, item):
        app_name = item.text().strip()
        self.launch_app(app_name)
        self.hide()
