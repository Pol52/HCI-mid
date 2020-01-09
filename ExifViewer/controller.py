import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui
from ExifViewer.models.BeautyWindowView import BeautyWindow
from ExifViewer.models.ImageModel import ImageModel
import os
import glob


class Controller:
    fileList = []

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('assets/main-icon.png', QtCore.QSize(24, 24))
        self.app.setWindowIcon(self.app_icon)
        self.currentImageIndex = 0
        self.ui = BeautyWindow()
        self.model = ImageModel()
        self.connectButtons()

    def init(self):
        self.ui.loadSignal.connect(self.loadFiles)

    def connectButtons(self):
        self.ui.rotateCWButton.clicked.connect(lambda: self.rotateImage(90))
        self.ui.rotateAntiCWButton.clicked.connect(lambda: self.rotateImage(-90))
        self.ui.loadPreviousButton.clicked.connect(self.previousPhoto)
        self.ui.loadNextButton.clicked.connect(self.nextPhoto)
        self.ui.loadButton.clicked.connect(self.loadFiles)
        self.ui.loadPreviousButton.setShortcut(QtCore.Qt.Key_Left)
        self.ui.loadNextButton.setShortcut(QtCore.Qt.Key_Right)
        self.ui.folderPathInput.returnPressed.connect(self.loadFiles)

    def rotateImage(self, angle):
        if self.model.imageUrl != '':
            self.ui.rotateImage(angle)

    def previousPhoto(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.model.loadImage(self.fileList[self.currentImageIndex])
            self.ui.loadImage(self.model.imageUrl)
            self.loadExif()

    def nextPhoto(self):
        if self.currentImageIndex < len(self.fileList) - 1:
            self.currentImageIndex += 1
            self.model.loadImage(self.fileList[self.currentImageIndex])
            self.ui.loadImage(self.model.imageUrl)
            self.loadExif()

    def loadFiles(self):
        folderPath = self.ui.folderPathInput.text()
        try:
            os.chdir(folderPath)
        except OSError:
            self.ui.folderNotFound.setText("Can not locate folder")
            self.ui.folderNotFound.setStyleSheet("color:red;")
        else:
            self.fileList = []
            types = ('*.jpeg', '*.jpg', '*.JPEG', '*.JPG',  '*.png')
            for files in types:
                self.fileList.extend(glob.glob(files))
            for i in range(0, len(self.fileList)):
                self.fileList[i] = folderPath + "/" + self.fileList[i]
            self.ui.folderNotFound.setText("")
            self.model.loadImage(self.fileList[0])
            self.ui.init(self.model.imageUrl, self.model.isPortrait())
            self.currentImageIndex = 0
            self.loadExif()

    def loadExif(self):
        exifData = self.model.convertExif()
        table = self.ui.tableWidget
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


if __name__ == '__main__':
    controller = Controller()
    controller.ui.show()
    controller.app.exec_()


