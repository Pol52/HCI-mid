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

    def loadFiles(self, folderPath):
        try:
            os.chdir(folderPath)
        except OSError as e:
            self.window.ui.folderNotFound.setText("Can not locate folder")
        else:
            self.fileList = []
            types = ('*.jpg', '*.JPEG', '*.JPG', '*.png')
            for files in types:
                self.fileList.extend(glob.glob(files))
            for i in range(0, len(self.fileList)):
                self.fileList[i] = folderPath + "/" + self.fileList[i]
            self.window.ui.folderNotFound.setText("")
            self.window.ui.widget.loadImage(self.fileList[0])
            self.currentImageIndex = 0
            self.loadExif()

    def loadExif(self):
        exifData = self.window.ui.widget.image.convertExif()
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

    def connectButtons(self):
        self.window.ui.pushButton_3.clicked.connect(lambda: self.window.ui.widget.rotate(90))
        self.window.ui.pushButton.clicked.connect(lambda: self.window.ui.widget.rotate(-90))
        self.window.ui.pushButton_2.clicked.connect(self.previousPhoto)
        self.window.ui.pushButton_4.clicked.connect(self.nextPhoto)
        self.window.ui.pushButton_5.clicked.connect(lambda: self.loadFiles(self.window.ui.lineEdit.text()))

    def previousPhoto(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.window.ui.widget.loadImage(self.fileList[self.currentImageIndex])
            self.loadExif()

    def nextPhoto(self):
        if self.currentImageIndex < len(self.fileList)-1:
            self.currentImageIndex += 1
            self.window.ui.widget.loadImage(self.fileList[self.currentImageIndex])
            self.loadExif()

    def run(self):
        self.window.show()
        return self.app.exec_()


controller = Controller()

