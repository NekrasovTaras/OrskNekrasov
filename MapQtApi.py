import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import os
from Samples.geocoder import get_ll_span


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTmain.ui', self)
        self.gibrid_button.clicked.connect(self.gibrid_on)
        self.sputnik_button.clicked.connect(self.sputnik_on)
        self.shema_button.clicked.connect(self.shema_on)
        self.reset_button.clicked.connect(self.reset)
        self.button_find_object.clicked.connect(self.mark_image)
        self.spn = [0.3, 0.3]
        self.coordinates = [37.617644, 55.755819]
        self.map_type = []
        self.mark_on = False
        self.shema_on()

    def sputnik_on(self):
        self.map_type.append("sputnik_on")
        if self.mark_on:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat,skl&size=650,450&{self.point_param}"
        else:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat,skl&size=650,450"
        self.map_image(ya_statick)

    def sputnik_on(self):
        self.map_type.append("sputnik_on")
        if self.mark_on:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat&size=650,450&{self.point_param}"
        else:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat&size=650,450"
        self.map_image(ya_statick)

    def shema_on(self):
        self.map_type.append("shema_on")
        if self.mark_on:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=map&size=650,450&{self.point_param}"
        else:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=map&size=650,450"
        self.map_image(ya_statick)

    def map_image(self, ya_statick):
        response = requests.get(ya_statick)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        pixmap = QPixmap(map_file)
        self.photo_label.setPixmap(pixmap)
        os.remove(map_file)

    def mark_image(self):
        try:
            self.mark_on = True
            self.toponym_to_find = self.place.text()
            if self.map_type[-1] == "gibrid_on":
                map_type = "sat,skl"
            elif self.map_type[-1] == "shema_on":
                map_type = "map"
            else:
                map_type = "sat"
            ll, spn = get_ll_span(self.toponym_to_find)
            ll_spn = f"ll={ll}&spn={spn}"
            self.point_param = f"pt={ll}"
            self.spn = spn
            self.spn = spn.split(",")
            self.spn[0] = float(self.spn[0])
            self.spn[1] = float(self.spn[1])
            self.coordinates = ll.split(",")
            self.coordinates[0] = float(self.coordinates[0])
            self.coordinates[1] = float(self.coordinates[1])
            map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
            map_request += "&" + self.point_param
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            map_file = 'map.png'
            with open(map_file, "wb") as file:
                file.write(response.content)
            pixmap = QPixmap(map_file)
            self.photo_label.setPixmap(pixmap)
        except Exception:
            error_window('Неправильный формат данных')
            self.reset()

    def checked(self):
        if self.map_type[-1] == "gibrid_on":
            self.gibrid_on()
        elif self.map_type[-1] == "shema_on":
            self.shema_on()
        else:
            self.sputnik_on()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp:
            self.spn[0] = self.spn[0] / 2
            self.spn[1] = self.spn[1] / 2
            self.checked()
        elif key == Qt.Key_PageDown:
            self.spn[0] = self.spn[0] * 2
            self.spn[1] = self.spn[1] * 2
            self.checked()
        elif key == Qt.Key_Left:
            self.coordinates[0] -= self.spn[0] + self.spn[1]
            self.checked()
        elif key == Qt.Key_Right:
            self.coordinates[0] += self.spn[0] + self.spn[1]
            self.checked()
        elif key == Qt.Key_Up:
            self.coordinates[1] += self.spn[0] + self.spn[1]
            self.checked()
        elif key == Qt.Key_Down:
            self.coordinates[1] -= self.spn[0] + self.spn[1]
            self.checked()

    def reset(self):
        pass


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
    window.photo_label.setFocus()
    sys.exit(app.exec())
