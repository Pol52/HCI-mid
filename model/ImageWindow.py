from PyQt5.QtWidgets import QWidget
from model.Image import Image


class ImageWindow(QWidget):

    def __init__(self, parent=None, Qt_WindowFlags=None, Qt_WindowType=None, *args, **kwargs):
        QWidget.__init__(self)
        self.label = Image(self)

    def resizeEvent(self, event):
        self.label.resize(self.width(), self.height())
        self.checkAspectRatio()

    def rotate(self, angle):
        width = self.width()
        height = self.height()
        self.label.rotate(width, height, angle)
        self.checkAspectRatio()

    def checkAspectRatio(self):
        imageWidth = self.label.imageWidth
        expectedHeight = imageWidth / self.label.aspectRatio
        if expectedHeight > self.height():
            self.label.resizeOverflow('height', self.width(), self.height())

        imageHeight = self.label.imageHeight
        expectedWidth = imageHeight * self.label.aspectRatio
        if expectedWidth > self.width():
            self.label.resizeOverflow('width', self.width(), self.height())