import sys
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QRadioButton,
    QMainWindow,
    QApplication,
    QPushButton,
    QWidget,
    QAction,
    QTabWidget,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QLabel,
    QLineEdit

)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize
import cv2
import numpy as np

from pixel import PixelTab
from crop import CropTab

from utils import (
    RAW,
    PGM,
    PPM,
    get_file_type,
    read_pgm_ppm,
    save_pgm_ppm,
    read_raw,
    save_raw,
    crop_image,
    copy_crop_into_img,
    newButton,
    newAxisButton
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

        self.image = None # we should remove img as global

        self.show()

class MainWindow(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Loader")

        self.loaderTab()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def loaderTab(self):
        # Create first tab
        self.tab1.layout = QGridLayout(self)

        self.buttonOpen = QPushButton("Upload Image")
        self.buttonOpen.clicked.connect(self.uploadImage)
        self.tab1.layout.addWidget(self.buttonOpen, 0, 0)

        self.fileLabel = QLabel(f'Save with filename: ')
        self.fileInput = QLineEdit()
        self.tab1.layout.addWidget(self.fileLabel, 1, 0)
        self.tab1.layout.addWidget(self.fileInput, 1, 1)

        self.buttonSave = QPushButton("Save")
        self.buttonSave.clicked.connect(self.saveImage)
        self.tab1.layout.addWidget(self.buttonSave, 1, 2)

        self.filenameError = QLabel('Make sure you have loaded and image and set a filename')
        self.tab1.layout.addWidget(self.filenameError, 3, 0)
        self.filenameError.hide()

        self.tab1.setLayout(self.tab1.layout)


    def uploadImage(self):
        global img
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Discards file_type since we are checking from extension
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PGM (*.pgm);;PPM (*.ppm);;RAW (*.raw);;PNG (*.png)", options=options)

        # This validation prevents the program from abortin when
        # user cancels file operation
        if file:
            self.file_type = get_file_type(file)

            if self.file_type in [PGM, PPM]:
                img = read_pgm_ppm(file)
            else:
                img = read_raw(file)

            if img is not None:
                self.image = img
                self.imageFilename = QLabel(f'{file}')
                self.tab1.layout.addWidget(self.imageFilename, 0, 1)
                # IMPORTANT: tabs wont appear until image is loaded
                self.enableTabs()
    

    def saveImage(self):
        if hasattr(self, 'image') and self.fileInput.text() and self.fileInput.text() != '':
            self.filenameError.hide()
            
            # gets filepath using directory and filename
            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            filepath = f'{directory}/{self.fileInput.text()}'
            
            if self.file_type in [PGM, PPM]:
                # saves image
                save_pgm_ppm(self.image, filepath)
            else:
                save_raw(self.image, filepath)
            
            # displays success message
            self.filepath = QLabel(f'Image saved at {filepath}')
            self.tab1.layout.addWidget(self.filepath, 3, 0)
        else:
            self.filenameError.show()


    def enableTabs(self):
        self.tab2 = PixelTab(self)
        self.tab3 = CropTab(self)
        self.tabs.addTab(self.tab2,"Pixel")
        self.tabs.addTab(self.tab3,"Crop")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())