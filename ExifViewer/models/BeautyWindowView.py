from PyQt5.QtWidgets import QMainWindow
from ExifViewer.design.design import Ui_MainWindow
from PyQt5 import QtWidgets


class BeautyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def init(self, imagePath, isPortrait):
        self.imageWidget.loadImage(imagePath)
        self.init512(isPortrait)

    def loadImage(self, imagePath):
        self.imageWidget.loadImage(imagePath)

    def rotateImage(self, angle):
        self.imageWidget.rotate(angle)

    # only way to init the size of the picture to 512px
    def init512(self, isPortrait):
        if isPortrait:
            reductionRate = 100
            while self.imageWidget.image.width() != 512:
                if self.imageWidget.image.width() > 512:
                    if self.imageWidget.image.width() - reductionRate < 512:
                        reductionRate = reductionRate / 2
                    else:
                        self.resize(self.width() - reductionRate, self.height())
                else:
                    self.resize(self.ui.width() + 200, self.height())
        else:
            reductionRate = 100
            while self.imageWidget.image.height() != 512:
                if self.imageWidget.image.height() > 512:
                    if self.imageWidget.image.height() - reductionRate < 512:
                        reductionRate = reductionRate / 2
                    else:
                        self.resize(self.width(), self.height() - reductionRate)
                else:
                    self.resize(self.width(), self.height() + 200)
        print("Image size:", self.imageWidget.image.imageWidth, self.imageWidget.image.imageHeight)
