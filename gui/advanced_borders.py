from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox
)
from utils import (
    newButton,
    display_before_after,
)
from display import hdisplay
from filters import (
    GaussianFilter,
    PrewittFilter,
    SobelFilter,
)

class AdvancedBordersTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape


        # Harris Widgets
        self.harris = QLabel("Harris Method")
        self.harris.setStyleSheet("background-color: #ccccff")
        # self.t1_label, self.t1_input = QLabel("t1"), QLineEdit()
        # self.t1_input.setText("70")
        self.harris_btn = newButton("Apply", self.onHarrisClick)

        # We add widgets to layout
        self.layout.addWidget(self.harris, 0, 0)
        self.layout.addWidget(self.harris_btn, 0, 1)
        self.setLayout(self.layout)


    def onHarrisClick(self):
        self.image = self.parent.changes[-1]

        if len(self.imageShape) == 3:
            print("ERROR, RGB IMAGE DETECTED")
            return

        prewitt_dx = PrewittFilter(self.image, mode="dx").apply(normalize=True)
        prewitt_dy = PrewittFilter(self.image, mode="dy").apply(normalize=True)

        i_xx = GaussianFilter(np.square(prewitt_dx), sigma=2, L=7).apply()
        i_yy = GaussianFilter(np.square(prewitt_dy), sigma=2, L=7).apply()

        i_xy = GaussianFilter(np.multiply(prewitt_dx, prewitt_dy), sigma=2, L=7).apply()

        k = 0.04
        R = (i_xx * i_yy - np.square(i_xy)) - k * np.square((i_xx + i_yy))

        max_val = 80
        umbralized = np.array([list(map(lambda x: 255 if x > max_val else 0, col)) for col in R])

        display_before_after(
            self.parent,
            umbralized,
            f"Harris Method - Umbral {max_val}"
        )
