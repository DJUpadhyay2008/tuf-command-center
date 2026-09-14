import sys
import os
from PyQt6.QtWidgets import QApplication
from ui_main import AsusGuiWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ASUS TUF Control Center")
    app.setOrganizationName("AsusctlGUI")
    
    window = AsusGuiWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

