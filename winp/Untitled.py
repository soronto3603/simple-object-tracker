from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene,QButtonGroup
from PyQt5.QtGui import QPainter, QColor, QPen,QBrush
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
import sys
import points

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-100, -100, 200, 200)
        self.opt = ""
        self.pos1 = None
        self.pos2 = None
        self.count = 0
        self.PosArr = ()
    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        pen = QPen(QtCore.Qt.black)
        brush = QBrush(QtCore.Qt.black)
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.opt == "Generate":
            self.addEllipse(x, y, 4, 4, pen, brush)
        elif self.opt == "Select":
            print(x, y)


class SimpleWindow(QtWidgets.QMainWindow, points.Ui_Dialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)
        self.setupUi(self)

        self.scene = GraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        group = QButtonGroup(self)
        group.addButton(self.radioButton)
        group.addButton(self.radioButton_2)

        group.buttonClicked.connect(lambda btn: self.scene.setOption(btn.text()))
        self.radioButton.setChecked(True)
        self.scene.setOption(self.radioButton.text())

app = QtWidgets.QApplication(sys.argv)
form = SimpleWindow()
form.show()
app.exec_()
