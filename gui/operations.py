import sys
import numpy as np

from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QFileDialog
)
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, QSize
from utils import *
from matrix_util import *

class OperationsTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape
        
        # Buttons definitions
        self.sum = newButton("SUM", self.onSumClick)
        self.subst = newButton("SUBST", self.onSubstClick)
        self.mul = newButton("MUL", self.onMulClick)

        # We add widgets to layout
        self.layout.addWidget(self.sum, 0, 0)
        self.layout.addWidget(self.subst, 0, 1)
        self.layout.addWidget(self.mul, 0, 2)

        self.setLayout(self.layout)

    def onSumClick(self):
        otherImage = self.selectImage()
        if otherImage is not None:
            result = matrix_sum(self.image, otherImage)
            if result is not None:
                sumImage = Image.fromarray(result)
                sumImage.show()
                sumImage.save('./data/sum.png')
                return

        # all errors will be here
        self.operationError = QLabel('The sum could not be executed')
        self.layout.addWidget(self.operationError, 1, 0)

    def onSubstClick(self):
        otherImage = self.selectImage()
        if otherImage is not None:
            result = matrix_subst(self.image, otherImage)
            if result is not None:
                substImage = Image.fromarray(result)
                substImage.show()
                substImage.save('./data/subst.png')
                return
        
        # all errors will be here
        self.operationError = QLabel('The substraction could not be executed')
        self.layout.addWidget(self.operationError, 1, 0)


    def onMulClick(self):
        otherImage = self.selectImage()
        if otherImage is not None:
            result = matrix_mult(self.image, otherImage)
            if result is not None:
                mulImage = Image.fromarray(result)
                mulImage.show()
                mulImage.save('./data/mul.png')
                return
        
        # all errors will be here
        self.operationError = QLabel('The multiplication could not be executed')
        self.layout.addWidget(self.operationError, 1, 0)


    # Will return selected image as a numpy array
    def selectImage(self):
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

            if self.file_type in [PGM, PPM]:
                img = read_image(file)
            else:
                img = read_raw(file)

            if img is not None:
                return np.asarray(img)
        
        return None