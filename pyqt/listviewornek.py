from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QListView

app = QApplication([])
model = QStringListModel(['Bir eleman', 'İkinci eleman', 'başka eleman'])
view = QListView()
view.setModel(model)
view.show()
app.exec_()