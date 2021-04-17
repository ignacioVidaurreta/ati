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
from filters import (
    PrewittFilter,
    LaplacianFilter,
    ZeroCrosses
)

class ShapeDetectTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape

        # Prewitt Widgets
        self.prewitt = QLabel("Prewitt Method")
        self.prewitt.setStyleSheet("background-color: #d4ebf2")
        self.prewitt_filter = newButton("Apply", self.onPrewittClick)

        # Laplacian Widgets
        self.laplacian = QLabel("Laplacian Method")
        self.laplacian.setStyleSheet("background-color: #d4ebf2")
        self.laplacian_filter = newButton("Apply", self.onLaplacianClick)

        # We add widgets to layout
        self.layout.addWidget(self.prewitt, 0, 0)
        self.layout.addWidget(self.prewitt_filter, 0, 1)
        self.layout.addWidget(self.laplacian, 1, 0)
        self.layout.addWidget(self.laplacian_filter, 1, 1)

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

    def onLaplacianClick(self):
        zero_crosses = ZeroCrosses()

        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = LaplacianFilter(r)
            filter_g = LaplacianFilter(g)
            filter_b = LaplacianFilter(b)

            # we wont normalize since we need to
            # find zeros crosses.    
            r_result = zero_crosses.apply(filter_r.apply())
            g_result = zero_crosses.apply(filter_g.apply())
            b_result = zero_crosses.apply(filter_b.apply())

            np_img = (r_result, g_result, b_result)
        else:
            laplacian_filter = LaplacianFilter(image)
            np_img = zero_crosses.apply(laplacian_filter.apply())

        display_before_after(
            self.parent, 
            np_img, 
            f'Laplacian Method'
        )
