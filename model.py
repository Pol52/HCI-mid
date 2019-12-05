import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QLayout, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import PIL.Image
from design import Ui_MainWindow
from PyQt5 import QtWidgets


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
        self.imageData = PIL.Image.open(self.imageUrl)
        self.exif_data = self.imageData._getexif()
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
        exif_data = self.exif_data
        exif_data["Image Type"] = self.imageUrl.split(".")[-1]
        exif_data["Width"] = exif_data.pop(40962)
        exif_data["Height"] = exif_data.pop(40963)
        exif_data["Camera Brand"] = exif_data.pop(271)
        exif_data["Camera Model"] = exif_data.pop(272)
        shutterSpeed = exif_data.pop(37377)
        exif_data["Exposure Time"] = round(2 ** (shutterSpeed[0] / shutterSpeed[1]))
        exif_data["Exposure Program"] = getExposureProgram(exif_data.pop(34850))
        exif_data["Aperture Value"] = getApertureValue(exif_data.pop(37378))
        exif_data["ISO"] = exif_data.pop(34855)
        exif_data["Flash used"] = exif_data.pop(37385)
        focalLengthTuple = exif_data.pop(37386)
        exif_data["Focal length"] = focalLengthTuple[0] / focalLengthTuple[1]
        # exif_data["Comment"] = exif_data.pop(37510)
        exif_data["Creator"] = exif_data.pop(315)
        exif_data["Generated on"] = exif_data.pop(36867)
        exif_data["Last modified on"] = exif_data.pop(36868)
        exif_data["Copyright"] = exif_data.pop(33432)
        for data in exif_data:
            if type(data) != int:
                result[data] = exif_data[data]

        return result


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
    print(key)
    programs[1] = "Manual"
    return programs[key]

def getApertureValue(value): #TODO:
    return '2.8'