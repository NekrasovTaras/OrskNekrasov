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
        self.place.setEnabled(False)
        self.button_find.setEnabled(False)

    def gibrid_on(self):
        ya_statick = \
            f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat,skl&size=650,450"
        self.map_image(ya_statick)

    def sputnik_on(self):
        ya_statick = \
            f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat&size=650,450"
        self.map_image(ya_statick)

    def shema_on(self):
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

    def mark_image(self):
        try:
            self.toponym_to_find = self.place.text()
            map_type = "sat"
            ll, spn = get_ll_span(self.toponym_to_find)
            ll_spn = f"ll={ll}&spn={spn}"
            point_param = f"pt={ll}"
            map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
            map_request += "&" + point_param
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

    def keyPressEvent(self, event):
        key = event.text()
        if key == Qt.Key_PageUp:
            print(1)
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
