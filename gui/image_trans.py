import sys
import numpy as np

from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QFormLayout,
    QLabel,
    QLineEdit

)
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, QSize
from utils import newButton, newAxisButton
from PIL import Image
import cv2

class ImageTransformTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Buttons definitions
        self.negative = newButton("Negative", self.onNegativeClick)


        # We add widgets to layout
        self.layout.addWidget(self.negative, 1, 1)

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onNegativeClick(self):
        print(self.imageShape)
        if len(self.imageShape) != 2:
            raise NotImplementedError("Oops unsupported file for now")

        neg_operator = lambda x: -x + 255
        vectorized_op = np.vectorize(neg_operator)

        new_arr = vectorized_op(self.image)

        a =  Image.fromarray(new_arr, mode="L")
        a.show()

