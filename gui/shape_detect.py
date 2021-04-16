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
    display_before_after, 
    numpy_to_pil_image,
    TRANSFORMATION_FOLDER
)
from display import hdisplay
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

            filter_r = PrewittFilter(r)
            filter_g = PrewittFilter(g)
            filter_b = PrewittFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            prewitt_filter = PrewittFilter(image)
            np_img = prewitt_filter.apply(normalize=True)

        display_before_after(
            self.parent, 
            np_img, 
            f'Prewitt Filter'
        )


class PrewittFilter(Filter):
       
    def __init__(self, image):
        super().__init__(image, L=3)

    def compute(self, pixels, x, y):
        x_value = 0
        y_value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                x_value += pixels[x + x_index, y + y_index] * y_index
                y_value += pixels[x + x_index, y + y_index] * x_index

        return math.sqrt(x_value ** 2 + y_value ** 2)
