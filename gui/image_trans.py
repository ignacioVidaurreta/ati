import cv2
import sys
import math
import numpy as np

from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QFormLayout,
    QLabel,
    QLineEdit

)
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from utils import newButton, newAxisButton
from PIL import Image
from display import hdisplay
from utils import (
    compute_accumulated_frequencies,
    compute_histogram,
    display_before_after,
    TRANSFORMATION_FOLDER,
    get_shape
)
import matplotlib.pyplot as plt


class ImageTransformTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = get_shape(self.image)

        self.negative_title = QLabel("Negative")
        self.negative_title.setStyleSheet("background-color: #FFD0ED")
        self.negative = newButton("Apply", self.onNegativeClick)

        self.umbralization_title = QLabel("Umbralization")
        self.umbralization_title.setStyleSheet("background-color: #FFD0ED")
        self.umbralLabel = QLabel("Umbral")
        self.umbralInput = QLineEdit()
        self.umbralInput.setText('255')
        self.umbralization = newButton("Apply", self.onUmbralizationClick)
        self.globalUmbral = newButton("Global", self.onGlobalUmbralClick)
        if len(self.imageShape) < 3:
            self.otsuUmbral = newButton("Otsu", self.onOtsuUmbralClick)

        self.gamma_title = QLabel("Power Function")
        self.gamma_title.setStyleSheet("background-color: #FFD0ED")
        self.gamma = newButton("Apply", self.onGammaClick)
        self.gammaLabel = QLabel("Gamma")
        self.gammaInput = QLineEdit()
        self.gammaInfo = QLabel("0 < \u03B3 < 2, \u03B3 != 1")
        self.gammaInput.setText('0.1')

        self.equalize_title = QLabel("Equalization")
        self.equalize_title.setStyleSheet("background-color: #FFD0ED")
        self.equalize = newButton("Apply", self.onEqualizeClick)

        # We add widgets to layout for each transformation
        self.layout.addWidget(self.negative_title, 0, 0)
        self.layout.addWidget(self.negative, 0, 1)

        self.layout.addWidget(self.umbralization_title, 1, 0)
        self.layout.addWidget(self.umbralLabel, 1, 1)
        self.layout.addWidget(self.umbralInput, 1, 2)
        self.layout.addWidget(self.umbralization, 1, 3)
        self.layout.addWidget(self.globalUmbral, 1, 4)
        if len(self.imageShape) < 3:
            self.layout.addWidget(self.otsuUmbral, 1, 5)

        self.layout.addWidget(self.gamma_title, 2, 0)
        self.layout.addWidget(self.gammaLabel, 2, 1)
        self.layout.addWidget(self.gammaInput, 2, 2)
        self.layout.addWidget(self.gammaInfo, 2, 3)
        self.layout.addWidget(self.gamma, 2, 4)

        # # Just for B&w images
        if len(self.imageShape) != 3:
            self.layout.addWidget(self.equalize_title, 3, 0)
            self.layout.addWidget(self.equalize, 3, 1)

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onNegativeClick(self):
        image = np.copy(self.parent.changes[-1])

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            r_result = self.negativeTransform(r)
            g_result = self.negativeTransform(g)
            b_result = self.negativeTransform(b)

            np_img = (r_result, g_result, b_result)
        else:
            np_img = self.negativeTransform(image)

        display_before_after(
            self.parent,
            np_img,
            "Negative Transformation of Image"
        )

    def negativeTransform(self, image):
        for x,y in np.ndindex(image.shape):
            image[x,y] = 255 - image[x,y]
        return image

    def onUmbralizationClick(self):
        self.umbralValue = int(self.umbralInput.text())

        image = np.copy(self.parent.changes[-1])

        if len(self.image.shape) == 3:

            # we umbralize every channel
            r,g,b = image[0], image[1], image[2]

            self.umbralizationTransform(r, self.umbralValue)
            self.umbralizationTransform(g, self.umbralValue)
            self.umbralizationTransform(b, self.umbralValue)

            # We now need to merge the modified values into an RGB image
            np_img = (r, g, b)

        else:
            self.umbralizationTransform(image, self.umbralValue)
            np_img = image

        display_before_after(
            self.parent,
            np_img,
            "Umbralization of Image"
        )

    def umbralizationTransform(self, image, umbral):
        for x,y in np.ndindex(image.shape):
            if image[x,y] < umbral:
                image[x,y] = 0
            else:
                image[x,y] = 255

    def onGammaClick(self):
        self.gammaValue = float(self.gammaInput.text())

        # We do not want to loose original image
        image = np.copy(self.parent.changes[-1])

        # We want to apply T(r) = c * r ^ gamma
        # where c = (L-1)^(1-gamma)
        self.c = 255 ** (1-self.gammaValue)

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            self.gammaTransform(r)
            self.gammaTransform(g)
            self.gammaTransform(b)

            np_img = (r,g,b)
        else:
            self.gammaTransform(image)
            np_img = image

        display_before_after(
            self.parent,
            np_img,
            f"Power function with \u03B3={self.gammaValue}"
        )

    def gammaTransform(self, image):
        for x,y in np.ndindex(image.shape):
            pixel = image[x,y]
            image[x,y] = int(
                math.ceil(
                    self.c*(pixel ** self.gammaValue)
                )
            )

    def onEqualizeClick(self):
        image = np.copy(self.parent.changes[-1])

        histogram = compute_histogram(image)
        accumulated_frequencies = compute_accumulated_frequencies(histogram)

        s_min = accumulated_frequencies[0]
        new_colors = np.zeros(256)

        for i in range(len(accumulated_frequencies)):
            # corresponds to formula
            # the ceil or floor of (sk-smin)*(L-1)/(1-smin)
            new_colors[i] = math.ceil(
                ((accumulated_frequencies[i]-s_min)*255)/(1-s_min)
            )

        new_colors = [int(x) for x in new_colors]

        for x,y in np.ndindex(image.shape):
            index = image[x,y]
            image[x,y] = new_colors[index]

        display_before_after(
            self.parent,
            image,
            "Equalized Image"
        )

    def globalUmbralAlgorithm(self, original):
        # step 1
        current_t = 100 # this was randomly selected
        current = None

        iterations = 0

        while True:
            current = np.copy(original)

            iterations += 1

            # step 2
            self.umbralizationTransform(current, current_t)

            # step 3, 4
            # n stands for quantity, m for mean
            n_g0 = 0
            n_g255 = 0
            m_g0 = 0
            m_g255 = 0

            for x,y in np.ndindex(original.shape):
                if current[x,y] == 0:
                    m_g0 += original[x,y]
                    n_g0 += 1
                else:
                    m_g255 += original[x,y]
                    n_g255 += 1

            m_g0 *= (1/n_g0)
            m_g255 *= (1/n_g255)

            # step 5
            new_t = math.floor(0.5*(m_g0 + m_g255))

            # step 6
            if abs(current_t-new_t) < 1: break

            current_t = new_t

        return current, current_t, iterations

    def onGlobalUmbralClick(self):
        # this image is NOT modified
        image = self.parent.changes[-1]

        if len(self.image.shape) == 3:

            # we umbralize every channel
            r,g,b = image[0], image[1], image[2]

            current_r, t_r, it_r = self.globalUmbralAlgorithm(r)
            current_g, t_g, it_g = self.globalUmbralAlgorithm(g)
            current_b, t_b, it_b = self.globalUmbralAlgorithm(b)

            # We now need to merge the modified values into an RGB image
            np_img = (current_r, current_g, current_b)

            display_before_after(
                self.parent,
                np_img,
                f"t:{t_r},{t_g},{t_b}, iter:{it_r},{it_g},{it_b}"
            )

        else:
            current, current_t, iterations = self.globalUmbralAlgorithm(image)

            display_before_after(
                self.parent,
                current,
                f"Global Umbral t:{current_t}, iter:{iterations}"
            )


    def onOtsuUmbralClick(self):
        image = np.copy(self.parent.changes[-1])

        histogram = compute_histogram(image)

        umbral = -1
        max_val = -1

        for t in range(len(histogram)):
            prob_c1 = np.sum(histogram[:t])
            prob_c2 = np.sum(histogram[t:])

            mean_c1 = np.mean(histogram[:t])
            mean_c2 = np.mean(histogram[t:])

            # we want to maxim. this in order to find proper t
            value = prob_c1 * prob_c2 * (mean_c1 - mean_c2) ** 2

            if value > max_val:
                umbral = t
                max_val = value

        self.umbralizationTransform(image, umbral)

        display_before_after(
            self.parent,
            image,
            f"Otsu Umbral with t:{umbral}"
        )
