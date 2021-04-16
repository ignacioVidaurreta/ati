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

            filter_r = PrewittFilter(r)
            filter_g = PrewittFilter(g)
            filter_b = PrewittFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
            np_img_x = (filter_r.dx, filter_g.dx, filter_b.dx)
            np_img_y = (filter_r.dy, filter_g.dy, filter_b.dy)

            hdisplay(
                [numpy_to_pil_image(np_img_x), numpy_to_pil_image(np_img_y)], 
                rows=1, 
                cols=2, 
                titles=['Prewitt Filter (dI/dx)', 'Prewitt Filter (dI/dy)']
            )

        else:
            prewitt_filter = PrewittFilter(image)
            np_img = prewitt_filter.apply(normalize=True)
            
            hdisplay(
                [numpy_to_pil_image(prewitt_filter.dx), numpy_to_pil_image(prewitt_filter.dy)], 
                rows=1, 
                cols=2, 
                titles=['Prewitt Filter (dI/dx)', 'Prewitt Filter (dI/dy)'],
                cmap="gray"
            )
            
        display_before_after(
            self.parent, 
            np_img, 
            f'Prewitt Filter'
        )


class Modes:
        DX = 0
        DY = 1
        FULL = 2

class PrewittFilter(Filter):
       
    def __init__(self, image, mode=Modes.FULL):
        super().__init__(image, L=3)

        self.dx = np.zeros(image.shape)
        self.dy = np.zeros(image.shape)

        self.mode = mode
    
    def apply(self, normalize=False):
        original_pixels = np.copy(self.image)

        h = math.floor(self.L/2)
        self.mid = h

        max_idx_width = self.image.shape[1]-1
        max_idx_height = self.image.shape[0]-1

        new_pixels = np.zeros(shape=self.image.shape)

        for x,y in np.ndindex(self.image.shape):
            if x-h < 0 or \
               y-h < 0 or \
               x+h > max_idx_width or \
               y+h > max_idx_height:
                # We wont do anything at borders
                pass
            else:
                new_pixels[x][y] = self.compute(original_pixels, x, y)

        if normalize:
            max_value = new_pixels.max()
            min_value = new_pixels.min()

            max_value_x = self.dx.max()
            min_value_x = self.dx.min()

            max_value_y = self.dy.max()
            min_value_y = self.dy.min()

            for x,y in np.ndindex(self.image.shape):
                new_pixels[x][y] = ((new_pixels[x][y] - min_value) * 255)/(max_value-min_value)
                self.dx[x][y] = ((self.dx[x][y] - min_value_x) * 255)/(max_value_x-min_value_x)
                self.dy[x][y] = ((self.dy[x][y] - min_value_y) * 255)/(max_value_y-min_value_y)

        return new_pixels


    def compute(self, pixels, x, y):
        x_value = 0
        y_value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                x_value += pixels[x + x_index, y + y_index] * y_index
                y_value += pixels[x + x_index, y + y_index] * x_index

        self.dx[x][y] = x_value
        self.dy[x][y] = y_value

        return math.sqrt(x_value ** 2 + y_value ** 2)