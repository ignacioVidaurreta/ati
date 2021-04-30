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

        self.saltpepper_title = QLabel('Salt and Pepper')
        self.saltpepper_title.setStyleSheet("background-color: #d6f9d6")
        self.saltpepper_noise = newButton("Apply", self.onSaltPepperClick)
        self.p0_label, self.p0_input = QLabel("p0:"), QLineEdit()
        self.p1_label, self.p1_input = QLabel("p1:"), QLineEdit()

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

        self.layout.addWidget(self.saltpepper_title, 4, 0)
        self.layout.addWidget(self.p0_label, 4, 1)
        self.layout.addWidget(self.p0_input, 4, 2)
        self.layout.addWidget(self.p1_label, 4, 3)
        self.layout.addWidget(self.p1_input, 4, 4)
        self.layout.addWidget(self.saltpepper_noise, 4, 5)

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
        image = self.parent.changes[-1]
        rng = np.random.default_rng()
        psi = float(self.psi_input.text()) # Hay que ponerle un psi grande, tipo 30 para ver el ruido
        print(f"RAYLEIGH {rng.rayleigh(psi)}")

        if len(image) == 3:
            r_im = image[0]
            noise = self.generate_noise_mat(rng, rng.rayleigh(psi, r_im.shape), True)
            result1 = matrix_mult(r_im, noise)

            g_im = image[1]
            noise = self.generate_noise_mat(rng, rng.rayleigh(psi, g_im.shape), True)
            result2 = matrix_mult(g_im, noise)

            b_im = image[2]
            noise = self.generate_noise_mat(rng, rng.rayleigh(psi, b_im.shape), True)
            result3 = matrix_mult(b_im, noise)
            img = (result1, result2, result3)
        else:
            noise = self.generate_noise_mat(rng, rng.rayleigh(psi, image.shape), True)
            img = matrix_mult(self.parent.changes[-1], noise)

        display_before_after(
            self.parent,
            img,
            f"Image with added noise (ψ: {psi})"
        )

        plt.figure()
        count, bins, ignored = plt.hist(rng.rayleigh(psi, 10000), bins=200, density=True)
        plt.plot(bins, (bins/(psi**2))* np.exp((-bins**2)/(2*(psi**2))), linewidth=2, color='r')
        plt.title(f"Rayleigh Distribution plot psi={psi}")
        plt.show()

    def onExponentialClick(self):
        image = self.parent.changes[-1]
        rng = np.random.default_rng()
        lambda_param = float(self.lambda_input.text())
        # Exponential receives Beta which is 1/lambda
        print(f"EXPONENTIAL: {rng.exponential(1/lambda_param)}")
        if len(image) == 3:
            r_im = image[0]
            noise = self.generate_noise_mat(rng, rng.exponential(1/lambda_param, r_im.shape) , True)
            result1 = matrix_mult(r_im, noise)

            g_im = image[1]
            noise = self.generate_noise_mat(rng, rng.exponential(1/lambda_param, g_im.shape) , True)
            result2 = matrix_mult(g_im, noise)

            b_im = image[2]
            noise = self.generate_noise_mat(rng, rng.exponential(1/lambda_param, b_im.shape) , True)
            result3 = matrix_mult(b_im, noise)
            img = (result1, result2, result3)
        else:
            noise = self.generate_noise_mat(rng, rng.exponential(1/lambda_param, image.shape) , True)
            img = matrix_mult(image, noise)

        display_before_after(
            self.parent,
            img,
            f"Image with added noise (λ: {lambda_param})"
        )

        plt.figure()
        count, bins, ignored = plt.hist(rng.exponential(1/lambda_param, 1000), 30, density=True)
        plt.plot(bins, lambda_param * np.exp(-bins*lambda_param), linewidth=2, color='r')
        plt.title(f"Exponential Distribution plot lambda={lambda_param}")
        plt.show()

    # IMPORTANT: does not use noise percentage
    # TODO: fix it to use noise percentage
    def onSaltPepperClick(self):
        print(f"P0: {self.p0_input.text()}; P1: {self.p1_input.text()}")

        img = np.copy(self.parent.changes[-1])

        p0 = float(self.p0_input.text())
        p1 = float(self.p1_input.text())

        rng = np.random.default_rng()

        if(len(self.image.shape) == 3):
            r, g, b = img[0], img[1], img[2]
            for x,y in np.ndindex(r.shape):
                rnd = rng.random()
                if (rnd < p0):
                    r[x,y] = 0
                    g[x,y] = 0
                    b[x,y] = 0
                elif (rnd >= p1):
                    r[x,y] = 255
                    g[x,y] = 255
                    b[x,y] = 255            
            img = (r,g,b)

        else:
            for x in range(np.size(img,0)):
                for y in range(np.size(img,1)):
                    rnd = rng.random()
                    if (rnd < p0):
                        img[x,y] = 0
                    elif (rnd >= p1):
                        img[x,y] = 255 


        display_before_after(
            self.parent,
            img,
            f'S&P Noise: p0=' + self.p0_input.text() + ', p1=' + self.p1_input.text()
        )
