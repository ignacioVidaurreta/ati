import sys
from PyQt5.QtWidgets import QFileDialog,QHBoxLayout, QRadioButton, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import cv2

from utils import (
    RAW,
    PGM,
    PPM,
    get_file_type,
    read_pgm_ppm
)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'ATI Project'
        self.left, self.top = 0, 0
        self.width, self.height = 600, 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_window = MainWindow(self)
        self.setCentralWidget(self.main_window)

        self.show()

class MainWindow(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Image Uploader")
        self.tabs.addTab(self.tab2,"WIP")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.buttonOpen = QPushButton("Upload Image")
        self.buttonOpen.clicked.connect(self.uploadImage)
        self.tab1.layout.addWidget(self.buttonOpen)
        self.tab1.setLayout(self.tab1.layout)

        self.radio_sublayout = QVBoxLayout(self)
        self.radioButton = QRadioButton("By pixel")
        self.radioButton_2 = QRadioButton("By square")
        self.radioButton_2.setChecked(True)
        self.radio_sublayout.addWidget(self.radioButton)
        self.radio_sublayout.addWidget(self.radioButton_2)

        self.tab1.layout.addLayout(self.radio_sublayout)
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # @pyqtSlot()
    # def on_click(self):
    #     print("Hello World\n")
    def uploadImage(self):
        global img
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        
        # Discards file_type since we are checking from extension
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PGM (*.pgm);;PPM (*.ppm);;RAW (*.raw);;PNG (*.png)", options=options)
        
        file_type = get_file_type(file)
        
        if file_type in [PGM, PPM]:
            img = read_pgm_ppm(file)
        else:
            pass #TODO: implement
        
        if img is not None:
            img.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())