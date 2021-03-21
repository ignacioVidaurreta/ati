import sys
from PyQt5 import sip
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

from crop import CropTab
from histogram import HistogramTab
from image_trans import ImageTransformTab
from operations import OperationsTab
from pixel import PixelTab

from utils import (
    RAW,
    get_file_type,
    read_image,
    save_image,
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
        self.setBasicLayout()

    def setBasicLayout(self):
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

        self.buttonRestart = QPushButton("Restart")
        self.buttonRestart.clicked.connect(self.onRestartClick)
        self.tab1.layout.addWidget(self.buttonRestart, 4, 0)

        self.tab1.setLayout(self.tab1.layout)


    def uploadImage(self):
        global img

        self.filenameError.hide()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Discards file_type since we are checking from extension
        file, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;PGM (*.pgm);;PPM (*.ppm);;RAW (*.raw);;PNG (*.png)",
            options=options
        )

        # This validation prevents the program from abortin when
        # user cancels file operation
        if file:
            self.file_type = get_file_type(file)

            if self.file_type == RAW:
                img = read_raw(file)
            else:
                img = read_image(file)

            if img is not None:
                self.image = img
                self.filename = file
                self.imageFilename = QLabel(f'{file}')
                self.tab1.layout.addWidget(self.imageFilename, 0, 1)
                # IMPORTANT: tabs wont appear until image is loaded
                self.enableTabs()
                # TODO: missing original image title
                img.show()


    def saveImage(self):
        if hasattr(self, 'image') and self.fileInput.text() and self.fileInput.text() != '':
            self.filenameError.hide()

            directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            filename = self.fileInput.text()
            filepath = f'{directory}/{filename}'

            # Actual saving image
            if self.file_type != RAW:
                # gets filepath using directory and filename
                save_image(self.image, filepath)
            else:
                shape = np.asarray(self.image).shape

                save_raw(
                    self.image,
                    filename,
                    directory,
                    shape[0],
                    shape[1]
                )

            # displays success message
            self.filepath = QLabel(f'Image saved at {filepath}')
            self.tab1.layout.addWidget(self.filepath, 3, 0)
        else:
            self.filenameError.show()


    def enableTabs(self):
        self.tab2 = PixelTab(self)
        self.tab3 = CropTab(self)
        self.tab4 = OperationsTab(self)
        self.tab5 = ImageTransformTab(self)

        self.tabs.addTab(self.tab2, "Pixel")
        self.tabs.addTab(self.tab3, "Crop")
        self.tabs.addTab(self.tab4, "Operations")
        self.tabs.addTab(self.tab5, "Transform")

        if len(np.asarray(self.image).shape) != 3:
            self.tab6 = HistogramTab(self)
            self.tabs.addTab(self.tab6, "Histogram")
    
    def onRestartClick(self):
        self.layout.removeWidget(self.tabs)
        sip.delete(self.tabs)
        self.tabs = None
        self.setBasicLayout()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())