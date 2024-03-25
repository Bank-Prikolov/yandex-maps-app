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


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('data/MainWindow.ui', self)
        self.setWindowTitle('Maps')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
