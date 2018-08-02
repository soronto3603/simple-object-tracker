from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QIcon, QPixmap,QPainter, QColor, QPen,QBrush
from mainwindow import Ui_MainWindow
import cv2
import numpy as np
import os

class GraphicsScene(QGraphicsScene):
    def __init__(self,parent = None):
        QGraphicsScene.__init__(self,parent)
        self.pos1 = None
        self.pos2 = None
        self.count = 0
        self.PosArr = ()
    def mousePressEvent(self,event):
        pen = QPen(QtCore.Qt.black)
        brush = QBrush(QtCore.Qt.black)
        x = event.scenePos().x()
        y = event.scenePos().y()
        if(self.count%2 ==0):
            self.pos1 = event.pos()
            self.count = self.count+1
        else:
            self.pos2 = event.pos()
            self.count = self.count + 1
            self.PosArr += (self.pos1,self.pos2)
        print(self.count)
        print(self.PosArr)
        for i in self.PosArr:
            print(i)
        self.addEllipse(x, y, 4, 4, pen, brush)    

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.FindButton.clicked.connect(self.get_file)
        self.CloseButton.clicked.connect(self.exitWindow)
        self.scene = GraphicsScene(self)
        self.graphicsView.setScene(self.scene)
    def exitWindow(self):
        app.quit()

    def get_file(self):
        filename = QFileDialog.getOpenFileName()
        self.PathText.setText(filename[0])
        cap = cv2.VideoCapture(filename[0])
        ret,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],frame.strides[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.scene.addPixmap(pix.scaled(self.graphicsView.width(),self.graphicsView.height(), QtCore.Qt.KeepAspectRatio))
        self.graphicsView.setScene(self.scene)
        self.graphicsView.resize(self.scene.width(),self.scene.height())
        self.graphicsView.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
