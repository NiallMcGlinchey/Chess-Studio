import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

ROOT = Path(__file__).resolve().parent

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Chess Studio")
    app.setOrganizationName("Chess Studio")
    window = MainWindow(ROOT)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
