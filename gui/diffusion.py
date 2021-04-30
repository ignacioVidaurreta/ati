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
    TRANSFORMATION_FOLDER,
    get_shape
)
from PIL import Image

import numpy as np
from matrix_util import *

from utils import TRANSFORMATION_FOLDER, get_shape

#The biggest difference between istropic and anisotropic diffusion
#is how they interact with boundaries. Isotropic diffusion
#acts without knowledge of them, and thus smooths the image
#difuminating contrasting pixels. Meanwhile, the anisotropic
#will ONLY smooth within the boundaries, not though them
#the lambda chosen for the discretization is 0.25

class DiffusionTab(QWidget):

    
    def lorentzDetector(self, delta):
        sigma = float(self.sigma.text())
        return 1/(math.pow(delta/sigma,2) + 1)

    def leclercDetector(self, delta):
        sigma = float(self.sigma.text())
        return math.exp(-(math.pow(delta,2)))/(math.pow(sigma,2))

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = get_shape(self.image)

        self.iso_label= QLabel("Isotropic Filter")
        self.anis_label= QLabel("Anisotropic Filter")
        self.bi_label= QLabel("Bilateral Filter")
        self.iso_label.setStyleSheet("background-color: #FFDFD3")
        self.anis_label.setStyleSheet("background-color: #FFDFD3")
        self.bi_label.setStyleSheet("background-color: #FFDFD3")


        # Buttons definitions
        self.isotropic = newButton("Apply", self.onIsotropicClick)
        self.anisotropic = newButton("Apply", self.onAnisotropicClick)
        self.bilateral = newButton("Apply", self.onBilateralClick)

        #As t (time) augmentates, the smoothing effect increases
        self.iter_label = QLabel("Iterations")
        self.iter_label.setStyleSheet("background-color: #FFDFD3")
        self.t_label, self.t_input = QLabel("t Value:"), QLineEdit()
        self.sigma_label, self.sigma = QLabel("Sigma:"), QLineEdit()

        # Bilteral widgets
        self.size_label, self.size_input = QLabel("Window Size:"), QLineEdit()
        self.s_label, self.s_value = QLabel("Sigma S:"), QLineEdit()
        self.r_label, self.r_value = QLabel("Sigma R:"), QLineEdit()

        # We add widgets to layout

        self.layout.addWidget(self.iter_label, 1, 0)
        self.layout.addWidget(self.t_label, 1, 1)
        self.layout.addWidget(self.t_input, 1, 2)

        self.layout.addWidget(self.iso_label, 2, 0)
        self.layout.addWidget(self.isotropic, 2, 1)
        
        self.layout.addWidget(self.anis_label, 3, 0)
        self.layout.addWidget(self.sigma_label, 3, 1)
        self.layout.addWidget(self.sigma, 3, 2)
        self.layout.addWidget(self.anisotropic, 3, 3)
        
        self.layout.addWidget(self.bi_label, 4, 0)
        self.layout.addWidget(self.size_label, 4, 1)
        self.layout.addWidget(self.size_input, 4, 2)
        self.layout.addWidget(self.s_label, 4, 3)
        self.layout.addWidget(self.s_value, 4, 4)
        self.layout.addWidget(self.r_label, 4, 5)
        self.layout.addWidget(self.r_value, 4, 6)
        self.layout.addWidget(self.bilateral, 4, 7)



        self.setLayout(self.layout)

    def normalizeChannel(self, channel):
        maxval = np.amax(channel)
        minval = np.amin(channel)
        for x in range(self.imageShape[0]):
            for y in range(self.imageShape[1]):
                if(minval == 0 and maxval == 0):
                    channel[x,y] = 0
                else:
                    channel[x,y] = (channel[x,y] - minval)*255 / (maxval-minval)
        return channel

    def onIsotropicClick(self):
        img = np.copy(self.parent.changes[-1]).astype(np.float64)
        
        if(len(self.image.shape) == 3):
            r, g, b = img[0], img[1], img[2]
            rO = self.IsoChannel(r)
            rO = self.normalizeChannel(rO)
            gO = self.IsoChannel(g)
            gO = self.normalizeChannel(gO)
            bO = self.IsoChannel(b)
            bO = self.normalizeChannel(bO)

            img = (rO,gO,bO)

        else:
            img = self.IsoChannel(img)
            img = self.normalizeChannel(img)

        display_before_after(
            self.parent,
            img,
            f'Isotropic Diffusion: t=' + self.t_input.text()
        )

    def onAnisotropicClick(self):
        img = np.copy(self.parent.changes[-1]).astype(np.float64)

        if(len(self.image.shape) == 3):
            r, g, b = img[0], img[1], img[2]
            rO = self.AnisoChannel(r)
            rO = self.normalizeChannel(rO)
            gO = self.AnisoChannel(g)
            gO = self.normalizeChannel(gO)
            bO = self.AnisoChannel(b)
            bO = self.normalizeChannel(bO)

            img = (rO,gO,bO)
            
        else:
            img = self.AnisoChannel(img)
            img = self.normalizeChannel(img)

        display_before_after(
            self.parent,
            img,
            f'Anisotropic Diffusion: t=' + self.t_input.text() + ', sigma=' + self.sigma.text()
        )

    def AnisoChannel(self, img):
        img2 = np.copy(img).astype(np.float64)

        t_value = int(self.t_input.text())
        for i in range(t_value):
            for x in range(1, np.size(img,0) - 1):
                for y in range(1, np.size(img,1) -1):
                    right = img[x + 1, y] - img[x, y]
                    left = img[x - 1, y] - img[x, y]
                    up = img[x, y + 1] - img[x, y]
                    down = img[x, y - 1] - img[x, y]
                    img2[x,y] = img[x,y] + 0.25*(left*self.lorentzDetector(left) +
                    up*self.lorentzDetector(up) + 
                    down*self.lorentzDetector(down) + 
                    right*self.lorentzDetector(right))
            img = img2
        return img

    def IsoChannel(self, img):
        img2 = np.copy(img).astype(np.float64)

        t_value = int(self.t_input.text())
        for i in range(t_value):
            for x in range(1, np.size(img,0) - 1):
                for y in range(1, np.size(img,1) -1):
                    right = img[x + 1, y] - img[x, y]
                    left = img[x - 1, y] - img[x, y]
                    up = img[x, y + 1] - img[x, y]
                    down = img[x, y - 1] - img[x, y]
                    img2[x,y] = img[x,y] + 0.25*(left + up + down + left)
            img = img2
        return img
    
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
            img = (rO,gO,bO)

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
