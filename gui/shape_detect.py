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

            filter_r = PrewittFilter(r, mode=Modes.DX)
            filter_g = PrewittFilter(g, mode=Modes.DX)
            filter_b = PrewittFilter(b, mode=Modes.DX)

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

            filter_r = PrewittFilter(r, mode=Modes.DX)
            filter_g = PrewittFilter(g, mode=Modes.DY)
            filter_b = PrewittFilter(b, mode=Modes.DY)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img_y = (r_result, g_result, b_result)

            hdisplay(
                [numpy_to_pil_image(np_img_x), numpy_to_pil_image(np_img_y)], 
                rows=1, 
                cols=2, 
                titles=['Prewitt Filter (dI/dx)', 'Prewitt Filter (dI/dy)']
            )

            filter_r = PrewittFilter(r)
            filter_g = PrewittFilter(g)
            filter_b = PrewittFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)

        else:
            prewitt_filter = PrewittFilter(image, mode=Modes.DX)
            np_img_x = prewitt_filter.apply(normalize=True)
            

            prewitt_filter = PrewittFilter(image, mode=Modes.DY)
            np_img_y = prewitt_filter.apply(normalize=True)

            hdisplay(
                [numpy_to_pil_image(np_img_x), numpy_to_pil_image(np_img_y)], 
                rows=1, 
                cols=2, 
                titles=['Prewitt Filter (dI/dx)', 'Prewitt Filter (dI/dy)'],
                cmap="gray"
            )
            
            prewitt_filter = PrewittFilter(image)
            np_img = prewitt_filter.apply(normalize=True)

        display_before_after(
            self.parent, 
            np_img, 
            f'Prewitt Filter',
            submit=False
        )


class Modes:
        DX = 0
        DY = 1
        FULL = 2

class PrewittFilter(Filter):
       
    def __init__(self, image, mode=Modes.FULL):
        super().__init__(image, L=3)

        self.mode = mode

    def compute(self, pixels, x, y):
        x_value = 0
        y_value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                #mult = y_index if self.is_dx else x_index
                x_value += pixels[x + x_index, y + y_index] * y_index
                y_value += pixels[x + x_index, y + y_index] * x_index

        if self.mode == Modes.DX:
            return x_value
        elif self.mode == Modes.DY:
            return y_value
        else:
            return math.sqrt(x_value ** 2 + y_value ** 2)