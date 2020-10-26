import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout


class PyQtLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        button1 = QPushButton("PyQt", self)
        button1.move(10,20)

        button2 = QPushButton("Layout", self)
        button2.move(40,50)

        button3 = QPushButton("Management", self)
        button3.move(60, 90)

        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("PyQt5 Layout Management")
        self.show()


class PyQtLayout2(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        button1 = QPushButton('PyQt')
        button2 = QPushButton('Layout')
        button3 = QPushButton('Management')

        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("PyQt5 Layout Management")
        self.show()

class PyQtLayout3(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        button1 = QPushButton('PyQt')
        button2 = QPushButton('Layout')
        button3 = QPushButton('Management')

        vbox = QHBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("PyQt5 Layout Management")
        self.show()


class PyQtLayout4(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        button1 = QPushButton('Up')
        button2 = QPushButton('Left')
        button3 = QPushButton('Right')
        button4 = QPushButton('Down')

        vbox = QGridLayout()
        vbox.addWidget(button1, 0, 0, 1, 3)
        vbox.addWidget(button2, 1, 0)
        vbox.addWidget(button3, 1, 2)
        vbox.addWidget(button4, 1, 1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("PyQt5 Layout Management")
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = PyQtLayout()
    ex2 = PyQtLayout2()
    ex3 = PyQtLayout3()
    ex4 = PyQtLayout4()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

