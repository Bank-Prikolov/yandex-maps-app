import sys
from dataclasses import dataclass, field
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QRadioButton,
)

import requests


@dataclass
class MapsData:
    spn: float = 0.003
    coords: List[float] = field(default_factory=list)
    display: str = 'map'
    pt: str = ''
    postal_code: str = ''
    address: str = ''


def get_place_map(data) -> requests.Response:
    """получаем ответ от static maps"""
    map_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'spn': f'{data.spn},{data.spn}',
        'pt': data.pt,
        'size': '619,429',
    }

    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return response


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.data = None
        self.map_type_choices = None
        self.setupUI()

    def setupUI(self):
        self.setupData()
        uic.loadUi('data/MainWindow.ui', self)
        self.setWindowTitle('Maps')
        self.mapTypeGroup.buttonClicked.connect(self.chooseMapType)
        self.buttonSearch.clicked.connect(self.searchPlace)
        self.getPicture()

    def searchPlace(self):
        pass

    def setupData(self) -> None:
        self.data = MapsData()
        self.data.coords = [30.312363709126018, 59.94157564755226]
        self.map_type_choices = {
            'Схема': 'map',
            'Спутник': 'sat',
            'Гибрид': 'sat,skl',
        }

    def getPicture(self) -> None:
        """получаем картинку запросом"""
        response = get_place_map(self.data)
        if response:
            self.setPicture(response)
        else:
            self.showMessage(
                'reqerror',
                f'Ошибка запроса: {response.status_code}. '
                f'Причина: {response.reason}, {response.request.url}',
            )

    def setPicture(self, response: requests.Response) -> None:
        with open('image.png', 'wb') as file:
            file.write(response.content)
        pixmap = QPixmap('image.png')
        pixmap_rounded = QPixmap(pixmap.size())
        pixmap_rounded.fill(Qt.transparent)
        painter = QPainter(pixmap_rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 12
        rect = QRectF(QRect(0, 0, pixmap.width(), pixmap.height()))
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        self.map.setPixmap(pixmap_rounded)

    def chooseMapType(self, button: QRadioButton):
        self.data.display = self.map_type_choices[button.text()]
        self.getPicture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
