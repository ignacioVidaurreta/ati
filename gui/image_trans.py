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
from display import hdisplay

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
        img = self.parent.image.copy()
        if len(self.imageShape) == 3:
            # if image has r,g,b channels, apply the transform
            # to every channel
            r,g,b = img.split()
            self.negativeTransform(r)
            self.negativeTransform(g)
            self.negativeTransform(b)
            # We now need to merge the modified values into an RGB image
            img = Image.merge("RGB", (r,g,b))
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                "Negative Transformation of Image"
            ])
        else:
            self.negativeTransform(img)
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                "Negative Transformation of Image"
            ], cmap="gray")

    def negativeTransform(self, img):
        # This method is cool because you receive the pixels by memory
        # then, when modifying the pixels you modify the image.
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            pixels[x,y] = 255 - pixels[x,y]




