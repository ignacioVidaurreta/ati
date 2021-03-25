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
from utils import newButton, compute_histogram, TRANSFORMATION_FOLDER
from PIL import Image
import numpy as np
from matrix_util import matrix_mult, matrix_sum

class NoiseTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        self.noise_ptg_label, self.noise_ptg_input = QLabel("Noice Percentage"), QLineEdit()

        # Buttons definitions
        self.gaussian_noise = newButton("Gaussian Noise", self.onGaussianClick)
        self.mu_label, self.mu_input = QLabel("Gaussian Mu"), QLineEdit()
        self.sigma_label, self.sigma_input = QLabel("Gaussian Sigma"), QLineEdit()

        self.rayleigh_btn = newButton("Rayleigh Noise", self.onRayleighClick)
        self.psi_label, self.psi_input = QLabel("Rayleigh Param"), QLineEdit()

        self.exponential = newButton("Exponential Noise", self.onExponentialClick)
        self.lambda_label, self.lambda_input = QLabel("Lambda Param"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.noise_ptg_label, 1, 0)
        self.layout.addWidget(self.noise_ptg_input, 1, 1)

        self.layout.addWidget(self.mu_label, 2, 0)
        self.layout.addWidget(self.mu_input, 2, 1)
        self.layout.addWidget(self.sigma_label, 2, 2)
        self.layout.addWidget(self.sigma_input, 2, 3)
        self.layout.addWidget(self.gaussian_noise, 3, 0)

        self.layout.addWidget(self.psi_label, 4, 0)
        self.layout.addWidget(self.psi_input, 4, 1)
        self.layout.addWidget(self.rayleigh_btn, 4, 2)

        self.layout.addWidget(self.lambda_label, 5, 0)
        self.layout.addWidget(self.lambda_input, 5, 1)
        self.layout.addWidget(self.exponential, 5, 2)


        self.setLayout(self.layout)

    def generate_noise_mat(self, rng, full_noise, is_mult):
        replace_rate = float(self.noise_ptg_input.text()) / 100
        if replace_rate == 1:
            return full_noise

        mask = np.random.choice([0,1], size=full_noise.shape, p=((1-replace_rate), replace_rate)).astype(np.bool)
        if is_mult:
            neut = np.ones(full_noise.shape)
        else:
            neut = np.zeros(full_noise.shape)

        neut[mask] = full_noise[mask]
        return neut


    # Convention: on[ButtonName]Click
    def onGaussianClick(self):
        print(f"SIGMA: {self.sigma_input.text()}; MU: {self.mu_input.text()}")
        rng = np.random.default_rng()
        sigma = float(self.sigma_input.text())
        mu = float(self.mu_input.text()) # Should usually be zero

        shape = self.image.shape
        noise = self.generate_noise_mat(rng, rng.normal(sigma, mu, shape).astype(int), False)
        img = Image.fromarray(matrix_sum(self.image, noise))

        cmap = "gray" if len(shape) == 2 else None

        print(f"CMAP: {cmap}\n LEN: {len(shape)}")
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Image with added noise (σ: {self.sigma_input.text()} µ: {self.mu_input.text()})"
            ], cmap=cmap)

        # filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        # img.save(f'{TRANSFORMATION_FOLDER}/{filename}_gaussNoise_mu{mu}_sigma{sigma}.png')


    def onRayleighClick(self):
        rng = np.random.default_rng()
        psi = float(self.psi_input.text()) # Hay que ponerle un psi grande, tipo 30 para ver el ruido
        print(f"RAYLEIGH {rng.rayleigh(psi)}")
        shape = self.image.shape
        # import ipdb; ipdb.set_trace()
        ray = np.random.rayleigh(psi, shape).astype(int)
        # We want to replace zeros to 1
        noise = self.generate_noise_mat(rng, np.where(ray == 0, 1, ray), True)
        img = Image.fromarray(matrix_mult(self.image, noise))

        cmap = "gray" if len(shape) == 2 else None

        print(f"CMAP: {cmap}\n LEN: {len(shape)}")
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Image with added noise (ψ: {psi})"
            ], cmap=cmap)

    def onExponentialClick(self):
        rng = np.random.default_rng()
        lambda_param = float(self.lambda_input.text())
        # Exponential receives Beta which is 1/lambda
        print(f"EXPONENTIAL: {rng.exponential(1/lambda_param)}")
        shape = self.image.shape
        exp = rng.exponential(1/lambda_param, shape).astype(int)
        noise = self.generate_noise_mat(rng, np.where(exp == 0, 1, exp) , True)
        # img = Image.fromarray(matrix_mult(self.image, noise))
        img = Image.fromarray(np.multiply(self.image, noise))

        cmap = "gray" if len(shape) == 2 else None

        print(f"CMAP: {cmap}\n LEN: {len(shape)}")
        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Image with added noise (λ: {lambda_param})"
            ], cmap=cmap)