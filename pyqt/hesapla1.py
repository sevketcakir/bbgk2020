from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('hesapla.ui', self)
        self.dugme.clicked.connect(self.updateUI)
        self.girdi.returnPressed.connect(self.updateUI)
        self.show()

    def updateUI(self):
        try:
            text = self.girdi.text()
            self.liste.addItem(f"{text} = <b>{eval(text)}</b>")
        except :
            self.liste.addItem(f"<font color=red>{text} geçersiz</font>")


if __name__ == '__main__':
    app = QApplication([])
    pencere = UI()
    app.exec_()
