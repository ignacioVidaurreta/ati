import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit

)
from display import hdisplay
from utils import newButton, compute_histogram
from PIL import Image
import numpy as np

class SaltPepperTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Buttons definitions
        self.saltpepper_noise = newButton("Salt and Pepper Noise", self.onSaltPepperClick)
        self.p0_label, self.p0_input = QLabel("p0:"), QLineEdit()
        self.p1_label, self.p1_input = QLabel("p1:"), QLineEdit()

        # We add widgets to layout
        self.layout.addWidget(self.p0_label, 1, 0)
        self.layout.addWidget(self.p0_input, 1, 1)
        self.layout.addWidget(self.p1_label, 1, 3)
        self.layout.addWidget(self.p1_input, 1, 4)
        self.layout.addWidget(self.saltpepper_noise, 2, 2)


        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onSaltPepperClick(self):
        print(f"P0: {self.p0_input.text()}; P1: {self.p1_input.text()}")
        img2 = self.image.copy()
        p0 = float(self.p0_input.text())
        p1 = float(self.p1_input.text())
        RGB = type(img2[0][0]) is tuple
        cmap = None
        if not RGB:
            cmap = "gray"
        rng = np.random.default_rng()

        for x in range(self.imageShape[0]):
            for y in range(self.imageShape[1]):
                rnd = rng.random()
                if (rnd < p0):
                    if(RGB):
                        img2[x,y] = (0,0,0)
                    else:
                        img2[x,y] = 0
                elif (rnd >= p1):
                    if(RGB):
                        img2[x,y] = (255,255,255)
                    else:
                        img2[x,y] = 255

        hdisplay([self.image, img2], rows=1, cols=2, titles=[
                "Original Image",
                "With Salt and Pepper, p0=" + self.p0_input.text() + ", p1=" +
                self.p1_input.text()

            ], cmap=cmap)

