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

class NoiseTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Buttons definitions
        self.gaussian_noise = newButton("Gaussian Noise", self.onGaussianClick)
        self.mu_label, self.mu_input = QLabel("Gaussian Mu"), QLineEdit()
        self.sigma_label, self.sigma_input = QLabel("Gaussian Sigma"), QLineEdit()

        self.rayleigh_btn = newButton("Rayleigh Noise", self.onRayleighClick)
        self.psi_label, self.psi_input = QLabel("Rayleigh Param"), QLineEdit()

        self.exponential = newButton("Exponential Noise", self.onExponentialClick)
        self.lambda_label, self.lambda_input = QLabel("Lambda Param"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.mu_label, 1, 0)
        self.layout.addWidget(self.mu_input, 1, 1)
        self.layout.addWidget(self.sigma_label, 1, 2)
        self.layout.addWidget(self.sigma_input, 1, 3)
        self.layout.addWidget(self.gaussian_noise, 2, 0)

        self.layout.addWidget(self.psi_label, 3, 0)
        self.layout.addWidget(self.psi_input, 3, 1)
        self.layout.addWidget(self.rayleigh_btn, 3, 2)

        self.layout.addWidget(self.lambda_label, 4, 0)
        self.layout.addWidget(self.lambda_input, 4, 1)
        self.layout.addWidget(self.exponential, 4, 2)


        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onGaussianClick(self):
        print(f"SIGMA: {self.sigma_input.text()}; MU: {self.mu_input.text()}")
        rng = np.random.default_rng()
        sigma = float(self.sigma_input.text())
        mu = float(self.mu_input.text())
        print(f"GAUSSIAN RAND: {rng.normal(sigma, mu)}")

    def onRayleighClick(self):
        rng = np.random.default_rng()
        psi = float(self.psi_input.text())
        print(f"RAYLEIGH {rng.rayleigh(psi)}")

    def onExponentialClick(self):
        rng = np.random.default_rng()
        lambda_param = float(self.lambda_input.text())
        # Exponential receives Beta which is 1/lambda
        print(f"EXPONENTIAL: {rng.exponential(1/lambda_param)}")