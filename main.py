import sys
import json

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QRadioButton,
    QPushButton,
    QLineEdit,
)

import requests


class Maps_WA(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 500, 400, 50)
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
