import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import os
from Samples.geocoder import get_ll_span, get_nearest_object
from Samples.business import find_business, find_businesses


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTmain.ui', self)
        self.gibrid_button.clicked.connect(self.gibrid_on)
        self.sputnik_button.clicked.connect(self.sputnik_on)
        self.shema_button.clicked.connect(self.shema_on)
        self.reset_button.clicked.connect(self.reset)
        self.button_find_object.clicked.connect(self.mark_image)
        self.postal_code_button.clicked.connect(self.postal_code_click)
        self.spn = [0.3, 0.3]
        self.coordinates = [37.617644, 55.755819]
        self.map_type = ['map']
        self.mark_on = False
        self.point_param = ''
        self.shema_on()
        self.ll_spn = f"ll={self.coordinates[0]}"
        self.ll_spn += f",{self.coordinates[1]}"
        self.ll_spn += f"&spn={self.spn[0]}"
        self.ll_spn += f",{self.spn[1]}"

    def sputnik_on(self):
        self.map_type.append("sat")
        ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat&size=650,450&{self.point_param}"
        self.map_image(ya_statick)

    def gibrid_on(self):
        self.map_type.append("sat,skl")
        ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=sat,skl&size=650,450&{self.point_param}"
        self.map_image(ya_statick)

    def shema_on(self):
        self.map_type.append("map")
        ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l=map&size=650,450&{self.point_param}"
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
        self.mark_on = True
        self.toponym_to_find = self.place.text()
        ll, spn = get_ll_span(self.toponym_to_find)
        self.ll_spn = f"ll={ll}&spn={spn}"
        self.point_param = f"pt={ll}"
        self.spn = spn
        self.spn = spn.split(",")
        self.spn[0] = float(self.spn[0])
        self.spn[1] = float(self.spn[1])
        self.coordinates = ll.split(",")
        self.coordinates[0] = float(self.coordinates[0])
        self.coordinates[1] = float(self.coordinates[1])
        self.map_request = f"http://static-maps.yandex.ru/1.x/?{self.ll_spn}&l={self.map_type[-1]}&&size=650,450"
        self.map_request += "&" + self.point_param
        response = requests.get(self.map_request)
        map_file = 'map.png'
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.adress = get_nearest_object(self.coordinates, kind="house")
        try:
            self.postal_code_click()
        except Exception:
            self.adress_label.setText('Не удалось загрузить полный адрес :(')
        pixmap = QPixmap(map_file)
        self.photo_label.setPixmap(pixmap)

    def mark_from_click(self, mark_ll, org=False):
        self.point_param = f"pt={mark_ll[0]}"
        if org:
            self.point_param += f",{mark_ll[1]},pm2rdm"
        else:
            self.point_param += f",{mark_ll[1]},pm2blm"
        self.map_request = f"http://static-maps.yandex.ru/1.x/?{self.ll_spn}&l={self.map_type[-1]}&&size=650,450"
        self.map_request += "&" + self.point_param
        print(self.map_request)
        response = requests.get(self.map_request)
        map_file = 'map.png'
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.adress = get_nearest_object([mark_ll[0], mark_ll[1]], kind="house")
        if self.adress:
            self.postal_code_click()
        pixmap = QPixmap(map_file)
        self.photo_label.setPixmap(pixmap)

    def postal_code_click(self):
        if self.postal_code_button.isChecked():
            if self.adress['postal_code']:
                self.adress_label.setText(self.adress["formatted"] + ", " + self.adress["postal_code"])
        else:
            self.adress_label.setText(self.adress["formatted"])

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp:
            self.spn[0] = self.spn[0] / 2
            self.spn[1] = self.spn[1] / 2
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")
        elif key == Qt.Key_PageDown:
            self.spn[0] = self.spn[0] * 2
            self.spn[1] = self.spn[1] * 2
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")
        elif key == Qt.Key_Left:
            self.coordinates[0] -= self.spn[0] + self.spn[1]
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")
        elif key == Qt.Key_Right:
            self.coordinates[0] += self.spn[0] + self.spn[1]
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")
        elif key == Qt.Key_Up:
            self.coordinates[1] += self.spn[0] + self.spn[1]
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")
        elif key == Qt.Key_Down:
            self.coordinates[1] -= self.spn[0] + self.spn[1]
            self.ll_spn = f"ll={self.coordinates[0]}"
            self.ll_spn += f",{self.coordinates[1]}"
            self.ll_spn += f"&spn={self.spn[0]}"
            self.ll_spn += f",{self.spn[1]}"
            self.map_image(
                f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coordinates[0]},{self.coordinates[1]}'}&spn={f'{self.spn[0]},{self.spn[1]}'}&l={self.map_type[-1]}&size=650,450&{self.point_param}")

    def mousePressEvent(self, event):
        self.adress_label.clear()
        x = event.x()
        y = event.y()
        if 500 <= x <= 1150 and 110 <= y <= 560:
            x -= 500
            y -= 110
            new_x = (x - 320) * self.spn[0] * 1.5 / 320
            new_y = (y - 225) * self.spn[0] * 0.58 / 225
            new_pt_ll = [self.coordinates[0] + new_x, self.coordinates[1] - new_y]
            if event.button() == Qt.LeftButton:
                self.mark_from_click(new_pt_ll)
            elif event.button() == Qt.RightButton:
                organization = find_business(f"{new_pt_ll[0]},{new_pt_ll[1]}", "0.00000005,0.00000005", "organization")
                try:
                    point = organization["geometry"]["coordinates"]
                    org_lat = float(point[0])
                    org_lon = float(point[1])
                    point_param = [org_lat, org_lon]
                    self.mark_from_click(point_param, org=True)
                except Exception:
                    self.adress_label.setText('Нет организаций поблизности')


    def reset(self):
        self.mark_on = False
        self.adress_label.setText("")
        self.point_param = ''


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
