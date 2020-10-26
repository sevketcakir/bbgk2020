import sys

from PyQt5.QtWidgets import QDialog, QTextBrowser, QLineEdit, QVBoxLayout, QApplication, QWidget
from math import *

class Form(QDialog):
    def __init(self, parent=None): # hatalı kısım bulundu, init yanlış yazılmış
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit("Bir ifade yazıp Enter tuşuna basın")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()#Odağı lineedit nesnesine ver
        self.setWindowTitle("Hesapla")
        self.lineedit.returnPressed.connect(self.updateUI)

    def updateUI(self):
        try:
            text = self.lineedit.text()
            self.browser.append(f"{text} = {eval(text)}")
        except :
            self.browser.append(f"<font color=red>{text} geçersiz</font>")

#if __name__ == '__main__':
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()