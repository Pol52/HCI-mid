import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui

from model.BeautyWindow import BeautyWindow


class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        app_icon = QtGui.QIcon()
        app_icon.addFile('assets/main-icon.png', QtCore.QSize(24, 24))
        self.app.setWindowIcon(app_icon)
        self.window = BeautyWindow()
        self.connectButtons()

    def connectButtons(self):
        self.window.ui.pushButton_3.clicked.connect(lambda: self.window.ui.widget.rotate(90))
        self.window.ui.pushButton.clicked.connect(lambda: self.window.ui.widget.rotate(-90))

    def loadExif(self):
        exifData = self.window.ui.widget.label.convertExif()
        table = self.window.ui.tableWidget
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

    @staticmethod
    def loadGPS(table, exifData):
        gpsLabel = QLabel()
        gpsLabel.setText('<a href="' + exifData['GPSInfo'] + '">Click to see Location</a>')
        gpsLabel.setOpenExternalLinks(True)
        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem('GPS Info'))
        table.setCellWidget(table.rowCount() - 1, 1, gpsLabel)

    def run(self):
        self.window.show()
        self.loadExif()
        return self.app.exec_()


controller = Controller()

