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

        self.image = np.asarray(self.parent.image).copy()
        self.imageShape = self.image.shape

        # Buttons definitions
        self.isotropic = newButton("Isotropic Diffusion", self.onIsotropicClick)
        self.anisotropic = newButton("Anisotropic Diffusion", self.onAnisotropicClick)

        #As t (time) augmentates, the smoothing effect increases
        self.t_label, self.t_input = QLabel("t Value:"), QLineEdit()
        self.sigma_label, self.sigma = QLabel("Sigma:"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.t_label, 1, 1)
        self.layout.addWidget(self.t_input, 1, 2)

        self.layout.addWidget(self.isotropic, 2, 1)
        self.layout.addWidget(self.anisotropic, 3, 1)

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

    def normalizeAllChannels(self):
        rI, gI, bI = self.image[:,:,0], self.image[:,:,1], self.image[:,:,2]
        rO = self.normalizeChannel(rI)
        gO = self.normalizeChannel(gI)
        bO = self.normalizeChannel(bI)

        imgO = np.dstack((rO,gO,bO))
        return imgO

    def onIsotropicClick(self):
        img = np.asarray(self.parent.image).copy()
        t_value = int(self.t_input.text())

        cmap = "gray"
        RGB = False

        if(type(img[0][0]) is tuple or type(img[0][0]) is np.ndarray):
            cmap = None
            RGB = True
            
        for i in range(t_value):
            for x in range(1, self.imageShape[0] - 1):
                for y in range(1, self.imageShape[1] -1):
                    right = self.image[x + 1, y] - self.image[x, y]
                    left = self.image[x - 1, y] - self.image[x, y]
                    up = self.image[x, y + 1] - self.image[x, y]
                    down = self.image[x, y - 1] - self.image[x, y]
                    img[x,y] = self.image[x,y] + (up + down + left + right)*0.25
            self.image = img

        if not RGB:
            img = self.normalizeChannel(self.image)
        else:
            img = self.normalizeAllChannels()

        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                "Isotropic Diffusion, t=" + self.t_input.text()

            ], cmap=cmap)

        self.parent.changes.append(self.parent.image)
        self.parent.image = Image.fromarray(img)
        self.parent.buttonUndo.setEnabled(True)

    def onAnisotropicClick(self):
        img = np.asarray(self.parent.image).copy()
        t_value = int(self.t_input.text())

        cmap = "gray"
        RGB = False

        if(type(img[0][0]) is tuple or type(img[0][0]) is np.ndarray):
            cmap = None
            RGB = True

        for i in range(t_value):
            for x in range(1, self.imageShape[0] - 1):
                for y in range(1, self.imageShape[1] -1):
                    right = self.image[x + 1, y] - self.image[x, y]
                    left = self.image[x - 1, y] - self.image[x, y]
                    up = self.image[x, y + 1] - self.image[x, y]
                    down = self.image[x, y - 1] - self.image[x, y]
                    img[x,y] = self.image[x,y] + 0.25*(left*self.lorentzDetector(left, RGB) +
                    up*self.lorentzDetector(up, RGB) + 
                    down*self.lorentzDetector(down, RGB) + 
                    right*self.lorentzDetector(right, RGB))
            self.image = img

        if not RGB:
            img = self.normalizeChannel(self.image)
        else:
            img = self.normalizeAllChannels()

        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                "Anisotropic Diffusion, t=" + self.t_input.text() + ", sigma=" + self.sigma.text()

            ], cmap=cmap)

        self.parent.changes.append(self.parent.image)
        self.parent.image = Image.fromarray(img)
        self.parent.buttonUndo.setEnabled(True)
