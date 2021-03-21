import cv2
import sys
import math
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
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from utils import newButton, newAxisButton
from PIL import Image
from display import hdisplay
from utils import compute_histogram

TRANSFORMATION_FOLDER = 'transformations'

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
        self.gamma = newButton("Apply Gamma", self.onGammaClick)
        self.equalize = newButton("Equalize", self.onEqualizeClick)
        
        # Labels for umbral input
        self.umbralLabel = QLabel("Umbral")
        self.umbralInput = QLineEdit()
        self.umbralInput.setText('255')

        # Labels for umbral input
        self.gammaLabel = QLabel("Gamma")
        self.gammaInput = QLineEdit()
        self.gammaInfo = QLabel("0 < \u03B3 < 2, \u03B3 != 1")
        self.gammaInput.setText('0.1')

        # We add widgets to layout for each transformation
        
        self.layout.addWidget(self.negative, 1, 0)
        
        self.layout.addWidget(self.umbralLabel, 2, 0)
        self.layout.addWidget(self.umbralInput, 2, 1)
        self.layout.addWidget(self.umbralization, 3, 0)

        # Just for B&w images
        if len(self.imageShape) != 3:
            self.layout.addWidget(self.gammaLabel, 4, 0)
            self.layout.addWidget(self.gammaInput, 4, 1)
            self.layout.addWidget(self.gammaInfo, 4, 2)
            self.layout.addWidget(self.gamma, 5, 0)

            self.layout.addWidget(self.equalize, 6, 0)

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
        
        filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        img.save(f'{TRANSFORMATION_FOLDER}/{filename}_negative.png')

    def negativeTransform(self, img):
        # This method is cool because you receive the pixels by memory
        # then, when modifying the pixels you modify the image.
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            pixels[x,y] = 255 - pixels[x,y]
    
    def onUmbralizationClick(self):
        self.umbralValue = int(self.umbralInput.text())

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
        
        filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        img.save(f'{TRANSFORMATION_FOLDER}/{filename}_umbral_{str(self.umbralValue)}.png')
    
    def umbralizationTransform(self, img):
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            if pixels[x,y] < self.umbralValue:
                pixels[x,y] = 0
            else:
                pixels[x,y] = 255

    def onGammaClick(self):
        gamma = float(self.gammaInput.text())

        # We do not want to loose original image
        img = self.parent.image.copy()

        # We want to apply T(r) = c * r ^ gamma
        # where c = (L-1)^(1-gamma)
        c = 255 ** (1-gamma)

        pixels = img.load()
        for x,y in np.ndindex(img.size):
            pixel = pixels[x,y]
            pixels[x,y] = int(
                math.ceil(
                    c*(pixel ** gamma)
                )
            )
        
        filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        img.save(f'{TRANSFORMATION_FOLDER}/{filename}_power_{str(gamma)}.png')
        
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Power function with \u03B3={gamma}"
            ], cmap="gray")

    def onEqualizeClick(self):
        # We do not want to loose original image
        # so we make a copy to show equalized image
        img = self.parent.image.copy()

        histogram = compute_histogram(img, self.imageShape)
        accumulated_frequencies = np.zeros(256)

        for i in range(len(accumulated_frequencies)):
            if i == 0:
                accumulated_frequencies[i] = histogram[i]
            else:
                accumulated_frequencies[i] = histogram[i] + accumulated_frequencies[i-1]

        s_min = accumulated_frequencies[0]
        new_colors = np.zeros(256)

        for i in range(len(accumulated_frequencies)):
            # corresponds to formula
            # the ceil or floor of (sk-smin)*(L-1)/(1-smin)
            new_colors[i] = math.ceil(
                ((accumulated_frequencies[i]-s_min)*255)/(1-s_min)
            )
        
        new_colors = [int(x) for x in new_colors]
        
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            index = pixels[x,y]
            pixels[x,y] = new_colors[index]
        
        filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        img.save(f'{TRANSFORMATION_FOLDER}/{filename}_equalized.png')
        
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
            "Original Image",
            f"Equalized Image"
        ], cmap="gray")
