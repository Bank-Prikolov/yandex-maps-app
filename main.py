from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent, QMouseEvent, QCloseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QMessageBox
import specfunctions
import sys
import os
import db

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MapsData:
    db.firstTime()
    spn = db.get_spn()
    coords = list(db.get_coords())
    display = db.get_display()
    pt = db.get_pt()
    postal_code = db.get_postal_code()
    address = db.get_address()
    z = db.get_zoom()


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.data = None
        self.map_type_choices = None
        self.e = None
        self.setupUI()

    def setupUI(self):
        uic.loadUi('data/MainWindow.ui', self)
        self.setupData()
        self.setWindowTitle('Yandex Maps Widget')
        self.setFixedSize(870, 504)
        self.setWindowIcon(QIcon('data/icon.png'))
        self.mapTypeGroup.buttonClicked.connect(self.chooseMapType)
        self.buttonSearch.clicked.connect(self.searchPlace)
        self.buttonClearResults.clicked.connect(self.resetSearchResult)
        self.checkboxIndex.stateChanged.connect(self.resetPostalCode)
        self.buttonLeftArrow.clicked.connect(self.leftArrowClicked)
        self.buttonRightArrow.clicked.connect(self.rightArrowClicked)
        self.buttonTopArrow.clicked.connect(self.topArrowClicked)
        self.buttonBottomArrow.clicked.connect(self.bottomArrowClicked)
        self.buttonPlus.clicked.connect(self.plusClicked)
        self.buttonMinus.clicked.connect(self.minusClicked)
        self.getPicture()

    def setupData(self):
        self.data = MapsData()
        self.map_type_choices = {
            'Схема': 'map',
            'Спутник': 'sat',
            'Гибрид': 'sat,skl',
        }
        if db.get_search_info() != '':
            self.fieldSearch.setPlainText(db.get_search_info())
        self.checkWhatRadioButton()
        if self.data.address != '':
            # print(self.fieldAdressShow)
            self.fieldAdressShow.setPlainText(self.data.address)
        if db.get_checkbox_index() == 1:
            self.checkboxIndex.setChecked(True)
            self.resetPostalCode()

    def checkWhatRadioButton(self):
        if self.data.display == 'map':
            self.radioButtonScheme.setChecked(True)
        elif self.data.display == 'sat':
            self.radioButtonSatellite.setChecked(True)
        elif self.data.display == 'sat,skl':
            self.radioButtonHybrid.setChecked(True)

    def getPicture(self):
        response = specfunctions.get_place_map(self.data)
        if response:
            self.setPicture(response)
        else:
            self.showMessage(
                'req_error',
                f'Ошибка запроса: {response.status_code}. '
                f'Причина: {response.reason}, {response.request.url}',
            )

    def setPicture(self, response):
        with open('data/image.png', 'wb') as file:
            file.write(response.content)
        pixmap = QPixmap('data/image.png')
        self.map.setPixmap(pixmap)

    def showMessage(self, action, text):
        if action == 'req_error':
            QMessageBox.critical(self, 'Ошибка запроса', text, QMessageBox.Ok)

    def leftArrowClicked(self):
        self.data.coords[0] -= self.data.spn
        if self.data.coords[0] < 1:
            self.data.coords[0] = min(self.data.spn, 1)
        else:
            self.getPicture()

    def rightArrowClicked(self):
        self.data.coords[0] += self.data.spn
        if self.data.coords[0] > 179:
            self.data.coords[0] = 179
        else:
            self.getPicture()

    def topArrowClicked(self):
        self.data.coords[1] += self.data.spn
        if self.data.coords[1] > 85:
            self.data.coords[1] = 85
        else:
            self.getPicture()

    def bottomArrowClicked(self):
        self.data.coords[1] -= self.data.spn
        if self.data.coords[1] < 1:
            self.data.coords[1] = min(self.data.spn, 1)
        else:
            self.getPicture()

    def plusClicked(self):
        if self.data.spn != 0.002:
            self.data.spn = max(self.data.spn / 2, 0.002)
            self.getPicture()

    def minusClicked(self):
        if self.data.spn != 89:
            self.data.spn = min(self.data.spn * 2, 89)
            self.getPicture()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key == Qt.Key.Key_PageUp:
            if self.data.spn != 89:
                self.data.spn = min(self.data.spn * 2, 89)
                self.getPicture()

        elif key == Qt.Key.Key_PageDown:
            if self.data.spn != 0.002:
                self.data.spn = max(self.data.spn / 2, 0.002)
                self.getPicture()

        elif key == Qt.Key.Key_W:
            self.data.coords[1] += self.data.spn
            if self.data.coords[1] > 85:
                self.data.coords[1] = 85
            else:
                self.getPicture()

        elif key == Qt.Key.Key_S:
            self.data.coords[1] -= self.data.spn
            if self.data.coords[1] < 1:
                self.data.coords[1] = min(self.data.spn, 1)
            else:
                self.getPicture()

        elif key == Qt.Key.Key_D:
            self.data.coords[0] += self.data.spn
            if self.data.coords[0] > 179:
                self.data.coords[0] = 179
            else:
                self.getPicture()

        elif key == Qt.Key.Key_A:
            self.data.coords[0] -= self.data.spn
            if self.data.coords[0] < 1:
                self.data.coords[0] = min(self.data.spn, 1)
            else:
                self.getPicture()

    def chooseMapType(self, button: QRadioButton):
        self.data.display = self.map_type_choices[button.text()]
        self.getPicture()

    def searchPlace(self, coords):
        place = self.fieldSearch.toPlainText().strip()
        try:
            if coords:
                toponym = specfunctions.get_place_toponym(None, coords)
            elif place:
                toponym = specfunctions.get_place_toponym(place)
            else:
                toponym = None

            if toponym:
                toponym = toponym.json()['response']['GeoObjectCollection'][
                    'featureMember'
                ][0]['GeoObject']
                if coords:
                    self.setPlace(toponym, coords)
                else:
                    self.setPlace(toponym)
            else:
                self.showMessage(
                    'req_error',
                    f'Ошибка запроса: {toponym.status_code}.'
                    f' Причина: {toponym.reason}',
                )
        except Exception as e:
            self.e = e
            self.showMessage(
                'req_error',
                f'Ошибка! Местоположение по запросу [{place}] не найдено.'
            )

    def setPlace(self, toponym, coords=''):
        toponym_address = toponym['metaDataProperty']['GeocoderMetaData'][
            'text'
        ]
        toponym_coords = toponym['Point']['pos']

        if not coords:
            self.data.coords = list(map(float, toponym_coords.split()))
            self.data.spn = 0.003
            self.data.pt = (
                    ','.join(list(map(str, toponym_coords.split()))) + ',pm2ntm'
            )
        else:
            self.data.pt = coords + ',pm2ntm'
        self.data.address = toponym_address

        self.getPicture()
        self.getPostalCode(toponym)
        self.resetPostalCode()

    def getPostalCode(self, toponym):
        try:
            self.data.postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except Exception as e:
            self.e = e
            self.data.postal_code = ''

    def resetSearchResult(self):
        self.data.pt = ''
        self.data.postal_code = ''
        self.data.address = ''
        self.fieldAdressShow.setPlainText('')
        self.getPicture()

    def resetPostalCode(self):
        if self.checkboxIndex.isChecked() and self.data.postal_code:
            self.fieldAdressShow.setPlainText(
                self.data.address + ' (' + self.data.postal_code + ')'
            )
        else:
            self.fieldAdressShow.setPlainText(self.data.address)

    def mouseToCoords(self, pos):
        import math
        print(self.data.coords)
        dx = pos[0] - self.map.pos().x() - (self.map.pos().x() + 629) / 2
        # dy = 400 - pos[1]
        lx = self.data.coords[0] + dx * self.data.spn
        # ly = self.data.coords[1] + dy * (self.data.spn) * math.cos(math.radians(self.data.coords[1])) * 2 ** (-5)
        ly = self.data.coords[1]
        print(lx, round(ly, 6))
        return round(lx, 6), round(ly, 6)

    coord_to_geo_x, coord_to_geo_y = 0.0000428, 0.0000428

    def screen_to_geo(pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = longitude + dx * coord_to_geo_x * 2
        ly = lattitude + dy * coord_to_geo_y * math.cos(math.radians(lattitude)) * 2

        return round(lx, 6), round(ly, 6)

    # def mouseToCoords(self, mouse_pos):
    #     x1, x2 = self.map.pos().x(), self.map.pos().x() + 619
    #     y1, y2 = self.map.pos().y(), self.map.pos().y() + 429
    #     print(self.data.spn)
    #
    #     if x1 <= mouse_pos[0] <= x2 and y1 <= mouse_pos[1] <= y2:
    #         spn_x = self.data.spn / 309.5 * (mouse_pos[0] - x1)
    #         spn_y = self.data.spn / 214.5 * (mouse_pos[1] - y1)
    #
    #         coord_1 = self.data.coords[0] - self.data.spn + spn_x
    #         coord_2 = self.data.coords[1] + self.data.spn - spn_y
    #
    #         return round(coord_1, 6), round(coord_2, 6)
    #     else:
    #         return False, False

    def searchPlaceClick(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            self.searchPlace(coords=f'{coord_1},{coord_2}')

    def searchOrganization(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            response = specfunctions.get_organization(f'{coord_1},{coord_2}')
            if response:
                response_json = response.json()
                try:
                    organization = response_json['features'][0]
                    org_name = organization['properties']['CompanyMetaData']['name']
                    org_address = organization['properties']['CompanyMetaData']['address']
                    coords = organization['geometry']['coordinates']

                    print(specfunctions.lonlat_distance(self.data.coords, coords))
                    if specfunctions.lonlat_distance(self.data.coords, coords) <= 50:
                        self.data.pt = ','.join(list(map(str, coords))) + ',pm2vvm'
                        print(self.data.pt)
                        self.data.postal_code = ''
                        self.data.address = org_name + '\n' + org_address
                        print(self.data.address)
                        self.getPicture()
                        self.resetPostalCode()
                except Exception as e:
                    self.e = e
                    return
            else:
                self.showMessage(
                    'req_error',
                    f'Ошибка запроса: {response.status_code}. '
                    f'Причина: {response.reason}, {response.request.url}',
                )

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.searchPlaceClick((event.x(), event.y()))
        else:
            self.searchOrganization((event.x(), event.y()))

    def closeEvent(self, event: QCloseEvent):
        db.write_data(self.data.spn, self.data.coords, self.data.display, self.data.pt, self.data.z,
                      self.data.postal_code, self.data.address, --self.checkboxIndex.isChecked(),
                      self.fieldSearch.toPlainText().strip())
        db.con.close()
        os.remove('data/image.png')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exceptHook = except_hook
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
