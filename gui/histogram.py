import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,

)
from display import hdisplay
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
        self.equalize = newButton("Equalize", self.onEqualizeClick)

        # We add widgets to layout
        self.layout.addWidget(self.histogram, 1, 0)
        self.layout.addWidget(self.equalize, 2, 0)

        self.equalize.hide()

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onHistogramClick(self):
        # We do not want to loose original image
        img = self.parent.image.copy()
        pixels = img.load()

        # We initialize 256 bins in 0, this array will hold
        # relative frequencies
        histogram = np.zeros(256)

        # Computes relative frequencies
        for x,y in np.ndindex(img.size):
            current = histogram[pixels[x,y]]
            histogram[pixels[x,y]] = current + 1
        
        total = self.imageShape[0]*self.imageShape[1]
        histogram = histogram/total

        # Needed information for equalization
        self.histogram = histogram
        self.equalize.show()

        # Plots histogram
        plt.bar(np.arange(len(histogram)), histogram)
        filename = self.parent.filename.split("/")[-1]
        plt.title(f'Histogram for {filename}')
        plt.show()


    def onEqualizeClick(self):
        accumulated_frequencies = np.zeros(256)

        for i in range(len(accumulated_frequencies)):
            if i == 0:
                accumulated_frequencies[i] = self.histogram[i]
            else:
                accumulated_frequencies[i] = self.histogram[i] + accumulated_frequencies[i-1]

        s_min = accumulated_frequencies[0]
        new_colors = np.zeros(256)

        for i in range(len(accumulated_frequencies)):
            # corresponds to formula
            # the ceil or floor of (sk-smin)*(L-1)/(1-smin)
            new_colors[i] = math.ceil(
                ((accumulated_frequencies[i]-s_min)*255)/(1-s_min)
            )
        
        new_colors = [int(x) for x in new_colors]
        
        # We do not want to loose original image
        # so we make a copy to show equalized image
        img = self.parent.image.copy()
        pixels = img.load()
        for x,y in np.ndindex(img.size):
            index = pixels[x,y]
            pixels[x,y] = new_colors[index]
        
        filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        img.save(f'{filename}_equalized.png')
        
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
            "Original Image",
            f"Equalized Image"
        ], cmap="gray")


