import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui
from model.BeautyWindow import BeautyWindow
import os
import glob


class Controller:
    fileList = []

    def __init__(self):
        self.app = QApplication(sys.argv)
        app_icon = QtGui.QIcon()
        app_icon.addFile('assets/main-icon.png', QtCore.QSize(24, 24))
        self.app.setWindowIcon(app_icon)
        self.currentImageIndex = 0
        self.window = BeautyWindow(None)
        self.connectButtons()

    def connectButtons(self):
        self.window.ui.rotateCWButton.clicked.connect(lambda: self.window.ui.imageWidget.rotate(90))
        self.window.ui.rotateAntiCWButton.clicked.connect(lambda: self.window.ui.imageWidget.rotate(-90))
        self.window.ui.loadPreviousButton.clicked.connect(self.previousPhoto)
        self.window.ui.loadNextButton.clicked.connect(self.nextPhoto)
        self.window.ui.loadButton.clicked.connect(lambda: self.loadFiles(self.window.ui.folderPathInput.text()))
        self.window.ui.loadPreviousButton.setShortcut(QtCore.Qt.Key_Left)
        self.window.ui.loadNextButton.setShortcut(QtCore.Qt.Key_Right)
        self.window.ui.folderPathInput.returnPressed.connect(lambda: self.loadFiles(self.window.ui.folderPathInput.text()))

    def previousPhoto(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.window.ui.imageWidget.loadImage(self.fileList[self.currentImageIndex])
            self.loadExif()

    def nextPhoto(self):
        if self.currentImageIndex < len(self.fileList) - 1:
            self.currentImageIndex += 1
            self.window.ui.imageWidget.loadImage(self.fileList[self.currentImageIndex])
            self.loadExif()

    def loadFiles(self, folderPath):
        try:
            os.chdir(folderPath)
        except OSError:
            self.window.ui.folderNotFound.setText("Can not locate folder")
            self.window.ui.folderNotFound.setStyleSheet("color:red;")
        else:
            self.fileList = []
            types = ( '*.jpeg', '*.jpg', '*.JPEG', '*.JPG', '*.png')
            for files in types:
                self.fileList.extend(glob.glob(files))
            for i in range(0, len(self.fileList)):
                self.fileList[i] = folderPath + "/" + self.fileList[i]
            self.window.ui.folderNotFound.setText("")
            self.window.ui.imageWidget.loadImage(self.fileList[0])
            self.currentImageIndex = 0
            self.loadExif()
            self.init512()

    def loadExif(self):
        exifData = self.window.ui.imageWidget.image.convertExif()
        table = self.window.ui.tableWidget
        table.clear()
        table.setRowCount(0)
        if len(exifData) > 0:
            for data in exifData:
                if data != 'GPSInfo':
                    table.insertRow(table.rowCount())
                    table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(data))
                    table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(exifData[data])))
                elif len(exifData[data]) > 1:
                    self.loadGPS(table, exifData)
        else:
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem('No Exif Data'))
            table.setItem(table.rowCount()-1, 1, QTableWidgetItem(':('))

    @staticmethod
    def loadGPS(table, exifData):
        gpsLabel = QLabel()
        gpsLabel.setText('<a href="' + exifData['GPSInfo'] + '">Click to see Location</a>')
        gpsLabel.setOpenExternalLinks(True)
        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem('GPS Info'))
        table.setCellWidget(table.rowCount() - 1, 1, gpsLabel)

    #only way to init the size of the picture to 512px
    def init512(self):
        if self.window.ui.imageWidget.image.isPortrait():
            reductionRate = 100
            while self.window.ui.imageWidget.image.width() != 512:
                if self.window.ui.imageWidget.image.width() > 512:
                    if self.window.ui.imageWidget.image.width() - reductionRate < 512:
                        reductionRate = reductionRate / 2
                    else:
                        self.window.resize(self.window.width() - reductionRate, self.window.height())
                else:
                    self.window.resize(self.window.width() + 200, self.window.height())
        else:
            reductionRate = 100
            while self.window.ui.imageWidget.image.height() != 512:
                if self.window.ui.imageWidget.image.height() > 512:
                    if self.window.ui.imageWidget.image.height() - reductionRate < 512:
                        reductionRate = reductionRate / 2
                    else:
                        self.window.resize(self.window.width(), self.window.height() - reductionRate)
                else:
                    self.window.resize(self.window.width(), self.window.height() + 200)
        print("Image size:", self.window.ui.imageWidget.image.imageWidth, self.window.ui.imageWidget.image.imageHeight)

    def run(self):
        self.window.show()
        return self.app.exec_()


controller = Controller()

