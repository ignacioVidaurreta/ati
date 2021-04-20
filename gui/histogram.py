import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel
)
from display import hdisplay
from utils import newButton, compute_histogram
from PIL import Image

from utils import get_shape

# *** IMPORTANT
# This tab will be available only for black and white images
class HistogramTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = get_shape(self.image)

        # Buttons definitions
        self.histogram_title = QLabel('')
        self.histogram_title.setAlignment(QtCore.Qt.AlignCenter)
        self.histogram_description = QLabel("Computes relative frequencies for image\'s greys")
        self.histogram_description.setAlignment(QtCore.Qt.AlignCenter)
        self.histogram = newButton("Plot", self.onHistogramClick)
        self.histogram.setFixedWidth(300)
        self.dummy = QLabel("")

        # We add widgets to layout
        self.layout.addWidget(self.histogram_title, 0, 0)
        self.layout.addWidget(self.histogram_description, 1, 0)
        self.layout.addWidget(self.histogram, 2, 0)
        self.layout.addWidget(self.dummy, 3, 0)


        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onHistogramClick(self):
        image = self.parent.changes[-1]

        histogram = compute_histogram(image)

        # Plots histogram
        plt.figure()
        plt.bar(np.arange(len(histogram)), histogram)
        filename = self.parent.filename.split("/")[-1]
        plt.title(f'Histogram for {filename}')
        plt.show()
