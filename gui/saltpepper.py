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
    get_shape,
    TRANSFORMATION_FOLDER
)
from PIL import Image
import numpy as np

from utils import TRANSFORMATION_FOLDER
class SaltPepperTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = self.parent.changes[-1]
        self.imageShape = get_shape(self.image)

        # Buttons definitions
        self.saltpepper_title = QLabel('Salt and Pepper Noise')
        self.saltpepper_title.setStyleSheet("background-color: #FDDABB")
        self.saltpepper_noise = newButton("Apply", self.onSaltPepperClick)
        self.p0_label, self.p0_input = QLabel("p0:"), QLineEdit()
        self.p1_label, self.p1_input = QLabel("p1:"), QLineEdit()
        # We add widgets to layout
        self.layout.addWidget(self.saltpepper_title, 1, 0)
        self.layout.addWidget(self.p0_label, 1, 1)
        self.layout.addWidget(self.p0_input, 1, 2)
        self.layout.addWidget(self.p1_label, 1, 3)
        self.layout.addWidget(self.p1_input, 1, 4)
        self.layout.addWidget(self.saltpepper_noise, 2, 0)


        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onSaltPepperClick(self):
        print(f"P0: {self.p0_input.text()}; P1: {self.p1_input.text()}")

        img = np.copy(self.parent.changes[-1])

        p0 = float(self.p0_input.text())
        p1 = float(self.p1_input.text())

        RGB = len(self.image.shape) == 3

        rng = np.random.default_rng()

        for x in range(self.imageShape[0]):
            for y in range(self.imageShape[1]):
                rnd = rng.random()
                if (rnd < p0):
                    if(RGB):
                        img[x,y] = (0,0,0)
                    else:
                        img[x,y] = 0
                elif (rnd >= p1):
                    if(RGB):
                        img[x,y] = (255,255,255)
                    else:
                        img[x,y] = 255

        display_before_after(
            self.parent,
            img,
            f'Salt and Pepper Noise: p0=' + self.p0_input.text() + ', p1=' + self.p1_input.text()
        )

