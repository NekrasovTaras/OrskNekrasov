import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import requests
import os
import keyboard


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTmain.ui', self)
        self.button_find.clicked.connect(self.receiving_data)
        self.gibrid_button.clicked.connect(self.gibrid_on)
        self.sputnik_button.clicked.connect(self.sputnik_on)
        self.shema_button.clicked.connect(self.shema_on)
        self.reset_button.clicked.connect(self.reset)
        self.width = 0
        self.longitude = 0
        self.scale_user = 0
        self.gibrid = False
        self.sputnik = False
        self.map_is_visible = False

    def receiving_data(self):
        try:
            self.width = float(self.spin_S.value())
            self.longitude = float(self.spin_D.value())
            self.scale_user = int(self.scale_sipin_box.value())
            self.map_is_visible = True
        except Exception:
            error_window('Неправильный формат данных')
            return
        self.click_tracking()
        self.map_image()
        self.spin_S.setEnabled(False)
        self.spin_D.setEnabled(False)
        self.place.setEnabled(False)
        self.scale_sipin_box.setEnabled(False)
        self.button_find.setEnabled(False)

    def gibrid_on(self):
        self.gibrid = self.gibrid_button.isChecked()

    def sputnik_on(self):
        self.sputnik = self.sputnik_button.isChecked()

    def shema_on(self):
        self.gibrid = self.sputnik = False

    def map_image(self):
        if self.gibrid:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.width},{self.longitude}&z={self.scale_user}&l=sat,skl&size=650,450"
        elif self.sputnik:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.width},{self.longitude}&z={self.scale_user}&l=sat&size=650,450"
        else:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.width},{self.longitude}&z={self.scale_user}&l=map&size=650,450"
        response = requests.get(ya_statick)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.photo_label.setPixmap(QPixmap(map_file))

    def KeyboardEventReceived(self, event):
        if event.event_type == 'down':
            if event.scan_code == 73:
                if self.scale_user + 1 <= 17:
                    self.scale_user += 1
                    self.map_image()
            elif event.scan_code == 81:
                if self.scale_user - 1 >= 1:
                    self.scale_user -= 1
                    self.map_image()
            elif event.scan_code == 72:
                if self.longitude + 10 / self.scale_user ** 2 <= 90:
                    self.longitude += 10 / self.scale_user ** 2
                    self.map_image()
            elif event.scan_code == 80:
                if self.longitude - 10 / self.scale_user ** 2 >= -90:
                    self.longitude -= 10 / self.scale_user ** 2
                    self.map_image()
            elif event.scan_code == 75:
                if self.width - 10 / self.scale_user ** 2 >= -180:
                    self.width -= 10 / self.scale_user ** 2
                    self.map_image()
            elif event.scan_code == 77:
                if self.width + 10 / self.scale_user ** 2 <= 180:
                    self.width += 10 / self.scale_user ** 2
                    self.map_image()

    def click_tracking(self):
        if self.map_is_visible:
            self.hook = keyboard.on_press(self.KeyboardEventReceived)

    def reset(self):
        self.spin_S.setEnabled(True)
        self.spin_S.setValue(0)
        self.spin_D.setEnabled(True)
        self.spin_D.setValue(0)
        self.place.setEnabled(True)
        self.place.setText("")
        self.scale_sipin_box.setEnabled(True)
        self.scale_sipin_box.setValue(1)
        self.button_find.setEnabled(True)
        self.gibrid = False
        self.sputnik = False
        self.map_is_visible = False
        self.width = self.longitude = 0
        self.scale_user = 1
        self.map_image()
        keyboard.unhook(self.hook)


def error_window(text):
    ERROR = QMessageBox()
    ERROR.setWindowTitle('Упс, что-то пошло не так... 🤔')
    ERROR.setText(text)
    ERROR.setIcon(QMessageBox.Warning)
    ERROR.setStandardButtons(QMessageBox.Cancel)
    ERROR.exec_()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())
