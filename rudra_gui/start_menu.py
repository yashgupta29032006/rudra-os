from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QFrame,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve

class StartMenu(QWidget):
    def __init__(self, launch_app, taskbar):
        super().__init__(taskbar.window())
        self.launch_app = launch_app
        self.taskbar = taskbar

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
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QListWidget {
                background-color: #1c1c1c;
                color: white;
                border-radius: 5px;
            }
        """)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.slide_anim = QPropertyAnimation(self, b"pos")
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search apps...")
        self.search.textChanged.connect(self.filter_apps)
        layout.addWidget(self.search)

        pinned_label = QLabel("Pinned")
        pinned_label.setStyleSheet("color:#bbb; padding-left:4px;")
        layout.addWidget(pinned_label)

        pinned_row = QHBoxLayout()
        for app in ["terminal", "files", "browser", "settings"]:
            b = QPushButton(app.capitalize())
            b.clicked.connect(lambda _, a=app: self.launch_and_close(a))
            pinned_row.addWidget(b)
        layout.addLayout(pinned_row)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color:#444;")
        layout.addWidget(divider)

        apps_label = QLabel("All Apps")
        apps_label.setStyleSheet("color:#bbb; padding-left:4px;")
        layout.addWidget(apps_label)

        self.apps_list = QListWidget()
        self.all_apps = [
            "terminal", "files", "browser", "editor",
            "rudra_ai", "settings", "shutdown"
        ]
        self.load_apps(self.all_apps)
        self.apps_list.itemClicked.connect(self.on_item_click)
        layout.addWidget(self.apps_list)

        self.setLayout(layout)

    def load_apps(self, apps):
        self.apps_list.clear()
        for a in apps:
            self.apps_list.addItem(QListWidgetItem("  " + a))

    def filter_apps(self, text):
        t = text.lower().strip()
        if not t:
            self.load_apps(self.all_apps)
        else:
            self.load_apps([a for a in self.all_apps if t in a])

    def launch_and_close(self, app):
        self.launch_app(app)
        self.animate_hide()

    def on_item_click(self, item):
        self.launch_and_close(item.text().strip())

    def animate_show(self, x, y):
        sy = y + 40
        self.move(x, sy)
        self.show()

        try:
            self.fade_anim.finished.disconnect()
        except:
            pass

        self.slide_anim.setDuration(200)
        self.slide_anim.setStartValue(QPoint(x, sy))
        self.slide_anim.setEndValue(QPoint(x, y))
        self.slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade_anim.setDuration(200)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)

        self.search.setFocus()
        self.slide_anim.start()
        self.fade_anim.start()

    def animate_hide(self):
        if not self.isVisible():
            return

        x, y = self.x(), self.y()
        ey = y + 40

        self.slide_anim.setDuration(120)
        self.slide_anim.setStartValue(QPoint(x, y))
        self.slide_anim.setEndValue(QPoint(x, ey))
        self.slide_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        self.fade_anim.setDuration(120)
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)

        def finish():
            self.hide()
            self.taskbar.menu_open = False

        try:
            self.fade_anim.finished.disconnect()
        except:
            pass

        self.fade_anim.finished.connect(finish)
        self.slide_anim.start()
        self.fade_anim.start()
