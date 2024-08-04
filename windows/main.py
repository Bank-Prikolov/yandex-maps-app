from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent, QMouseEvent, QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QRadioButton, QMessageBox

from data import MapsData
from gateway import get_map, get_toponym, get_organization
from misc import degrees_to_pixels, ab_distance, translate, terminate
from .about import AboutWindow


class MainWindow(QMainWindow):
    # initialization
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.lang_choices = None
        self.langGroup = None
        self.radioButtonBe = None
        self.radioButtonEn = None
        self.radioButtonRu = None
        self.textLang = None
        self.textMapType = None
        self.textFullAddress = None
        self.map = None
        self.radioButtonSatellite = None
        self.radioButtonHybrid = None
        self.radioButtonScheme = None
        self.fieldAddressShow = None
        self.fieldSearch = None
        self.mapTypeGroup = None
        self.buttonSearch = None
        self.buttonClearResults = None
        self.checkboxIndex = None
        self.buttonLeftArrow = None
        self.buttonRightArrow = None
        self.buttonTopArrow = None
        self.buttonBottomArrow = None
        self.buttonPlus = None
        self.buttonMinus = None
        self.buttonInfo = None
        self.data = None
        self.map_type_choices = None
        self.e = None
        self.ex = None
        self.textForOrg = None
        self.setupUI()

    # interface setup
    def setupUI(self):
        uic.loadUi('assets/main/MainWindow.ui', self)
        self.setupData()
        self.setFixedSize(870, 504)
        self.setWindowIcon(QIcon('assets/general/icon.ico'))
        self.mapTypeGroup.buttonClicked.connect(self.chooseMapType)
        self.langGroup.buttonClicked.connect(self.chooseLang)
        self.buttonSearch.clicked.connect(self.searchPlace)
        self.buttonClearResults.clicked.connect(self.clearSearchResult)
        self.checkboxIndex.stateChanged.connect(self.remakePostalCode)
        self.buttonLeftArrow.clicked.connect(self.leftArrowClicked)
        self.buttonRightArrow.clicked.connect(self.rightArrowClicked)
        self.buttonTopArrow.clicked.connect(self.topArrowClicked)
        self.buttonBottomArrow.clicked.connect(self.bottomArrowClicked)
        self.buttonPlus.clicked.connect(self.plusClicked)
        self.buttonMinus.clicked.connect(self.minusClicked)
        self.buttonInfo.clicked.connect(self.infoClicked)
        if self.data.lang != 'ru':
            self.retranslateUI()
        self.getMapPicture()

    # receiving and processing data
    def setupData(self):
        self.data = MapsData()
        self.map_type_choices = {
            'radioButtonScheme': 'map',
            'radioButtonSatellite': 'sat',
            'radioButtonHybrid': 'sat,skl',
        }
        self.lang_choices = {
            'radioButtonRu': 'ru',
            'radioButtonBe': 'be',
            'radioButtonEn': 'en',
        }
        if self.data.search_info != '':
            self.fieldSearch.setPlainText(self.data.search_info)
        self.checkForRadioButtons()
        if self.data.address != '':
            self.fieldAddressShow.setPlainText(self.data.address)
        if self.data.checkbox_index == 1:
            self.checkboxIndex.setChecked(True)
            self.remakePostalCode()

    # getting a map
    def getMapPicture(self):
        response = get_map(self.data)
        if response:
            self.setMapPicture(response)
        else:
            print(response.request.url)
            self.showErrorMessage(
                'req_error',
                f'Ошибка запроса: {response.status_code}\n'
                f'Причина: {response.reason}',
            )

    # check map type and language
    def checkForRadioButtons(self):
        if self.data.display == 'map':
            self.radioButtonScheme.setChecked(True)
        elif self.data.display == 'sat':
            self.radioButtonSatellite.setChecked(True)
        elif self.data.display == 'sat,skl':
            self.radioButtonHybrid.setChecked(True)

        if self.data.lang == 'ru':
            self.radioButtonRu.setChecked(True)
        elif self.data.lang == 'be':
            self.radioButtonBe.setChecked(True)
        elif self.data.lang == 'en':
            self.radioButtonEn.setChecked(True)

    # installing a map
    def setMapPicture(self, response):
        with open('assets/general/map.png', 'wb') as file:
            file.write(response.content)
        pixmap = QPixmap('assets/general/map.png')
        self.map.setPixmap(pixmap)

    # button presses handling
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
            self.data.z += 1
            self.data.spn = self.data.spn / 2
        self.getMapPicture()

    def minusClicked(self):
        if self.data.z > 3:
            self.data.z -= 1
            self.data.spn = self.data.spn * 2
        self.getMapPicture()

    # keystroke handling
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key == Qt.Key.Key_PageUp:
            if self.data.z < 21:
                self.data.z += 1
                self.data.spn = self.data.spn / 2
            self.getMapPicture()

        elif key == Qt.Key.Key_PageDown:
            if self.data.z > 3:
                self.data.z -= 1
                self.data.spn = self.data.spn * 2
            self.getMapPicture()

        elif key == Qt.Key.Key_W:
            self.data.coords[1] += self.data.spn
            if self.data.coords[1] > 79.34568:
                self.data.coords[1] = 79.34568
            else:
                self.getMapPicture()

        elif key == Qt.Key.Key_S:
            self.data.coords[1] -= self.data.spn
            if self.data.coords[1] < -68.11032:
                self.data.coords[1] = -68.11032
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

    # select map type
    def chooseMapType(self, button: QRadioButton):
        self.data.display = self.map_type_choices[button.objectName()]
        self.getMapPicture()

    # select language
    def chooseLang(self, button: QRadioButton):
        self.data.lang = self.lang_choices[button.objectName()]
        self.retranslateUI()
        self.getMapPicture()

    # click on the map
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.searchPlaceClick((event.x(), event.y()))
        else:
            self.searchOrganization((event.x(), event.y()))

    # convert window coordinates to map coordinates
    def mouseToCoords(self, mouse_pos):
        x1, x2 = self.map.pos().x(), self.map.pos().x() + 619
        y1, y2 = self.map.pos().y(), self.map.pos().y() + 429
        if x1 <= mouse_pos[0] <= x2 and y1 <= mouse_pos[1] <= y2:
            coordX, coordY = degrees_to_pixels(self.data.coords[1], self.data.z)
            return (self.data.coords[0] + coordX * (mouse_pos[0]) - (coordX * (x1 + x2 / 2 - 2)),
                    self.data.coords[1] - coordY * (mouse_pos[1] - y1) + (coordY * (y1 + y2 / 3 - 5)))
        else:
            return False, False

    # click search
    def searchPlaceClick(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            self.searchPlace(coords=f'{coord_1},{coord_2}')

    # search for a place
    def searchPlace(self, coords):
        place = self.fieldSearch.toPlainText().strip()
        try:
            if coords:
                toponym = get_toponym(self.data.lang, None, coords)
            elif place:
                toponym = get_toponym(self.data.lang, place)
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

    # setting location
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

    # getting zip code
    def getPostalCode(self, toponym):
        try:
            self.data.postal_code = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except Exception as e:
            self.e = e
            self.data.postal_code = ''

    # reset location on last request/click
    def clearSearchResult(self):
        self.data.pt = ''
        self.data.postal_code = ''
        self.data.address = ''
        self.fieldAddressShow.setPlainText('')
        self.getMapPicture()

    # show info
    def infoClicked(self):
        self.ex = AboutWindow(self.data.lang)
        self.ex.show()

    # reset zip code
    def remakePostalCode(self):
        if self.checkboxIndex.isChecked() and self.data.postal_code:
            self.fieldAddressShow.setPlainText(self.data.address + ' (' + self.data.postal_code + ')')
        else:
            self.fieldAddressShow.setPlainText(self.data.address)

    # search for organization
    def searchOrganization(self, mouse_pos):
        coord_1, coord_2 = self.mouseToCoords(mouse_pos)
        if coord_1:
            toponym = get_toponym(self.data.lang, None, f'{coord_1},{coord_2}')
            self.textForOrg = \
                toponym.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                    'GeocoderMetaData']['text']
            response = get_organization(f'{coord_1},{coord_2}', self.textForOrg, self.data.lang)
            if response:
                response_json = response.json()
                try:
                    organization = response_json['features'][0]
                    org_name = organization['properties']['CompanyMetaData']['name']
                    org_address = organization['properties']['CompanyMetaData']['address']
                    coords = organization['geometry']['coordinates']
                    if ab_distance(self.data.coords, coords) <= 1000:
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

    # change app language
    def retranslateUI(self):
        _ = translate(self.data.lang, 'main')
        self.setWindowTitle(_('Яндекс Карты'))
        self.buttonSearch.setText(_('ПОИСК'))
        self.textFullAddress.setText(_('Полный адрес'))
        self.checkboxIndex.setText(_('Почтовый индекс'))
        self.textMapType.setText(_('Вид карты:'))
        self.radioButtonScheme.setText(_('Схема'))
        self.radioButtonSatellite.setText(_('Спутник'))
        self.radioButtonHybrid.setText(_('Гибрид'))
        self.textLang.setText(_('Язык:'))
        self.radioButtonRu.setText(_('Рус'))
        self.radioButtonEn.setText(_('Англ'))
        self.radioButtonBe.setText(_('Бел'))
        self.buttonClearResults.setText(_('Сброс результата'))

    # display errors
    def showErrorMessage(self, action, text):
        if action == 'req_error':
            QMessageBox.critical(self, 'Ошибка запроса', text, QMessageBox.Ok)

    # closing the window
    def closeEvent(self, event: QCloseEvent):
        self.data.post_data(
            self.data.lang, self.data.spn, self.data.coords, self.data.display, self.data.pt, self.data.z,
            self.data.postal_code, self.data.address, --self.checkboxIndex.isChecked(),
            self.fieldSearch.toPlainText().strip()
        )
        terminate()