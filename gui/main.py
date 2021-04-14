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
from noise import NoiseTab
from saltpepper import SaltPepperTab
from filters import FilterTab
from shape_detect import ShapeDetectTab

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
    newAxisButton,
    numpy_to_pil_image
)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'ATI Project'
        self.left, self.top = 0, 0
        self.width, self.height = 1000, 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_window = MainWindow(self)
        self.setCentralWidget(self.main_window)

        # IMAGE CHANGE 1
        # This array wil contain changes. If image is B&N each element is a numpy array.
        # If image is color, each element is a tuple (r,g,b), where each is a numpy array.
        self.changes = []
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

        self.buttonShow = QPushButton("Show Image")
        self.buttonShow.clicked.connect(self.onShowClick)
        self.tab1.layout.addWidget(self.buttonShow, 5, 0)
        self.buttonShow.setEnabled(False)


        self.buttonUndo = QPushButton("Undo")
        self.buttonUndo.clicked.connect(self.onUndoClick)
        self.tab1.layout.addWidget(self.buttonUndo, 6, 0)
        self.buttonUndo.setEnabled(False)

        self.tab1.setLayout(self.tab1.layout)


    def uploadImage(self):
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
            img = None
            self.file_type = get_file_type(file)

            if self.file_type == RAW:
                img = read_raw(file)
            else:
                img = read_image(file)

            if img is not None:
                # stores original PIL image
                self.image = img
                
                # IMAGE CHANGE 2
                # we will store first image in order to
                # always access current image from changes
                self.changes = []
                if self.image.mode == 'RGB':
                    r,g,b = self.image.split()
                    self.changes.append((
                        np.array(r),
                        np.array(g),
                        np.array(b)))
                else:
                    self.changes.append(np.array(self.image))  
                print(self.changes[0])                  

                self.filename = file
                self.imageFilename = QLabel(f'{file}')
                self.tab1.layout.addWidget(self.imageFilename, 0, 1)
                # IMPORTANT: tabs wont appear until image is loaded
                self.enableTabs()
                self.buttonShow.setEnabled(True)
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
                save_image(self.image, filepath + ".jpg")
            else:
                shape = np.asarray(self.image).shape

                save_raw(
                    self.image,
                    filename + ".RAW",
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
        # Tab 6 is the histogram
        self.tab7 = FilterTab(self)
        self.tab8 = NoiseTab(self)
        self.tab9 = SaltPepperTab(self)
        self.tab10 = ShapeDetectTab(self)

        # TODO: commented tabs still need round problem to be solved
        # 2, 3, 4, 5, 6, 8, 9, 10

        # self.tabs.addTab(self.tab2, "Pixel")
        # self.tabs.addTab(self.tab3, "Crop")
        # self.tabs.addTab(self.tab4, "Operations")
        # self.tabs.addTab(self.tab5, "Transform")
        self.tabs.addTab(self.tab7, "Filter")
        # self.tabs.addTab(self.tab8, "Noise")
        # self.tabs.addTab(self.tab9, "S and P")
        # self.tabs.addTab(self.tab10, "Shape Detection")


        if len(np.asarray(self.image).shape) != 3:
            self.tab6 = HistogramTab(self)
            # self.tabs.addTab(self.tab6, "Histogram")

    def onRestartClick(self):
        self.layout.removeWidget(self.tabs)
        sip.delete(self.tabs)
        self.tabs = None
        self.setBasicLayout()

    def onUndoClick(self):
        self.image = numpy_to_pil_image(self.changes.pop())
        # we always have the first image stored here !!
        if len(self.changes) == 1:
            self.buttonUndo.setEnabled(False)

    def onShowClick(self):
        self.image.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())