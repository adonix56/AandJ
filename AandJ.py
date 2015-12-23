import sys
from PyQt4 import QtGui
import MainWindow

def AandJ():
    app = QtGui.QApplication(sys.argv)
    GUI = MainWindow.AandJ()
    sys.exit(app.exec_())

AandJ()
