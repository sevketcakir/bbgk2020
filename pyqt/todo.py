
#Model View Controller
from PyQt5 import uic, QtGui, Qt, QtWidgets
from PyQt5.QtCore import QAbstractListModel

qt_creator_file = "mainwindow.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
tick = QtGui.QImage('tick.png')

class TodoModel(QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.todos[index.row()]
            return text
        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)

class MainWindow(QtWidgets.QMainWindow, UI_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUI()
        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)
        self.addButton.clicked.connect(self.add)
        self.deleteButton.clicked.connect(self.delete)
        self.completeButton.clicked.connect(self.complete)