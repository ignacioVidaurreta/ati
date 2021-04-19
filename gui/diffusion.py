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

#The biggest difference between istropic and anisotropic diffusion
#is how they interact with boundaries. Isotropic diffusion
#acts without knowledge of them, and thus smooths the image
#difuminating contrasting pixels. Meanwhile, the anisotropic
#will ONLY smooth within the boundaries, not though them

class DiffusionTab(QWidget):

    
    def lorentzDetector(self, delta, RGB):
        sigma = float(self.sigma.text())
        if(RGB):
            r = 1/(math.pow(delta[0]/sigma,2) + 1)
            g = 1/(math.pow(delta[1]/sigma,2) + 1)
            b = 1/(math.pow(delta[2]/sigma,2) + 1)
            return [r,g,b]
        return 1/(math.pow(delta/sigma,2) + 1)

    def leclercDetector(self, delta):
        sigma = float(self.sigma.text())
        return math.exp(-(math.pow(delta,2)))/(math.pow(sigma,2))

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = self.parent.changes[-1]
        self.imageShape = self.image.shape

        self.iso_label= QLabel("Isotropic Diffusion")
        self.anis_label= QLabel("Anisotropic Diffusion")
        self.iso_label.setStyleSheet("background-color: #FFDFD3")
        self.anis_label.setStyleSheet("background-color: #FFDFD3")


        # Buttons definitions
        self.isotropic = newButton("Apply", self.onIsotropicClick)
        self.anisotropic = newButton("Apply", self.onAnisotropicClick)

        #As t (time) augmentates, the smoothing effect increases
        self.t_label, self.t_input = QLabel("t Value:"), QLineEdit()
        self.sigma_label, self.sigma = QLabel("Sigma:"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.t_label, 1, 2)
        self.layout.addWidget(self.t_input, 1, 3)

        self.layout.addWidget(self.iso_label, 2, 1)
        self.layout.addWidget(self.anis_label, 3, 1)

        self.layout.addWidget(self.isotropic, 2, 2)
        self.layout.addWidget(self.anisotropic, 3, 4)

        self.layout.addWidget(self.sigma_label, 3, 2)
        self.layout.addWidget(self.sigma, 3, 3)


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

    def normalizeAllChannels(self, img):
        rI, gI, bI = img[:,:,0], img[:,:,1], img[:,:,2]
        rO = self.normalizeChannel(rI)
        gO = self.normalizeChannel(gI)
        bO = self.normalizeChannel(bI)

        imgO = np.dstack((rO,gO,bO))
        return imgO

    def onIsotropicClick(self):
        img = self.parent.changes[-1].copy()
        img2 = self.parent.changes[-1].copy()
        t_value = int(self.t_input.text())

        cmap = "gray"
        RGB = False

        if(type(img[0][0]) is tuple or type(img[0][0]) is np.ndarray):
            cmap = None
            RGB = True
            
        for i in range(t_value):
            for x in range(1, self.imageShape[0] - 1):
                for y in range(1, self.imageShape[1] -1):
                    right = img[x + 1, y] - img[x, y]
                    left = img[x - 1, y] - img[x, y]
                    up = img[x, y + 1] - img[x, y]
                    down = img[x, y - 1] - img[x, y]
                    img2[x,y] = img[x,y] + (up + down + left + right)*0.25
            img = img2

        if not RGB:
            img = self.normalizeChannel(img)
        else:
            img = self.normalizeAllChannels(img)

        display_before_after(
            self.parent,
            img,
            f'Isotropic Diffusion: t=' + self.t_input.text()
        )

    def onAnisotropicClick(self):
        img = self.parent.changes[-1].copy()
        img2 = self.parent.changes[-1].copy()
        t_value = int(self.t_input.text())

        cmap = "gray"
        RGB = False

        if(type(img[0][0]) is tuple or type(img[0][0]) is np.ndarray):
            cmap = None
            RGB = True

        for i in range(t_value):
            for x in range(1, self.imageShape[0] - 1):
                for y in range(1, self.imageShape[1] -1):
                    right = img[x + 1, y] - img[x, y]
                    left = img[x - 1, y] - img[x, y]
                    up = img[x, y + 1] - img[x, y]
                    down = img[x, y - 1] - img[x, y]
                    img2[x,y] = img[x,y] + 0.25*(left*self.lorentzDetector(left, RGB) +
                    up*self.lorentzDetector(up, RGB) + 
                    down*self.lorentzDetector(down, RGB) + 
                    right*self.lorentzDetector(right, RGB))
            img = img2

        if not RGB:
            img = self.normalizeChannel(img)
        else:
            img = self.normalizeAllChannels(img)


        display_before_after(
            self.parent,
            img,
            f'Anisotropic Diffusion: t=' + self.t_input.text() + ', sigma=' + self.sigma.text()
        )
