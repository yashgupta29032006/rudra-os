from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from rudra_gui.clock_panel import ClockPanel


class SystemTray(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(40)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(16)

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

        # --- Clock (clickable) ---
        self.clock = QLabel()
        self.clock.setObjectName("clockLabel")
        self.clock.setStyleSheet("""
            QLabel#clockLabel {
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding-right: 6px;
            }
        """)
        layout.addWidget(self.clock)

        self.setLayout(layout)

        # Timer to update clock every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

        # For calendar panel
        self.clock.mousePressEvent = self.toggle_clock_panel
        self.clock_panel = None
        self.panel_open = False

    # --------------------------------------------------------
    # Clock update logic
    # --------------------------------------------------------
    def update_clock(self):
        current_time = QTime.currentTime().toString("hh:mm")
        self.clock.setText(current_time)

    # --------------------------------------------------------
    # Click to open/close the calendar panel
    # --------------------------------------------------------
    def toggle_clock_panel(self, event):
        if not self.clock_panel:
            self.clock_panel = ClockPanel(self.parent())

        # If already open => close it
        if self.panel_open:
            self.clock_panel.animate_hide()
            self.panel_open = False
            return

        # If closed => open it
        parent = self.parent()
        if parent:
            x = parent.width() - self.clock_panel.width() - 10
            y = parent.height() - self.clock_panel.height() - 60

            self.clock_panel.animate_show(x, y)
            self.panel_open = True
