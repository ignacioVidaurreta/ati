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

from utils import (
    RAW,
    PGM,
    PPM,
    get_file_type,
    read_pgm_ppm,
    read_raw,
    crop_image,
    copy_crop_into_img
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
        self.tab3 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Loader")
        self.tabs.addTab(self.tab2,"Pixel")
        self.tabs.addTab(self.tab3,"Crop")

        self.loaderTab()
        self.pixelTab()
        self.cropTab()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def loaderTab(self): 
        # Create first tab
        self.tab1.layout = QGridLayout(self)

        self.buttonOpen = QPushButton("Upload Image")
        self.buttonOpen.clicked.connect(self.uploadImage)
        self.tab1.layout.addWidget(self.buttonOpen, 0, 0)

        self.buttonSave = QPushButton("Save Image")
        self.buttonSave.clicked.connect(self.uploadImage)
        self.tab1.layout.addWidget(self.buttonSave, 0, 1)

        self.tab1.setLayout(self.tab1.layout)

    def pixelTab(self):
        self.tab2.layout = QGridLayout(self)
        
        self.tab2.layout.addWidget(QLabel("X: "), 0, 0)
        self.tab2.layout.addWidget(QLineEdit(), 0, 1)
        self.tab2.layout.addWidget(QLabel("Y: "), 0, 2)
        self.tab2.layout.addWidget(QLineEdit(), 0, 3)

        self.buttonValue = QPushButton("Get pixel value")
        self.buttonValue.clicked.connect(self.uploadImage)
        self.tab2.layout.addWidget(self.buttonValue, 1, 0)
        
        self.tab2.layout.addWidget(QLabel("Value: "), 2, 0)
        self.tab2.layout.addWidget(QLineEdit(), 2, 1)

        self.tab2.setLayout(self.tab2.layout)

    def cropTab(self):
        pass

    def uploadImage(self):
        global img
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Discards file_type since we are checking from extension
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PGM (*.pgm);;PPM (*.ppm);;RAW (*.raw);;PNG (*.png)", options=options)

        # This validation prevents the program from abortin when
        # user cancels file operation
        if file:
            file_type = get_file_type(file)

            if file_type in [PGM, PPM]:
                img = read_pgm_ppm(file)
            else:
                img = read_raw(file)

            if img is not None:
                #img.show()
                copy_crop_into_img(img, 10, 10, 100, 100)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())