from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit

)
from display import hdisplay
from utils import newButton, compute_histogram, TRANSFORMATION_FOLDER
from filters import Filter

class ShapeDetectTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape

        # Prewitt Widgets
        self.prewitt = QLabel("PREWITT DETECTION")
        self.prewitt.setStyleSheet("background-color: #d4ebf2")

        self.prewitt_filter = newButton("Apply", self.onPrewittClick)


        # We add widgets to layout
        self.layout.addWidget(self.prewitt, 0, 0)
        self.layout.addWidget(self.prewitt_filter, 0, 1)

        self.setLayout(self.layout)

    def display_and_save(self, img, legend):
        if len(self.imageShape) == 3:
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"{legend}"
            ])
        else:
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"{legend}"
            ], cmap="gray")

        self.parent.changes.append(self.parent.image)
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)

    def onPrewittClick(self):
        img = self.parent.image.copy()

        if len(self.imageShape) == 3:
            r,g,b = img.copy().split()

            filter_r = PrewittFilter(r, is_dx=True)
            filter_g = PrewittFilter(g, is_dx=True)
            filter_b = PrewittFilter(b, is_dx=True)

            r = filter_r.apply(normalize=True)
            g = filter_g.apply(normalize=True)
            b = filter_b.apply(normalize=True)

            img_x = Image.merge("RGB", (r,g,b))

            self.display_and_save(img_x, f'Prewitt Filter (dI/dx)')

            r,g,b = img.split()

            filter_r = PrewittFilter(r, is_dx=False)
            filter_g = PrewittFilter(g, is_dx=False)
            filter_b = PrewittFilter(b, is_dx=False)

            r = filter_r.apply(normalize=True)
            g = filter_g.apply(normalize=True)
            b = filter_b.apply(normalize=True)

            img_y = Image.merge("RGB", (r,g,b))

            self.display_and_save(img_y, f'Prewitt Filter (dI/dy)')
        else:
            prewitt_filter = PrewittFilter(img, is_dx=True)
            img_x = prewitt_filter.apply(normalize=True)
            self.display_and_save(img_x, f'Prewitt Filter (dI/dx)')

            prewitt_filter = PrewittFilter(img, is_dx=False)
            img_y = prewitt_filter.apply(normalize=True)
            self.display_and_save(img_y, f'Prewitt Filter (dI/dy)')


class PrewittFilter(Filter):
    """
    TODO: implement synthesis to join dx and dy.
    """
    def __init__(self, image, is_dx):
        super().__init__(image, L=3)

        self.weighted_mask = [4,2,1]
        self.is_dx = is_dx
    def compute(self, pixels, x, y):
        value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                mult = y_index if self.is_dx else x_index
                value += pixels[x + x_index, y + y_index] * mult

        return value