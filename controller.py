import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt
import PIL.Image
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from design import Ui_MainWindow

from model import Window, BeautyWindow


class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = BeautyWindow()
        self.window.ui.pushButton_3.clicked.connect(lambda: self.window.ui.widget.rotate(90))
        self.window.ui.pushButton.clicked.connect(lambda: self.ui.widget.rotate(-90))

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
            table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(exifData[data])))

if __name__ == '__main__':
    controller = Controller()
    controller.run()