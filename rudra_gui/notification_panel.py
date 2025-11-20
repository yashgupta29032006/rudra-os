# rudra_gui/notification_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QFrame, QScrollArea, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from rudra_gui.notify import get_manager
from PyQt6.QtCore import QDateTime

class NotificationWidget(QWidget):
    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QLabel.title {
                color: #fff;
                font-weight: 600;
            }
            QLabel.message {
                color: #ddd;
            }
            QLabel.ts {
                color: #aaa;
                font-size: 11px;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        title = QLabel(self.notification.title)
        title.setObjectName("title")
        title.setProperty("class", "title")
        title.setStyleSheet("font-size:14px;")

        message = QLabel(self.notification.message)
        message.setObjectName("message")
        message.setWordWrap(True)
        message.setStyleSheet("font-size:12px;")

        ts = QLabel(self.notification.ts.toString("hh:mm ap"))
        ts.setObjectName("ts")
        ts.setStyleSheet("font-size:11px;")

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addWidget(ts, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.setFixedWidth(320)


class NotificationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, int(parent.height() * 0.6) if parent else 500)

        self.container = QWidget(self)
        self.container.setObjectName("panel_container")
        self.container.setGeometry(0, 0, self.width(), self.height())
        self.container.setStyleSheet("""
            QWidget#panel_container {
                background: rgba(28,28,30,0.72);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.06);
                backdrop-filter: blur(8px);
            }
        """)

        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)

        self.slide_anim = QPropertyAnimation(self, b"pos")
        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")

        cr = QVBoxLayout(self.container)
        cr.setContentsMargins(12, 12, 12, 12)
        cr.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("Notifications")
        title.setStyleSheet("color: white; font-weight: 700; font-size: 16px;")
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("""
            QPushButton { color: #ddd; background: transparent; border: none; }
            QPushButton:hover { color: white; }
        """)
        clear_btn.clicked.connect(self.clear_notifications)
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(clear_btn)
        cr.addLayout(header)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: rgba(255,255,255,0.06);")
        cr.addWidget(divider)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(8)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)

        cr.addWidget(self.scroll)

        self.manager = get_manager()
        self.manager.changed.connect(self.reload_notifications)
        self.reload_notifications()

        self.panel_open = False

    def clear_notifications(self):
        # naive clear by reinitializing manager.items deque (import inside to avoid circular)
        from rudra_gui.notify import _global_manager
        _global_manager.items.clear()
        _global_manager.changed.emit()

    def reload_notifications(self):
        # remove old
        for i in reversed(range(self.scroll_layout.count())):
            w = self.scroll_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        items = self.manager.list()
        for n in items:
            w = NotificationWidget(n)
            card = QWidget()
            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(8,8,8,8)
            card.setStyleSheet("""
                QWidget {
                    background: rgba(255,255,255,0.03);
                    border-radius: 8px;
                }
            """)
            card_layout.addWidget(w)
            card.setLayout(card_layout)
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch(1)

    def animate_show(self, x, y):
        parent = self.window()  # Correct parent reference

        # slide from the right edge of the window
        start_pos = QPoint(parent.width(), y)
        end_pos = QPoint(x, y)

        self.move(start_pos)
        self.show()

        self.slide_anim.setDuration(250)
        self.slide_anim.setStartValue(start_pos)
        self.slide_anim.setEndValue(end_pos)
        self.slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade_anim.setDuration(250)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)

        self.slide_anim.start()
        self.fade_anim.start()


    def animate_hide(self):
        parent = self.window()

        cur = self.pos()
        end = QPoint(parent.width(), cur.y())  # slide to right edge

        self.slide_anim.setDuration(180)
        self.slide_anim.setStartValue(cur)
        self.slide_anim.setEndValue(end)
        self.slide_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        self.fade_anim.setDuration(160)
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)

        def finish():
            self.hide()

        try:
            self.fade_anim.finished.disconnect()
        except:
            pass

        self.fade_anim.finished.connect(finish)
        self.slide_anim.start()
        self.fade_anim.start()

