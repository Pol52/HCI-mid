import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QLayout, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import PIL.Image
import PIL.ExifTags
from design import Ui_MainWindow
from PyQt5 import QtWidgets
import datetime


class Image(QLabel):

    rotation = 0
    imageUrl = 'image.jpeg'
    aspectRatio = 0
    originalWidth = 0
    originalHeight = 0

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)
        self.pixmap = QPixmap(self.imageUrl)
        self.setPixmap(self.pixmap)
        imageData = PIL.Image.open(self.imageUrl)
        self.exif_data = imageData._getexif()
        print(self.exif_data)
        self.rotation = 0
        self.aspectRatio = self.pixmap.width() / self.pixmap.height()
        self.setAlignment(Qt.AlignCenter)

    def resize(self, width, height):
        QLabel.resize(self, width, height)
        self.pixmap = QPixmap(self.imageUrl)
        self.pixmap = self.pixmap.transformed(QTransform().rotate(self.rotation))
        if self.pixmap.width() > self.pixmap.height():
            self.pixmap = self.pixmap.scaledToHeight(height)
        else:
            self.pixmap = self.pixmap.scaledToWidth(width)
        self.setPixmap(self.pixmap)

    def resizeOverflow(self, axis, width, height):
        if axis == 'width':
            QLabel.resize(self, width, height)
            self.pixmap = QPixmap(self.imageUrl)
            self.pixmap = self.pixmap.transformed(QTransform().rotate(self.rotation))
            self.pixmap = self.pixmap.scaledToWidth(width)
            self.setPixmap(self.pixmap)
        if axis == 'height':
            QLabel.resize(self, width, height)
            self.pixmap = QPixmap(self.imageUrl)
            self.pixmap = self.pixmap.transformed(QTransform().rotate(self.rotation))
            self.pixmap = self.pixmap.scaledToHeight(height)
            self.setPixmap(self.pixmap)

    def rotate(self, width, height, angle):
        QLabel.resize(self, width, height)
        pixmap = QPixmap(self.imageUrl)
        rotation = self.rotation + angle
        pixmap = pixmap.transformed(QTransform().rotate(rotation))
        self.rotation = self.rotation % 360
        self.rotation = self.rotation + angle
        if self.rotation % 180 == 0:
            pixmap = pixmap.scaledToWidth(width)
        else:
            pixmap = pixmap.scaledToHeight(height)
        self.pixmap = pixmap
        self.aspectRatio = self.pixmap.width() / self.pixmap.height()
        self.setPixmap(self.pixmap)
        self.setAlignment(Qt.AlignCenter)

    def convertExif(self):
        result = {}
        for key in self.exif_data:
            if key in PIL.ExifTags.TAGS:

                result[PIL.ExifTags.TAGS[key]] = self.formatValue(key)
        return result

    def formatValue(self, key):
        if key == 36867 or key == 36868 or key == 306:
            result = self.dateFormatter(self.exif_data[key])
            print(list(self.exif_data[key]))
        else:
            result = self.exif_data[key]
        return result

    def dateFormatter(self, exifDate):
        dateParser = datetime.datetime.strptime(exifDate, '%Y:%m:%d %H:%M:%S')
        newDate = dateParser.strftime('%d/%m/%y %H:%M:%S')
        return newDate


class Window(QWidget):

    def __init__(self, parent=None, Qt_WindowFlags=None, Qt_WindowType=None, *args, **kwargs):
        QWidget.__init__(self)
        self.label = Image(self)
        self.label.resize(self.width(), self.height())

    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height())
        self.checkAspectRatio()

    def rotate(self, angle):
        width = self.width()
        height = self.height()
        self.label.rotate(width, height, angle)
        self.checkAspectRatio()

    def checkAspectRatio(self):
        imageWidth = self.label.pixmap.width()
        expectedHeight = imageWidth / self.label.aspectRatio
        if expectedHeight > self.height():
            self.label.resizeOverflow('height', self.width(), self.height())

        imageHeight = self.label.pixmap.height()
        expectedWidth = imageHeight * self.label.aspectRatio
        if expectedWidth > self.width():
            self.label.resizeOverflow('width', self.width(), self.height())


class BeautyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

def getExposureProgram(key):
    programs = {}
    programs[1] = "Manual"
    return programs[key]

def getApertureValue(value):
    apexApertureValue = value[0]/value[1]
    fApertureValue = round(2 ** (apexApertureValue / 2), 1)
    return fApertureValue


