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


class Maps_WA(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(width // 2- 512, height // 2 - 352, 1024, 704)
        self.setWindowTitle('Карты')

        self.coords = QLineEdit(self)
        self.coords.resize(160, 40)
        self.coords.move(10, 5)

        self.second_value = QLineEdit(self)
        self.second_value.resize(160, 40)
        self.second_value.move(10, 60)

        self.second_value = QLineEdit(self)
        self.second_value.resize(160, 40)
        self.second_value.move(10, 60)

        self.trick_button = QPushButton('->', self)
        self.trick_button.resize(40, 40)
        self.trick_button.move(180, 5)

        self.simage = QPixmap('map.png').scaled(750, 563)
        razmer = self.simage.size()
        self.image = QLabel(self)
        self.image.move(220, 50)
        self.image.resize(razmer)
        self.image.setPixmap(self.simage)

        self.trick_button.clicked.connect(self.switch)

    def switch(self):
        if self.trick_button.text() == '->':
            self.trick_button.setText('<-')
            self.second_value.setText(self.coords.text())
            self.coords.setText('')
        else:
            self.trick_button.setText('->')
            self.coords.setText(self.second_value.text())
            self.second_value.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maps_WA()
    ex.show()
    sys.exit(app.exec())
