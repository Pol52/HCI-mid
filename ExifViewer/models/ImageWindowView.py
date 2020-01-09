from PyQt5.QtWidgets import QWidget
from ExifViewer.models.ImageView import Image


class ImageWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.image = Image(self)

    def resizeEvent(self, event):
        self.image.resize(self.width(), self.height())
        self.checkAspectRatio()

    def rotate(self, angle):
        width = self.width()
        height = self.height()
        self.image.rotate(width, height, angle)
        self.checkAspectRatio()

    def checkAspectRatio(self):
        imageWidth = self.image.imageWidth
        expectedHeight = imageWidth / self.image.aspectRatio
        if expectedHeight > self.height():
            self.image.resizeOverflow('height', self.width(), self.height())

        imageHeight = self.image.imageHeight
        expectedWidth = imageHeight * self.image.aspectRatio
        if expectedWidth > self.width():
            self.image.resizeOverflow('width', self.width(), self.height())

    def loadImage(self, imagePath):
        if imagePath is not None:
            self.image.loadImage(imagePath)
            self.image.resize(self.width(), self.height())
            self.checkAspectRatio()
