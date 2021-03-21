import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,

)
from utils import newButton
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
        # We do not want to loose original image
        img = self.parent.image.copy()
        pixels = img.load()

        # We initialize 256 bins in 0, this array will hold
        # relative frequencies
        histogram = np.zeros(256)

        for x,y in np.ndindex(img.size):
            current = histogram[pixels[x,y]]
            histogram[pixels[x,y]] = current + 1

        # Plots histogram
        plt.bar(np.arange(len(histogram)), histogram)
        filename = self.parent.filename.split("/")[-1]
        plt.title(f'Histogram for {filename}')
        plt.show()
