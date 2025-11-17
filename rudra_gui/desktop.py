from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from rudra_gui.taskbar import Taskbar
import sys

class RudraDesktop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rudra OS Desktop")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #121212;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QLabel("RUDRA OS")
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        layout.addStretch(1)

        taskbar = Taskbar()
        layout.addWidget(taskbar)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()


def start_desktop():
    app = QApplication(sys.argv)
    desktop = RudraDesktop()
    desktop.showFullScreen()
    sys.exit(app.exec())
