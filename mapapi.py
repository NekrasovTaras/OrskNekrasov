import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MapQT
import pygame
import requests
import os
from  PyQt5.QtWidgets import QMessageBox


class Window(Ui_MapQT, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_find_maoa.clicked.connect(self.letsgo)

    def letsgo(self):
        try:
            self.shir = int(self.lineEdit_S.text())
            self.dolg = int(self.lineEdit_D.text())
            self.scale = int(self.scale.text())
        except Exception:
            self.ERROR_WINDOW('Неправильный формат данных')
        self.gib = self.Gibrid.isChecked()
        self.spu = self.Sputnik.isChecked()
        post = self.checkBox.isChecked()
        place = self.place.text()
        try:
            if self.gib:
                ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=sat,skl"
            elif self.spu:
                ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=sat"
            else:
                ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=map"
            response = requests.get(ya_statick)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            pygame.init()
            self.screen = pygame.display.set_mode((600, 450))
            self.screen.blit(pygame.image.load(map_file), (0, 0))
        except Exception:
            self.ERROR_WINDOW('Не удалось найти карту')
            pygame.quit()
            return
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            self.pg_update()
        pygame.quit()
        os.remove(map_file)

    def pg_update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.dolg += 5
            self.lineEdit_D.setText(str(self.dolg))
        if key[pygame.K_DOWN]:
            self.dolg -= 5
            self.lineEdit_D.setText(str(self.dolg))
        if key[pygame.K_LEFT]:
            self.shir += 5
            self.lineEdit_S.setText(str(self.shir))
        if key[pygame.K_RIGHT]:
            self.shir -= 5
            self.lineEdit_S.setText(str(self.shir))
        if self.gib:
            ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=sat,skl"
        elif self.spu:
            ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=sat"
        else:
            ya_statick = f"https://static-maps.yandex.ru/1.x/?ll={self.shir},{self.dolg}&z={self.scale}&l=map"
        response = requests.get(ya_statick)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.screen.blit(pygame.image.load(map_file), (0, 0))

    def ERROR_WINDOW(self, text):
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
    window = Window()
    window.show()
    sys.exit(app.exec())