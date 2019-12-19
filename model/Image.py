
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import PIL.Image
import PIL.ExifTags
import datetime
from model.ExifEnum import meteringMode, lightSource, exposureProgram, captureType, sensingMethod


class Image(QLabel):

    rotation = 0
    imageUrl = ''
    aspectRatio = 1
    imageWidth = 0
    imageHeight = 0

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)
        self.setAlignment(Qt.AlignCenter)

    def loadImage(self, imageUrl):
        if imageUrl is not None:
            self.rotation = 0
            self.imageUrl = imageUrl
            pixmap = QPixmap(self.imageUrl)
            self.setPixmap(pixmap)
            self.aspectRatio = pixmap.width() / pixmap.height()
            imageData = PIL.Image.open(self.imageUrl)
            self.exif_data = imageData._getexif()

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

    def convertExif(self):
        result = {}
        if self.exif_data is not None:
            for key in self.exif_data:
                if key in PIL.ExifTags.TAGS:
                    result[PIL.ExifTags.TAGS[key]] = self.convertToReadable(key)
        return result

    def convertToReadable(self, key):
        if "b'" in str(self.exif_data[key]) and key != 34853:
            result = str(list(self.exif_data[key]))
        elif key == 33434:
            result = "1/" + str(round(self.exif_data[key][1] / self.exif_data[key][0]))
        elif key == 33473:
            result = self.exif_data[key][0] / self.exif_data[key][1]
        elif key == 33473:
            result = self.exif_data[0] / self.exif_data[1]
        elif key == 37378:
            result = self.getApertureValue(self.exif_data[key])
        elif key == 37377:
            result = self.getShutterSpeedValue(self.exif_data[key])
        elif key == 37380:
            result = round(self.exif_data[key][0] / self.exif_data[key][1], 2)
        elif key == 37381:
            result = self.getApertureValue(self.exif_data[key])
        elif key == 37383:
            result = meteringMode[self.exif_data[key]]
        elif key == 37384:
            result = lightSource[self.exif_data[key]]
        elif key == 37386:
            result = self.exif_data[key][0] / self.exif_data[key][1]
        elif key == 34850:
            result = exposureProgram[self.exif_data[key]]
        elif key == 34853 and len(self.exif_data[key]) > 1:
            coordinates = self.get_coordinates(self.exif_data[key])
            result = "https://www.google.com/maps/search/?api=1&query=" + str(coordinates[0]) + "," + str(coordinates[1])
        elif key == 36867 or key == 36868 or key == 306:
            result = self.dateFormatter(self.exif_data[key])
        elif key == 41495:
            result = sensingMethod[self.exif_data[key]]
        elif key == 41990:
            result = captureType[self.exif_data[key]]
        else:
            result = self.exif_data[key]
        return result

    @staticmethod
    def dateFormatter(exifDate):
        dateParser = datetime.datetime.strptime(exifDate, '%Y:%m:%d %H:%M:%S')
        newDate = dateParser.strftime('%d/%m/%y %H:%M:%S')
        return newDate

    def get_coordinates(self, geotags):
        lat = self.get_decimal_from_dms(geotags[2], geotags[1])

        lon = self.get_decimal_from_dms(geotags[4], geotags[3])

        return lat, lon

    @staticmethod
    def get_decimal_from_dms(dms, ref):

        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    @staticmethod
    def getApertureValue(value):
        apexApertureValue = value[0] / value[1]
        fApertureValue = round(2 ** (apexApertureValue / 2), 1)
        return fApertureValue

    @staticmethod
    def getShutterSpeedValue(value):
        shutterSpeed = value[0] / value[1]
        return round(2**shutterSpeed)
