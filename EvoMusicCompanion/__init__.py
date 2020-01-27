import sys

from PyQt5.QtWidgets import QApplication

from ea.simulation import Simulation
from gui.Main import Main

if __name__ == '__main__':  
    sim = Simulation(0.5, 100, None, None)
    sim.run(30, None, None, None)
    #app = QApplication(sys.argv)
    #ex = Main()
    #sys.exit(app.exec_())
