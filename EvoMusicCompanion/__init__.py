import sys

from PyQt5.QtWidgets import QApplication

from gui.Main import Main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
