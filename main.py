# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import SortingSimulatorMainWindow

def main():
    app = QApplication(sys.argv)
    window = SortingSimulatorMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()