import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit

)
from display import hdisplay
from utils import newButton, TRANSFORMATION_FOLDER
from PIL import Image
import numpy as np
from matrix_util import matrix_mult, matrix_sum
from utils import get_shape, display_before_after

class NoiseTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = get_shape(self.image)

        self.noise_ptg_label, self.noise_ptg_input = QLabel("Noise Percentage"), QLineEdit()
        self.noise_ptg_input.setFixedWidth(100)
        self.nooise_message = QLabel("Must be between 0 and 100 (%)")

        # Buttons definitions
        self.gaussian_title = QLabel("Gaussian Noise")
        self.gaussian_title.setStyleSheet("background-color: #d6f9d6")
        self.gaussian_noise = newButton("Apply", self.onGaussianClick)
        self.mu_label, self.mu_input = QLabel("Mu"), QLineEdit()
        self.mu_input.setText('0')
        self.sigma_label, self.sigma_input = QLabel("Sigma"), QLineEdit()

        self.rayleigh_title = QLabel("Rayleigh Noise")
        self.rayleigh_title.setStyleSheet("background-color: #d6f9d6")
        self.psi_label, self.psi_input = QLabel("Psi"), QLineEdit()
        self.rayleigh_btn = newButton("Apply", self.onRayleighClick)

        self.exponential_title = QLabel("Exponential Noise")
        self.exponential_title.setStyleSheet("background-color: #d6f9d6")
        self.exponential = newButton("Apply", self.onExponentialClick)
        self.lambda_label, self.lambda_input = QLabel("Lambda"), QLineEdit()


        # We add widgets to layout
        self.layout.addWidget(self.noise_ptg_label, 0, 0)
        self.layout.addWidget(self.noise_ptg_input, 0, 1)
        self.layout.addWidget(self.nooise_message, 0, 2)

        self.layout.addWidget(self.gaussian_title, 1, 0)
        self.layout.addWidget(self.mu_label, 1, 1)
        self.layout.addWidget(self.mu_input, 1, 2)
        self.layout.addWidget(self.sigma_label, 1, 3)
        self.layout.addWidget(self.sigma_input, 1, 4)
        self.layout.addWidget(self.gaussian_noise, 1, 5)

        self.layout.addWidget(self.rayleigh_title, 2, 0)
        self.layout.addWidget(self.psi_label, 2, 1)
        self.layout.addWidget(self.psi_input, 2, 2)
        self.layout.addWidget(self.rayleigh_btn, 2, 3)

        self.layout.addWidget(self.exponential_title, 3, 0)
        self.layout.addWidget(self.lambda_label, 3, 1)
        self.layout.addWidget(self.lambda_input, 3, 2)
        self.layout.addWidget(self.exponential, 3, 3)


        self.setLayout(self.layout)

    def generate_noise_mat(self, rng, full_noise, is_mult):
        self.replace_rate = float(self.noise_ptg_input.text()) / 100
        if self.replace_rate == 1:
            return full_noise

        mask = np.random.choice([0,1], size=full_noise.shape, p=(1-self.replace_rate, self.replace_rate)).astype(np.bool)
        if is_mult:
            neut = np.ones(full_noise.shape)
        else:
            neut = np.zeros(full_noise.shape)

        neut[mask] = full_noise[mask]
        return neut


    # Convention: on[ButtonName]Click
    def onGaussianClick(self):
        image = self.parent.changes[-1]
        print(f"SIGMA: {self.sigma_input.text()}; MU: {self.mu_input.text()}")
        rng = np.random.default_rng()
        sigma = float(self.sigma_input.text())
        mu = float(self.mu_input.text()) # Should usually be zero

        shape = self.imageShape
        if len(image) == 3:
            r_im = image[0]
            noise = self.generate_noise_mat(rng, rng.normal(mu, sigma, r_im.shape), False)
            result1 = matrix_sum(r_im, noise)

            g_im = image[1]
            noise = self.generate_noise_mat(rng, rng.normal(mu, sigma, g_im.shape), False)
            result2 = matrix_sum(g_im, noise)

            b_im = image[2]
            noise = self.generate_noise_mat(rng, rng.normal(mu, sigma, b_im.shape), False)
            result3 = matrix_sum(b_im, noise)
            img = (result1, result2, result3)
        else:
            noise = self.generate_noise_mat(rng, rng.normal(mu, sigma, shape), False)
            img = matrix_sum(image, noise)

        cmap = "gray" if len(shape) == 2 else None

        print(f"CMAP: {cmap}\n LEN: {len(shape)}")
        display_before_after(
            self.parent,
            img,
            f"Image with added noise (σ: {self.sigma_input.text()} µ: {self.mu_input.text()})"
        )
        plt.figure()
        count, bins, ignored = plt.hist(rng.normal(mu, sigma, 1000), 30, density=True)
        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
        plt.title(f"Gaussian Distribution plot mu={mu}, sigma={sigma}")
        plt.show()

    def onRayleighClick(self):
        rng = np.random.default_rng()
        psi = float(self.psi_input.text()) # Hay que ponerle un psi grande, tipo 30 para ver el ruido
        print(f"RAYLEIGH {rng.rayleigh(psi)}")
        shape = self.imageShape

        noise = self.generate_noise_mat(rng, rng.rayleigh(psi, shape), True)

        img = Image.fromarray(matrix_mult(self.parent.image, noise))

        cmap = "gray" if len(shape) == 2 else None

        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Image with added noise (ψ: {psi})"
            ], cmap=cmap)

        plt.figure()
        count, bins, ignored = plt.hist(rng.rayleigh(psi, 10000), bins=200, density=True)
        plt.plot(bins, (bins/(psi**2))* np.exp((-bins**2)/(2*(psi**2))), linewidth=2, color='r')
        plt.title(f"Rayleigh Distribution plot psi={psi}")
        plt.show()
        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_rayleigh_psi{psi}_ptg{self.replace_rate}.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

    def onExponentialClick(self):
        rng = np.random.default_rng()
        lambda_param = float(self.lambda_input.text())
        # Exponential receives Beta which is 1/lambda
        print(f"EXPONENTIAL: {rng.exponential(1/lambda_param)}")
        shape = self.imageShape
        noise = self.generate_noise_mat(rng, rng.exponential(1/lambda_param, shape) , True)
        img = Image.fromarray(matrix_mult(self.parent.image, noise))

        cmap = "gray" if len(shape) == 2 else None

        hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"Image with added noise (λ: {lambda_param})"
            ], cmap=cmap)

        plt.figure()
        count, bins, ignored = plt.hist(rng.exponential(1/lambda_param, 1000), 30, density=True)
        plt.plot(bins, lambda_param * np.exp(-bins*lambda_param), linewidth=2, color='r')
        plt.title(f"Exponential Distribution plot lambda={lambda_param}")
        plt.show()
        #filename = (self.parent.filename.split("/")[-1]).split(".")[0]
        #img.save(f'{TRANSFORMATION_FOLDER}/{filename}_exponential_lambda{lambda_param}_ptg{self.replace_rate}.png')
        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)