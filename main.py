import os
import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent, QMouseEvent, QCloseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QMessageBox

import db
import specfunctions

# на случай нестандартного разрешения экрана
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# получение информации о карте из БД
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
    # инициализация
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.data = None
        self.map_type_choices = None
        self.e = None
        self.textForOrg = None
        self.setupUI()

    # настройка интерфейса
    def setupUI(self):
        uic.loadUi('data/MainWindow.ui', self)
        self.setupData()
        self.setWindowTitle('Yandex Maps Widget')
        self.setFixedSize(870, 504)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.mapTypeGroup.buttonClicked.connect(self.chooseMapType)
        self.buttonSearch.clicked.connect(self.searchPlace)
        self.buttonClearResults.clicked.connect(self.clearSearchResult)
        self.checkboxIndex.stateChanged.connect(self.remakePostalCode)
        self.buttonLeftArrow.clicked.connect(self.leftArrowClicked)
        self.buttonRightArrow.clicked.connect(self.rightArrowClicked)
        self.buttonTopArrow.clicked.connect(self.topArrowClicked)
        self.buttonBottomArrow.clicked.connect(self.bottomArrowClicked)
        self.buttonPlus.clicked.connect(self.plusClicked)
        self.buttonMinus.clicked.connect(self.minusClicked)
        self.getMapPicture()

    # получение и обработка данных
    def setupData(self):
        self.data = MapsData()
        self.map_type_choices = {
            'Схема': 'map',
            'Спутник': 'sat',
            'Гибрид': 'sat,skl',
        }
        if db.get_search_info() != '':
            self.fieldSearch.setPlainText(db.get_search_info())
        self.checkWhatMapType()
        if self.data.address != '':
            self.fieldAdressShow.setPlainText(self.data.address)
        if db.get_checkbox_index() == 1:
            self.checkboxIndex.setChecked(True)
            self.remakePostalCode()

    # получение карты
    def getMapPicture(self):
        response = specfunctions.get_map(self.data)
        if response:
            self.setMapPicture(response)
        else:
            print(response.request.url)
            self.showErrorMessage(
                'req_error',
                f'Ошибка запроса: {response.status_code}\n'
                f'Причина: {response.reason}',
            )

    # проверка типа карты
    def checkWhatMapType(self):
        if self.data.display == 'map':
            self.radioButtonScheme.setChecked(True)
        elif self.data.display == 'sat':
            self.radioButtonSatellite.setChecked(True)
        elif self.data.display == 'sat,skl':
            self.radioButtonHybrid.setChecked(True)

    # установка карты
    def setMapPicture(self, response):
        with open('data/map-image.png', 'wb') as file:
            file.write(response.content)
        pixmap = QPixmap('data/map-image.png')
        self.map.setPixmap(pixmap)

    # обработка нажатия кнопок
    def leftArrowClicked(self):
        self.data.coords[0] -= self.data.spn
        if self.data.coords[0] < -180:
            self.data.coords[0] = 180
        self.getMapPicture()

    def rightArrowClicked(self):
        self.data.coords[0] += self.data.spn
        if self.data.coords[0] > 180:
            self.data.coords[0] = -180
        self.getMapPicture()

    def topArrowClicked(self):
        self.data.coords[1] += self.data.spn
        if self.data.coords[1] > 79.34568:
            self.data.coords[1] = 79.34568
        else:
            self.getMapPicture()

    def bottomArrowClicked(self):
        self.data.coords[1] -= self.data.spn
        if self.data.coords[1] < -68.11032:
            self.data.coords[1] = -68.11032
        else:
            self.getMapPicture()

    def plusClicked(self):
        if self.data.z < 21:
            self.data.spn = self.data.spn / 2
            self.data.z += 1
        self.getMapPicture()

    def minusClicked(self):
        if self.data.z > 3:
            self.data.z -= 1
            self.data.spn = self.data.spn * 2
        self.getMapPicture()

    # обработка нажатия клавиш
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key == Qt.Key.Key_PageUp:
            if self.data.z < 21:
                if self.data.spn != 0.002:
                    self.data.spn = max(self.data.spn / 2, 0.002)
                self.data.z += 1
            self.getMapPicture()

        elif key == Qt.Key.Key_PageDown:
            if self.data.z > 3:
                self.data.z -= 1
                if self.data.spn != 89:
                    self.data.spn = min(self.data.spn * 2, 89)
            self.getMapPicture()

        elif key == Qt.Key.Key_W:
            self.data.coords[1] += self.data.spn
            if self.data.coords[1] > 85:
                self.data.coords[1] = 85
            else:
                self.getMapPicture()

        elif key == Qt.Key.Key_S:
            self.data.coords[1] -= self.data.spn
            if self.data.coords[1] < -85:
                self.data.coords[1] = -85
            else:
                self.getMapPicture()

        elif key == Qt.Key.Key_D:
            self.data.coords[0] += self.data.spn
            if self.data.coords[0] > 180:
                self.data.coords[0] = -180
            self.getMapPicture()

        elif key == Qt.Key.Key_A:
            self.data.coords[0] -= self.data.spn
            if self.data.coords[0] < -180:
                self.data.coords[0] = 180
            self.getMapPicture()

    # выбор типа карты
    def chooseMapType(self, button: QRadioButton):
        self.data.display = self.map_type_choices[button.text()]
        self.getMapPicture()

    # клик по карте
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.searchPlaceClick((event.x(), event.y()))
        else:
            self.searchOrganization((event.x(), event.y()))

    # перевод координат окна в координаты карты
    def mouseToCoords(self, mouse_pos):
        x1, x2 = self.map.pos().x(), self.map.pos().x() + 619
        y1, y2 = self.map.pos().y(), self.map.pos().y() + 429
        if x1 <= mouse_pos[0] <= x2 and y1 <= mouse_pos[1] <= y2:
            coordX, coordY = specfunctions.degrees_to_pixels(self.data.coords[1], self.data.z)
            return (self.data.coords[0] + coordX * (mouse_pos[0]) - (coordX * (x1 + x2 / 2 - 2)),
                    self.data.coords[1] - coordY * (mouse_pos[1] - y1) + (coordY * (y1 + y2 / 3 - 5)))
        else:
            return False, False

    # поиск по клику
    def searchPlaceClick(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            self.searchPlace(coords=f'{coord_1},{coord_2}')

    # поиск места
    def searchPlace(self, coords):
        place = self.fieldSearch.toPlainText().strip()
        try:
            if coords:
                toponym = specfunctions.get_toponym(None, coords)
            elif place:
                toponym = specfunctions.get_toponym(place)
            else:
                toponym = None

            if toponym:
                toponym = toponym.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                if coords:
                    self.setPlace(toponym, coords)
                else:
                    self.setPlace(toponym)
            else:
                self.showErrorMessage(
                    'req_error',
                    f'Ошибка запроса: {toponym.status_code}\n'
                    f'Причина: {toponym.reason}',
                )
        except Exception as e:
            self.e = e
            self.showErrorMessage(
                'req_error',
                f'Ошибка запроса! Местоположение по запросу "{place}" не найдено.'
            )

    # установка местоположения
    def setPlace(self, toponym, coords=''):
        toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
        toponym_coords = toponym['Point']['pos']

        if not coords:
            self.data.coords = list(map(float, toponym_coords.split()))
            self.data.pt = (','.join(list(map(str, toponym_coords.split()))) + ',pm2ntm')
        else:
            self.data.pt = coords + ',pm2ntm'
        self.data.address = toponym_address

        self.getMapPicture()
        self.getPostalCode(toponym)
        self.remakePostalCode()

    # получение почтового индекса
    def getPostalCode(self, toponym):
        try:
            self.data.postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except Exception as e:
            self.e = e
            self.data.postal_code = ''

    # сброс местоположения по последнему запросу/клику
    def clearSearchResult(self):
        self.data.pt = ''
        self.data.postal_code = ''
        self.data.address = ''
        self.fieldAdressShow.setPlainText('')
        self.getMapPicture()

    # сброс почтового индекса
    def remakePostalCode(self):
        if self.checkboxIndex.isChecked() and self.data.postal_code:
            self.fieldAdressShow.setPlainText(self.data.address + ' (' + self.data.postal_code + ')')
        else:
            self.fieldAdressShow.setPlainText(self.data.address)

    # поиск организации
    def searchOrganization(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            toponym = specfunctions.get_toponym(None, f'{coord_1},{coord_2}')
            self.textForOrg = \
                toponym.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                    'GeocoderMetaData']['text']
            response = specfunctions.get_organization(f'{coord_1},{coord_2}', self.textForOrg)
            if response:
                response_json = response.json()
                try:
                    organization = response_json['features'][0]
                    org_name = organization['properties']['CompanyMetaData']['name']
                    org_address = organization['properties']['CompanyMetaData']['address']
                    coords = organization['geometry']['coordinates']
                    if specfunctions.ab_distance(self.data.coords, coords) <= 50:
                        self.data.pt = ','.join(list(map(str, coords))) + ',pm2vvm'
                        self.data.postal_code = ''
                        self.data.address = org_name + '\n' + org_address
                        self.getMapPicture()
                        self.remakePostalCode()
                except Exception as e:
                    self.e = e
                    return
            else:
                print(response.request.url)
                self.showErrorMessage(
                    'req_error',
                    f'Ошибка запроса: {response.status_code}\n'
                    f'Причина: {response.reason}',
                )

    # отображение ошибок
    def showErrorMessage(self, action, text):
        if action == 'req_error':
            QMessageBox.critical(self, 'Ошибка запроса', text, QMessageBox.Ok)

    # закрытие окна
    def closeEvent(self, event: QCloseEvent):
        db.write_data(self.data.spn, self.data.coords, self.data.display, self.data.pt, self.data.z,
                      self.data.postal_code, self.data.address, --self.checkboxIndex.isChecked(),
                      self.fieldSearch.toPlainText().strip())
        db.con.close()
        os.remove('data/map-image.png')


# ошибки PyQT
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exceptHook = except_hook
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
