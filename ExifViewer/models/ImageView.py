
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class Image(QLabel):

    rotation = 0
    imageUrl = ''
    aspectRatio = 1
    imageWidth = 0
    imageHeight = 0

    def __init__(self, *__args):
        QtCore.QAbstractItemModel.__init__(self, *__args)
        QLabel.__init__(self, *__args)
        self.setAlignment(Qt.AlignCenter)

    def loadImage(self, imageUrl):
        if imageUrl is not None:
            self.rotation = 0
            self.imageUrl = imageUrl
            pixmap = QPixmap(self.imageUrl)
            pixmap = pixmap.scaledToWidth(1000)
            self.setPixmap(pixmap)
            self.aspectRatio = pixmap.width() / pixmap.height()

    def resize(self, width, height):
        QLabel.resize(self, width, height)
        pixmap = QPixmap(self.imageUrl)
        pixmap = pixmap.transformed(QTransform().rotate(self.rotation))
        if pixmap.width() > pixmap.height():
            pixmap = pixmap.scaledToHeight(height)
        else:
            pixmap = pixmap.scaledToWidth(width)
        self.setPixmap(pixmap)
        self.imageHeight = pixmap.height()
        self.imageWidth = pixmap.width()

    def resizeOverflow(self, axis, width, height):
        if axis == 'width':
            QLabel.resize(self, width, height)
            pixmap = QPixmap(self.imageUrl)
            pixmap = pixmap.transformed(QTransform().rotate(self.rotation))
            pixmap = pixmap.scaledToWidth(width)
            self.setPixmap(pixmap)

        if axis == 'height':
            QLabel.resize(self, width, height)
            pixmap = QPixmap(self.imageUrl)
            pixmap = pixmap.transformed(QTransform().rotate(self.rotation))
            pixmap = pixmap.scaledToHeight(height)
            self.setPixmap(pixmap)
        self.imageHeight = pixmap.height()
        self.imageWidth = pixmap.width()

    def rotate(self, width, height, angle):
        QLabel.resize(self, width, height)
        pixmap = QPixmap(self.imageUrl)
        rotation = self.rotation + angle
        pixmap = pixmap.transformed(QTransform().rotate(rotation))
        self.rotation = rotation
        self.rotation = self.rotation % 360
        if self.rotation % 180 == 0:
            pixmap = pixmap.scaledToWidth(width)
        else:
            pixmap = pixmap.scaledToHeight(height)
        self.aspectRatio = pixmap.width() / pixmap.height()
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.imageHeight = pixmap.height()
        self.imageWidth = pixmap.width()
