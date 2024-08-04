from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from misc import translate


class AboutWindow(QMainWindow):
    # initialization
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.textYLNote = None
        self.textDevelopers = None
        self.textMikhalexandr = None
        self.textWaizorSote = None
        self.setupUI()

    # interface setup
    def setupUI(self):
        uic.loadUi('assets/about/AboutWindow.ui', self)
        self.setFixedSize(450, 188)
        self.setWindowIcon(QIcon('assets/general/icon.ico'))
        self.textMikhalexandr.setOpenExternalLinks(True)
        self.textWaizorSote.setOpenExternalLinks(True)
        self.retranslateUI()

    # changing app language
    def retranslateUI(self):
        _ = translate(self.lang, 'about')
        self.setWindowTitle(_('О нас'))
        self.textYLNote.setText(_('Приложение разработано в учебных целях'))
        self.textDevelopers.setText(_('Разработчики:'))
