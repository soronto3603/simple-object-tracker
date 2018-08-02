from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QPainter, QColor, QPen,QBrush
from PyQt5.QtWidgets import ( QGraphicsView, QGraphicsScene, QFileDialog)
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
        self.Postmp = ()

    def DrawLine(self):
        pen = QPen(QtCore.Qt.red)
        for pos1 in self.Postmp:
            for pos2 in self.Postmp:
                if(pos1 == pos2):
                    continue
                self.addLine(pos1[0],pos1[1],pos2[0],pos2[1],pen)
                self.Postmp = ()

    def mousePressEvent(self,event):
        pen = QPen(QtCore.Qt.black)
        brush = QBrush(QtCore.Qt.black)
        x = event.scenePos().x()
        y = event.scenePos().y()
        print('Coordinates: ( %d : %d )' % (x,y))
        self.addEllipse(x, y, 2, 2, pen, brush)

        if(self.count%2 ==0):
            self.pos1 = (x,y)
            self.count = self.count + 1
        else:
            self.pos2 = (x,y)
            self.count = self.count + 1
            self.PosArr += (self.pos1,self.pos2)
            self.Postmp += (self.pos1,self.pos2)

        if(len(self.PosArr)%2 ==0 and self.count%2==0):
            self.DrawLine()




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
        self.scene.clear()
        self.graphicsView.setTransform(QtGui.QTransform())
        filename = QFileDialog.getOpenFileName()
        self.PathText.setText(filename[0])
        cap = cv2.VideoCapture(filename[0])
        ret,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],frame.strides[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        print("before graphicsview size w: %d h: %d" %(self.graphicsView.width(),self.graphicsView.height()))
        self.scene.addPixmap(pix.scaled(self.graphicsView.width(),self.graphicsView.height(), QtCore.Qt.KeepAspectRatio))
        self.graphicsView.resize(self.scene.width(),self.scene.height())
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
        print("graphicsview size w: %d h: %d" %(self.graphicsView.width(),self.graphicsView.height()))
        print("graphicsScene size w: %d h: %d" %(self.scene.width(),self.scene.height()))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
