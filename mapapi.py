import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MapQT
import pygame
import requests
import os
from PyQt5.QtWidgets import QMessageBox


class Window(Ui_MapQT, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_find_maoa.clicked.connect(self.letsgo)
        self.Gibrid.clicked.connect(self.gibr)
        self.Sputnik.clicked.connect(self.sputni)
        self.Sxema.clicked.connect(self.shema)

    def letsgo(self):
        try:
            self.shir = float(self.spin_S.value())
            self.dolg = float(self.spin_D.value())
            self.z = int(self.scale.value())
        except Exception:
            ERROR_WINDOW('Неправильный формат данных')
            return
        self.gib = self.Gibrid.isChecked()
        self.spu = self.Sputnik.isChecked()
        post = self.checkBox.isChecked()
        place = self.place.text()
        ya_map = PGMap(self.shir, self.dolg, self.z)

    def gibr(self):
        self.gib = self.Gibrid.isChecked()
        print(self.gib)

    def sputni(self):
        self.spu = self.Sputnik.isChecked()
        print(self.spu)

    def shema(self):
        self.gib = self.spu = False


class PGMap:
    def __init__(self, SH, DL, z):
        self.shirina = SH
        self.dolgota = DL
        self.scale = z
        if window.gib:
            ya_statick =\
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=sat,skl"
        elif window.spu:
            ya_statick =\
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=sat"
        else:
            ya_statick =\
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=map"
        response = requests.get(ya_statick)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        pygame.init()
        self.screen = pygame.display.set_mode((600, 450))
        self.screen.blit(pygame.image.load(map_file), (0, 0))
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                key = pygame.key.get_pressed()
                if key[pygame.K_UP]:
                    if self.dolgota + 5 / self.scale ** 2 <= 90:
                        self.dolgota += 5 / self.scale ** 2
                        self.zamena()
                elif key[pygame.K_DOWN]:
                    if self.dolgota - 5 / self.scale ** 2 >= -90:
                        self.dolgota -= 5 / self.scale ** 2
                        self.zamena()
                elif key[pygame.K_LEFT]:
                    if self.shirina - 5 / self.scale ** 2 >= -180:
                        self.shirina -= 5 / self.scale ** 2
                        self.zamena()
                elif key[pygame.K_RIGHT]:
                    if self.shirina + 5 / self.scale ** 2 <= 180:
                        self.shirina += 5 / self.scale ** 2
                        self.zamena()
                elif key[pygame.K_PAGEDOWN]:
                    if self.scale - 1 >= 1:
                        self.scale -= 1
                        self.zamena()
                elif key[pygame.K_PAGEUP]:
                    if self.scale + 1 <= 17:
                        self.scale += 1
                        self.zamena()
            pygame.display.flip()
        pygame.quit()
        os.remove(map_file)

    def zamena(self):
        if window.gib:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=sat,skl"
        elif window.spu:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=sat"
        else:
            ya_statick = \
                f"https://static-maps.yandex.ru/1.x/?ll={self.shirina},{self.dolgota}&z={self.scale}&l=map"
        response = requests.get(ya_statick)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.screen.blit(pygame.image.load(map_file), (0, 0))


def ERROR_WINDOW(text):
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