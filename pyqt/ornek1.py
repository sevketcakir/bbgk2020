# QT PyQT
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400, 400, 500, 300)
    win.setWindowTitle("Örnek 1")
    win.show()
    sys.exit(app.exec_())

window()
