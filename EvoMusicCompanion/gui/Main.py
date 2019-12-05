from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QHBoxLayout, QMainWindow

from ea.duration import Duration
from ea.individual import Individual, Measure, Note
from gui.MusicWindow import MusicWindow
from gui.Sidebar import Sidebar
from gui.models.MusicWindowViewModel import MusicWindowViewModel


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sidebar = Sidebar()

        population = [testIndividual, testIndividual]

        musicWindow = MusicWindow(MusicWindowViewModel(population, testIndividual, None))

        hbox = QHBoxLayout()
        hbox.addWidget(sidebar, 1)
        hbox.addWidget(musicWindow, 4)

        self.setLayout(hbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('EvoMusic')
        self.show()

    # def closeEvent(self, event):
    #
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure you want to quit?", QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


testIndividual = Individual(
    measures=[
        Measure(
            [
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5))
            ], 0, None),
        Measure(
            [
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5)),
                Note('C#5', Duration('half', 0.5))
            ], 0, None)
    ], fitness=0
)
