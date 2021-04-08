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
from utils import compute_histogram, TRANSFORMATION_FOLDER
import matplotlib.pyplot as plt


class ImageTransformTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        self.negative_title = QLabel("Negative")
        self.negative_title.setStyleSheet("background-color: #FFD0ED")
        self.negative = newButton("Apply", self.onNegativeClick)

        self.umbralization_title = QLabel("Umbralization")
        self.umbralization_title.setStyleSheet("background-color: #FFD0ED")
        self.umbralLabel = QLabel("Umbral")
        self.umbralInput = QLineEdit()
        self.umbralInput.setText('255')
        self.umbralization = newButton("Apply", self.onUmbralizationClick)

        self.gamma_title = QLabel("Power Function")
        self.gamma_title.setStyleSheet("background-color: #FFD0ED")
        self.gamma = newButton("Apply", self.onGammaClick)
        self.gammaLabel = QLabel("Gamma")
        self.gammaInput = QLineEdit()
        self.gammaInfo = QLabel("0 < \u03B3 < 2, \u03B3 != 1")
        self.gammaInput.setText('0.1')

        self.equalize_title = QLabel("Equalization")
        self.equalize_title.setStyleSheet("background-color: #FFD0ED")
        self.equalize = newButton("Apply", self.onEqualizeClick)
        
        # We add widgets to layout for each transformation
        self.layout.addWidget(self.negative_title, 0, 0)
        self.layout.addWidget(self.negative, 0, 1)

        self.layout.addWidget(self.umbralization_title, 1, 0)
        self.layout.addWidget(self.umbralLabel, 1, 1)
        self.layout.addWidget(self.umbralInput, 1, 2)
        self.layout.addWidget(self.umbralization, 1, 3)

        self.layout.addWidget(self.gamma_title, 2, 0)
        self.layout.addWidget(self.gammaLabel, 2, 1)
        self.layout.addWidget(self.gammaInput, 2, 2)
        self.layout.addWidget(self.gammaInfo, 2, 3)
        self.layout.addWidget(self.gamma, 2, 4)

        # Just for B&w images
        if len(self.imageShape) != 3:
            self.layout.addWidget(self.equalize_title, 3, 0)
            self.layout.addWidget(self.equalize, 3, 1)

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

        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_negative.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

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

        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_umbral_{str(self.umbralValue)}.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

    def umbralizationTransform(self, img):
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            if pixels[x,y] < self.umbralValue:
                pixels[x,y] = 0
            else:
                pixels[x,y] = 255

    def onGammaClick(self):
        self.gammaValue = float(self.gammaInput.text())

        # We do not want to loose original image
        img = self.parent.image.copy()

        # We want to apply T(r) = c * r ^ gamma
        # where c = (L-1)^(1-gamma)
        self.c = 255 ** (1-self.gammaValue)

        if len(self.imageShape) == 3:
            # if image has r,g,b channels, apply the transform
            # to every channel
            r,g,b = img.split()
            self.gammaTransform(r)
            self.gammaTransform(g)
            self.gammaTransform(b)

            img = Image.merge("RGB", (r,g,b))

            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Power function with \u03B3={self.gammaValue}"
            ])

        else:
            self.gammaTransform(img)

            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Power function with \u03B3={self.gammaValue}"
            ], cmap="gray")

        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_power_{str(self.gammaValue)}.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

    def gammaTransform(self, img):
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            pixel = pixels[x,y]
            pixels[x,y] = int(
                math.ceil(
                    self.c*(pixel ** self.gammaValue)
                )
            )

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

        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_equalized.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
            "Original Image",
            f"Equalized Image"
        ], cmap="gray")

        plt.figure()
        histogram = compute_histogram(img, self.imageShape)
        plt.bar(np.arange(len(histogram)), histogram)
        filename = self.parent.filename.split("/")[-1]
        plt.title(f'Equalized histogram for {filename}')
        plt.show()