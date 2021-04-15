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
from utils import (
    newButton, 
    compute_histogram,
    display_before_after, 
    TRANSFORMATION_FOLDER
)
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

    def onPrewittClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = PrewittFilter(r, is_dx=True)
            filter_g = PrewittFilter(g, is_dx=True)
            filter_b = PrewittFilter(b, is_dx=True)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img_x = (r_result, g_result, b_result)

            display_before_after(
                self.parent, 
                np_img_x, 
                f'Prewitt Filter (dI/dx)',
                submit=False
            )

            r,g,b = image[0], image[1], image[2]

            filter_r = PrewittFilter(r, is_dx=False)
            filter_g = PrewittFilter(g, is_dx=False)
            filter_b = PrewittFilter(b, is_dx=False)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img_y = (r_result, g_result, b_result)

            display_before_after(
                self.parent, 
                np_img_x, 
                f'Prewitt Filter (dI/dy)',
                submit=False
            )

        else:
            prewitt_filter = PrewittFilter(image, is_dx=True)
            np_img_x = prewitt_filter.apply(normalize=True)
            
            display_before_after(
                self.parent, 
                np_img_x, 
                f'Prewitt Filter (dI/dx)',
                submit=False
            )

            prewitt_filter = PrewittFilter(image, is_dx=False)
            np_img_y = prewitt_filter.apply(normalize=True)

            display_before_after(
                self.parent, 
                np_img_y, 
                f'Prewitt Filter (dI/dy)',
                submit=False
            )


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