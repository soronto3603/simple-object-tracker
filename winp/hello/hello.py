from PyQt5 import QtCore, QtGui, QtWidgets
from hello_ui import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    def __init__(self, w):
        Ui_MainWindow.__init__(self)
        self.setupUi(w)

        self.sayButton.clicked.connect(self.sayHello)
        self.closeButton.clicked.connect(self.exitWindow)

    def sayHello(self):
        self.helloEdit.setText('Hello world!')

    def exitWindow(self):
        app.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow(w)
    w.show()
    sys.exit(app.exec_())

