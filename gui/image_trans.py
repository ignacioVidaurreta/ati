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
        self.umbralization = newButton("Umbralization", self.onUmbralizationClick)
        
        # Labels for umbral input
        self.umbralLabel = QLabel("Umbral")
        self.umbralInput = QLineEdit()
        self.umbralInput.setText('255')

        # We add widgets to layout
        self.layout.addWidget(self.negative, 1, 0)
        self.layout.addWidget(self.umbralLabel, 2, 0)
        self.layout.addWidget(self.umbralInput, 2, 1)
        self.layout.addWidget(self.umbralization, 3, 0)

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onNegativeClick(self):
        # We do not want to loose original image
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
    
    def onUmbralizationClick(self):
        self.umbralValue = int(self.umbralInput.text())
        print(f"About to apply umbralization with umbral {self.umbralValue}")

        # We do not want to loose original image
        img = self.parent.image.copy()

        if len(self.imageShape) == 3:
            # if image has r,g,b channels, apply the transform
            # to every channel
            r,g,b = img.split()
            self.umbralizationTransform(r)
            self.umbralizationTransform(g)
            self.umbralizationTransform(b)
            # We now need to merge the modified values into an RGB image
            img = Image.merge("RGB", (r,g,b))
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                "Umbralization of Image"
            ])
        else:
            self.umbralizationTransform(img)
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Umbralization with Umbral={self.umbralValue}"
            ], cmap="gray")
    
    def umbralizationTransform(self, img):
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            if pixels[x,y] < self.umbralValue:
                pixels[x,y] = 0
            else:
                pixels[x,y] = 255
