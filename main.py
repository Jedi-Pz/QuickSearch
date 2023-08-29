import sys

from PyQt5.QtWidgets import QApplication
from HandmadeEverything import HandmadeEverything

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HandmadeEverything()
    window.show()
    sys.exit(app.exec_())
