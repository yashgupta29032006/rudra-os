# rudra_gui/notify.py
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal, QDateTime

class Notification:
    def __init__(self, title: str, message: str, ts=None):
        self.title = title
        self.message = message
        self.ts = ts or QDateTime.currentDateTime()

class NotificationManager(QObject):
    changed = pyqtSignal()

    def __init__(self, max_items=100):
        super().__init__()
        self.max_items = max_items
        self.items = deque(maxlen=max_items)

    def add(self, title: str, message: str):
        n = Notification(title, message)
        self.items.appendleft(n)
        self.changed.emit()

    def list(self):
        return list(self.items)

_global_manager = NotificationManager()

def notify(title: str, message: str):
    _global_manager.add(title, message)

def get_manager():
    return _global_manager
