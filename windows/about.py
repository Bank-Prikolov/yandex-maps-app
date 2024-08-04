from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class AboutWindow(QMainWindow):
    # initialization
    def __init__(self):
        super().__init__()
        self.textWaizorSote = None
        self.textMikhalexandr = None
        self.setupUI()

    # interface setup
    def setupUI(self):
        uic.loadUi('assets/ui/AboutWindow.ui', self)
        self.setWindowTitle('About')
        self.setFixedSize(450, 188)
        self.setWindowIcon(QIcon('assets/images/icon.ico'))
        self.textMikhalexandr.setOpenExternalLinks(True)
        self.textWaizorSote.setOpenExternalLinks(True)
        self.show()
