import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,

)
from display import hdisplay
from utils import newButton, compute_histogram
from PIL import Image

# *** IMPORTANT
# This tab will be available only for black and white images
class HistogramTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Buttons definitions
        self.histogram = newButton("Histogram", self.onHistogramClick)

        # We add widgets to layout
        self.layout.addWidget(self.histogram, 1, 0)

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onHistogramClick(self):
        # Just in case we use a copy of the image
        img = self.parent.image.copy()

        histogram = compute_histogram(img, self.imageShape)

        # Plots histogram
        plt.figure()
        plt.bar(np.arange(len(histogram)), histogram)
        filename = self.parent.filename.split("/")[-1]
        plt.title(f'Histogram for {filename}')
        plt.show()
