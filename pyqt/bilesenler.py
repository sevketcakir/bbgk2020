from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('bilesenler.ui', self)
        self.cinsiyet.addItems(['Kadın', 'Erkek'])
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    w = UI()
    app.exec_()