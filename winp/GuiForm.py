from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QIcon, QPixmap
from mainwindow import Ui_MainWindow
import cv2
import numpy as np
import os

class MainWindow(Ui_MainWindow):
    def __init__(self,w):
        Ui_MainWindow.__init__(self)
        self.setupUi(w)

        self.FindButton.clicked.connect(self.get_file)
        self.CloseButton.clicked.connect(self.exitWindow)

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
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pix.scaled(self.graphicsView.width(),self.graphicsView.height(), QtCore.Qt.KeepAspectRatio))
        self.graphicsView.setScene(scene)
        self.graphicsView.resize(scene.width(),scene.height())
        self.graphicsView.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow(w)
    w.show()
    sys.exit(app.exec())
