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
from utils import (
    newButton,
    display_before_after,
    numpy_to_pil_image,
    TRANSFORMATION_FOLDER
)
from PIL import Image

import numpy as np
from matrix_util import *

from utils import TRANSFORMATION_FOLDER

#S sigma affects space, R sigma affects colour

class BilateralTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        self.bi_label= QLabel("Bilateral Filter")
        self.bi_label.setStyleSheet("background-color: #F6F6EB")


        # Buttons definitions
        self.bilateral = newButton("Apply", self.onBilateralClick)

        self.size_label, self.size_input = QLabel("Window Size:"), QLineEdit()
        self.s_label, self.s_value = QLabel("Sigma S:"), QLineEdit()
        self.r_label, self.r_value = QLabel("Sigma R:"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.size_label, 1, 2)
        self.layout.addWidget(self.size_input, 1, 3)

        self.layout.addWidget(self.s_label, 2, 1)
        self.layout.addWidget(self.s_value, 2, 2)

        self.layout.addWidget(self.r_label, 2, 3)
        self.layout.addWidget(self.r_value, 2, 4)

        self.layout.addWidget(self.bi_label, 3, 2)
        self.layout.addWidget(self.bilateral, 3, 3)


        self.setLayout(self.layout)

    def normalizeChannel(self, channel):
        maxval = np.amax(channel)
        minval = np.amin(channel)
        for x in range(self.imageShape[0]):
            for y in range(self.imageShape[1]):
                if(minval == 0 and maxval == 0):
                    channel[x,y] = 0
                else:
                    channel[x,y] = round((channel[x,y] - minval)*255 / (maxval-minval))
        return channel

    def onBilateralClick(self):
        img = np.copy(self.parent.changes[-1])

        if(len(self.image.shape) == 3):
            r, g, b = img[0], img[1], img[2]

            rO = self.bilateralBW(r)
            gO = self.bilateralBW(g)
            bO = self.bilateralBW(b)
            img = np.dstack((rO,gO,bO))

        else:
            img = self.bilateralBW(img)

        display_before_after(
            self.parent,
            img,
            f'Bilateral Filter: Window=' + self.size_input.text() + "x" + self.size_input.text() +
             ', Sigma S=' + self.s_value.text() + ", Sigma R=" + self.r_value.text()
        )

    def bilateralBW(self, img):
        s = int(self.s_value.text())
        r = int(self.r_value.text())
        size = int(self.size_input.text())

        img2 = np.copy(img).astype(np.float64)

        for x in range(size, np.size(img,0) - size):
            for y in range(size, np.size(img,1) - size):
                total = 0
                value = 0
                for i in range(-size,size):
                    for j in range(-size, size):
                        weight = math.exp(-((i**2 + j**2)/(2*s**2)) - ((img2[x,y] - img2[x+i,y+j])**2/(2*r**2)))
                        total+= weight
                        value += img2[x+i,y+j]*weight
                img[x,y] = value/total
        return img        







        

        