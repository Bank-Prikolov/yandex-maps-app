import sys
import json
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import screeninfo
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QRadioButton,
    QPushButton,
    QLineEdit,
    QLabel
)

import requests

size = width, height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
# req = "http://static-maps.yandex.ru/1.x/"
# params = {"apikey": os.getenv("API_KEY"), }


class Maps(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(width // 2- 512, height // 2 - 352, 1024, 704)
        self.setWindowTitle('Карты')

        self.x = QLineEdit(self)
        self.x.resize(160, 40)
        self.x.move(10, 5)

        self.y = QLineEdit(self)
        self.y.resize(160, 40)
        self.y.move(10, 50)

        self.zoom = QLineEdit(self)
        self.zoom.resize(160, 40)
        self.zoom.move(10, 95)

        self.search = QPushButton('Поиск', self)
        self.search.resize(160, 40)
        self.search.move(10, 140)

        self.simage = QPixmap('map.png').scaled(750, 563)
        razmer = self.simage.size()
        self.image = QLabel(self)
        self.image.move(220, 50)
        self.image.resize(razmer)
        self.image.setPixmap(self.simage)

        self.search.clicked.connect(self.searchfunc)

    def searchfunc(self):
        x = self.x.text()
        y = self.y.text()
        zoom = self.zoom.text()
        map_request = f"http://static-maps.yandex.ru/1.x/?l=map&ll={x}%2C{y}&z={zoom}"
        response = requests.get(map_request)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.setpic()

    def setpic(self):
        self.simage = QPixmap('map.png').scaled(750, 563)
        razmer = self.simage.size()
        self.image = QLabel(self)
        self.image.move(220, 50)
        self.image.resize(razmer)
        self.image.setPixmap(self.simage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maps()
    ex.show()
    sys.exit(app.exec())
