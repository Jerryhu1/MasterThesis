import sys

from PyQt5.QtWidgets import QApplication, QToolBar, QStatusBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EvoMusic")
        self.setCentralWidget(QLabel("Central widget"))
        self._createMenu()
        self._createSidebar()
        self._createLowerbar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu('&Menu')
        self.menu.addAction('&Exit', self.close)

    def _createSidebar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createLowerbar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
