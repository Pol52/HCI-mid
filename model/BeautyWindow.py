from PyQt5.QtWidgets import QMainWindow
from design.design import Ui_MainWindow
from PyQt5 import QtWidgets


class BeautyWindow(QMainWindow):
    def __init__(self, imagePath):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.imageWidget.loadImage(imagePath)
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
