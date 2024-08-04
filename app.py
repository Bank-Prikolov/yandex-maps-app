import sys
from PyQt5.QtWidgets import QApplication

from misc import except_hook, check_screeninfo
from windows import MainWindow


if __name__ == '__main__':
    check_screeninfo()
    app = QApplication(sys.argv)
    sys.exceptHook = except_hook
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
