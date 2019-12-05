import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import PIL.Image
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from design import Ui_MainWindow

from model import Window


class BeautyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.ui.widget.label.rotateClockwise)
        self.ui.pushButton.clicked.connect(self.ui.widget.label.rotateAntiClockwise)

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = BeautyWindow()

    def run(self):
        self.window.show()
        self.loadExif()
        return self.app.exec_()

    def loadExif(self):
        exifData = self.window.ui.widget.label.convertExif()
        table = self.window.ui.tableWidget
        for data in exifData:
            print(data)
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(data))
            table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(exifData[data]))


if __name__ == '__main__':
    controller = Controller()
    controller.run()
    # app = QApplication(sys.argv)
    # newWindow = BeautyWindow()
    # newWindow.show()
    # exifData = model.image.label.exif_data
    # print(exifData)
    # for index, data in enumerate(exifData, start=0):
    #     print(data)
    #     newWindow.ui.tableWidget.setItem(index, 0, QTableWidgetItem(data))
    #     newWindow.ui.tableWidget.setItem(index, 1, QTableWidgetItem(exifData[data]))
    # app.exec_()