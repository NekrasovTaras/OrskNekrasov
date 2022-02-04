import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MapQT


class Window(Ui_MapQT, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())