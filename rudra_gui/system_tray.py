from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QIcon

class SystemTray(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(40)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(15)

        # --- Volume Icon ---
        self.volume = QLabel("🔊")
        self.volume.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.volume)

        # --- WiFi Icon ---
        self.wifi = QLabel("📶")
        self.wifi.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.wifi)

        # --- Battery Icon ---
        self.battery = QLabel("🔋")
        self.battery.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.battery)

        # --- Clock ---
        self.clock = QLabel()
        self.clock.setStyleSheet("color: white; font-weight: bold; font-size: 15px;")
        layout.addWidget(self.clock)

        self.setLayout(layout)

        # update time every 1 second
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)

        self.update_clock()

    def update_clock(self):
        time = QTime.currentTime().toString("hh:mm")
        self.clock.setText(time)
