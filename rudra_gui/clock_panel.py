from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QFrame
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect

class ClockPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(300, 380)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #303030;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
        """)

        self.opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)

        self.slide = QPropertyAnimation(self, b"pos")
        self.fade = QPropertyAnimation(self.opacity, b"opacity")

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.date_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color:#444;")
        layout.addWidget(line)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget QAbstractItemView {
                background-color:#2a2a2a;
                color:white;
                selection-background-color:#3a3cff;
            }
        """)
        layout.addWidget(self.calendar)

        self.setLayout(layout)

    def update_date(self):
        from datetime import datetime
        now = datetime.now().strftime("%A, %d %B %Y")
        self.date_label.setText(now)

    def animate_show(self, x, y):
        sy = y + 40
        self.move(x, sy)
        self.show()
        self.update_date()

        self.slide.setDuration(200)
        self.slide.setStartValue(QPoint(x, sy))
        self.slide.setEndValue(QPoint(x, y))
        self.slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade.setDuration(200)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)

        self.slide.start()
        self.fade.start()

    def animate_hide(self):
        x, y = self.x(), self.y()
        ey = y + 40

        self.slide.setDuration(150)
        self.slide.setStartValue(QPoint(x, y))
        self.slide.setEndValue(QPoint(x, ey))
        self.slide.setEasingCurve(QEasingCurve.Type.InCubic)

        self.fade.setDuration(150)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0)

        def finish():
            self.hide()

        try:
            self.fade.finished.disconnect()
        except:
            pass

        self.fade.finished.connect(finish)
        self.slide.start()
        self.fade.start()
