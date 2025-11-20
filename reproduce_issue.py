
import sys
from PyQt6.QtWidgets import QApplication, QPushButton
from rudra_gui.desktop import RudraDesktop
from PyQt6.QtCore import Qt, QTimer

def test_notification():
    app = QApplication(sys.argv)
    desktop = RudraDesktop()
    desktop.show()

    # Find the taskbar
    taskbar = desktop.findChild(object, "RUDRA_TASKBAR")
    if not taskbar:
        print("Taskbar not found")
        sys.exit(1)

    print("Taskbar found")
    
    # Check if bell is now a QPushButton
    if not hasattr(taskbar, 'bell'):
        print("Bell not found on taskbar")
        sys.exit(1)
        
    if not isinstance(taskbar.bell, QPushButton):
        print(f"Bell is NOT a QPushButton, it is {type(taskbar.bell)}")
        sys.exit(1)
        
    print("Bell is a QPushButton. Simulating click...")
    
    # Simulate click via signal
    taskbar.bell.click()
    
    # Check if notification panel is created and visible
    if taskbar.notification_panel:
        print(f"Notification panel created: {taskbar.notification_panel}")
        # Note: isVisible might be false immediately if animation takes time or if not shown yet?
        # But toggle_notifications calls animate_show which calls show()
        print(f"Notification panel visible: {taskbar.notification_panel.isVisible()}")
    else:
        print("Notification panel NOT created")

    QTimer.singleShot(1000, app.quit)
    app.exec()

if __name__ == "__main__":
    test_notification()
