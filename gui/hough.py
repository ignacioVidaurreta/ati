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

#Antes de pasar por Hough, la imagen debe ser umbralizada porque
#utiliza imagenes binarias (B&W)

#Ecuacion de recta: x*cos(theta) + y*sin(theta) = rho
#Si la diferencia entre rho y la recta es menor a epsilon ==> 
#Sumo en el acumulador
#Ganan los mas votados

class HoughTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = get_shape(self.image)

        self.sq_label= QLabel("Hough Square")
        self.cir_label= QLabel("Hough Circle")
        self.sq_label.setStyleSheet("background-color: #9DABDD")
        self.cir_label.setStyleSheet("background-color: #9DABDD")

        # Buttons definitions
        self.square = newButton("Apply", self.onHoughSquare)
        self.circle = newButton("Apply", self.onHoughCircle)

        # Bilteral widgets
        self.M_label, self.M_input = QLabel("Theta/A Values:"), QLineEdit()
        self.N_label, self.N_input = QLabel("Rho/B Values:"), QLineEdit()
        self.W_label, self.W_input = QLabel("Winners:"), QLineEdit()
        self.E_label, self.E_input = QLabel("Epsilon:"), QLineEdit()
        self.R_label, self.R_input = QLabel("Radius Values:"), QLineEdit()
        self.Rmin_label, self.Rmin_input = QLabel("Radius Min:"), QLineEdit()
        self.Rmax_label, self.Rmax_input = QLabel("Radius Max:"), QLineEdit()

        # We add widgets to layout
        self.layout.addWidget(self.M_label, 0, 0)
        self.layout.addWidget(self.M_input, 0, 1)
        self.layout.addWidget(self.N_label, 0, 2)
        self.layout.addWidget(self.N_input, 0, 3)

        self.layout.addWidget(self.W_label, 1, 0)
        self.layout.addWidget(self.W_input, 1, 1)
        self.layout.addWidget(self.R_label, 1, 2)
        self.layout.addWidget(self.R_input, 1, 3)

        self.layout.addWidget(self.Rmin_label, 2, 0)
        self.layout.addWidget(self.Rmin_input, 2, 1)
        self.layout.addWidget(self.Rmax_label, 2, 2)
        self.layout.addWidget(self.Rmax_input, 2, 3)

        self.layout.addWidget(self.E_label, 3,1)
        self.layout.addWidget(self.E_input, 3,2)

        self.layout.addWidget(self.sq_label, 4, 0)
        self.layout.addWidget(self.square, 4, 1)
        self.layout.addWidget(self.cir_label, 4, 2)
        self.layout.addWidget(self.circle, 4, 3)

        self.setLayout(self.layout)

    def onHoughSquare(self):
        epsilon = float(self.E_input.text())

        M = int(self.M_input.text())
        N = int(self.N_input.text())
        W = int(self.W_input.text())

        D = max(self.image.shape)

        thetas = np.linspace(-90, 90, M)
        rhos = np.linspace(-math.sqrt(2)*D, math.sqrt(2)*D, N)

        accumulator = []

        white_matrix = self.getWhitePixelsOnly()

        for t in thetas:
            rad = np.deg2rad(t)
            for r in rhos:
                value = 0
                for cords in white_matrix:
                    if(abs(r - cords[0]*math.cos(rad) - cords[1]*math.sin(rad)) < epsilon):
                        value += 1
                accumulator.append([rad,r,value])

        accumulator.sort(key=lambda x: x[2], reverse=True)

        self.drawAccumulatorSquare(accumulator[:W])

    def drawAccumulatorSquare(self, winners):
        fig, ax = plt.subplots()
        print(winners)
        print(self.image.shape)
        for w in winners:
            x = []
            y = []

            if math.sin(w[0]) !=0 and math.cos(w[0]) != 0:
                y = np.linspace(0, self.image.shape[1])
                x = (w[1] - y*math.cos(w[0]))/math.sin(w[0])
            elif math.sin(w[0]) == 0:
                x = np.linspace(0, self.image.shape[0])
                y = np.full(x.size, fill_value=w[1])
            else:
                x = np.linspace(0, self.image.shape[1])
                y = np.full(x.size, fill_value=w[1])

            ax.plot(x,y)
        ax.imshow(self.parent.changes[-1], cmap='gray')
        fig.show()

    def onHoughCircle(self):
        epsilon = float(self.E_input.text())

        M = int(self.M_input.text())
        N = int(self.N_input.text())
        W = int(self.W_input.text())
        R = int(self.R_input.text())
        Rmin = int(self.Rmin_input.text())
        Rmax = int(self.Rmax_input.text())

        As = np.linspace(Rmin, self.image.shape[0] - Rmin, M)
        Bs = np.linspace(Rmin, self.image.shape[1] - Rmin, N)
        Rs = np.linspace(Rmin, Rmax, R)

        accumulator = []

        white_matrix = self.getWhitePixelsOnly()

        for a in As:
            for b in Bs:
                for r in Rs:
                    value = 0
                    for cords in white_matrix:
                        if(abs(r**2 - (cords[0]-a)**2 - (cords[1]-b)**2) < epsilon):
                            value += 1
                    accumulator.append([a,b,r,value])

        accumulator.sort(key=lambda x: x[3], reverse=True)

        self.drawAccumulatorCircle(accumulator[:W])

    def drawAccumulatorCircle(self, winners):
        fig, ax = plt.subplots()
        print(winners)
        for w in winners:
            ax.add_artist(plt.Circle((w[1], w[0]), w[2], color='r', fill=False))
        ax.imshow(self.parent.changes[-1], cmap='gray')
        fig.show()

    def getWhitePixelsOnly(self):
        white_matrix = []
        img = self.parent.changes[-1]

        if(len(self.image.shape) == 3):
            for x,y in np.ndindex(self.image.shape):
                if(img[0][x,y] == 255 and img[1][x,y] == 255
                    and img[2][x,y]):
                    white_matrix.append([x,y])
        else:
            for x,y in np.ndindex(self.image.shape):
                if(img[x,y] == 255):
                    white_matrix.append([x,y])
        return white_matrix





