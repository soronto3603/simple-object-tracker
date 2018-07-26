from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    def __init__(self,w):
        Ui_MainWindow.__init__(self)
        self.setupUi(w)

        self.FindButton.clicked.connect(self.get_file_name)
        self.CloseButton.clicked.connect(self.exitWindow)

    def exitWindow(self):
        app.quit()

    def get_file_name(self):
        filename = QFileDialog.getOpenFileName()
        self.PathText.setText(filename[0])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow(w)
    w.show()
    sys.exit(app.exec())
