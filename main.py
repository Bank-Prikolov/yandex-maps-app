import sys
import json
import os
from dataclasses import dataclass, field

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
)

import requests

size = width, height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
req = "https://static-maps.yandex.ru/v1"
params = {"apikey": os.getenv("API_KEY")}

@dataclass
class MapsData:
    spn: float = 0.003
    display: str = 'map'
    pt: str = ''
    postal_code: str = ''
    address: str = ''

class Maps_WA(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 500, 1024, 704)
        self.setWindowTitle('Карты')

        self.first_value = QLineEdit(self)
        self.first_value.resize(160, 40)
        self.first_value.move(10, 5)

        self.second_value = QLineEdit(self)
        self.second_value.resize(160, 40)
        self.second_value.move(230, 5)

        self.trick_button = QPushButton('->', self)
        self.trick_button.resize(40, 40)
        self.trick_button.move(180, 5)

        self.trick_button.clicked.connect(self.switch)

    def switch(self):
        if self.trick_button.text() == '->':
            self.trick_button.setText('<-')
            self.second_value.setText(self.first_value.text())
            self.first_value.setText('')
        else:
            self.trick_button.setText('->')
            self.first_value.setText(self.second_value.text())
            self.second_value.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Maps_WA()
    ex.show()
    sys.exit(app.exec())
