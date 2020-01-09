import PIL.Image
import PIL.ExifTags
import datetime
from .ExifEnum import meteringMode, lightSource, exposureProgram, captureType, sensingMethod
from PyQt5 import QtCore


class ImageModel(QtCore.QAbstractItemModel):

    def __init__(self, *__args):
        QtCore.QAbstractItemModel.__init__(self, *__args)
        self.imageUrl = ''
        self.exifData = {}
        self.imageWidth = 0
        self.imageHeight = 0

    def loadImage(self, imageUrl):
        self.imageUrl = imageUrl
        im = PIL.Image.open(self.imageUrl)
        self.exifData = im._getexif()
        self.imageWidth, self.imageHeight = im.size

    def convertExif(self):
        result = {}
        if self.exifData is not None:
            for key in self.exifData:
                if key in PIL.ExifTags.TAGS:
                    result[PIL.ExifTags.TAGS[key]] = self.convertToReadable(key)
        return result

    def convertToReadable(self, key):
        if "b'" in str(self.exifData[key]) and key != 34853:
            result = str(list(self.exifData[key]))
        elif key == 33434:
            result = "1/" + str(round(self.exifData[key][1] / self.exifData[key][0]))
        elif key == 33473:
            result = self.exifData[key][0] / self.exifData[key][1]
        elif key == 33473:
            result = self.exifData[0] / self.exifData[1]
        elif key == 37378:
            result = self.getApertureValue(self.exifData[key])
        elif key == 37377:
            result = self.getShutterSpeedValue(self.exifData[key])
        elif key == 37380:
            result = round(self.exifData[key][0] / self.exifData[key][1], 2)
        elif key == 37381:
            result = self.getApertureValue(self.exifData[key])
        elif key == 37383:
            result = meteringMode[self.exifData[key]]
        elif key == 37384:
            result = lightSource[self.exifData[key]]
        elif key == 37386:
            result = self.exifData[key][0] / self.exifData[key][1]
        elif key == 34850:
            result = exposureProgram[self.exifData[key]]
        elif key == 34853 and len(self.exifData[key]) > 1:
            coordinates = self.get_coordinates(self.exifData[key])
            result = "https://www.google.com/maps/search/?api=1&query=" + str(coordinates[0]) + "," + str(coordinates[1])
        elif key == 36867 or key == 36868 or key == 306:
            result = self.dateFormatter(self.exifData[key])
        elif key == 41495:
            result = sensingMethod[self.exifData[key]]
        elif key == 41990:
            result = captureType[self.exifData[key]]
        else:
            result = self.exifData[key]
        return result

    def isPortrait(self):
        return (self.imageWidth / self.imageHeight) > 1

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
