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
    SobelFilter,
    DirectionalFilter,
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
        self.prewitt.setStyleSheet("background-color: #ccccff")
        self.prewitt_filter = newButton("Apply", self.onPrewittClick)

        # Sobel Widgets
        self.sobel = QLabel("Sobel Method")
        self.sobel.setStyleSheet("background-color: #ccccff")
        self.sobel_filter = newButton("Apply", self.onSobelClick)

        # Directional Widgets
        self.directional = QLabel("Directional Method")
        self.directional.setStyleSheet("background-color: #ccccff")
        self.directional_filter = newButton("Apply", self.onDirectionalClick)

        # Laplacian Widgets
        self.laplacian = QLabel("Laplacian Method")
        self.laplacian.setStyleSheet("background-color: #ccccff")
        self.laplacian_filter = newButton("Apply", self.onLaplacianClick)

        # Slope Widgets
        self.slope = QLabel("Laplacian with Slope")
        self.slope.setStyleSheet("background-color: #ccccff")
        self.umbral_label, self.umbral_input = QLabel("Umbral"), QLineEdit()
        self.join_label, self.join_input = QLabel("Join"), QLineEdit('union')
        self.umbral_input.setText('10')
        self.slope_evaluation = newButton("Apply", self.onSlopeClick)

        # We add widgets to layout
        self.layout.addWidget(self.prewitt, 0, 0)
        self.layout.addWidget(self.prewitt_filter, 0, 1)

        self.layout.addWidget(self.sobel, 1, 0)
        self.layout.addWidget(self.sobel_filter, 1, 1)

        self.layout.addWidget(self.directional, 2, 0)
        self.layout.addWidget(self.directional_filter, 2, 1)

        self.layout.addWidget(self.laplacian, 3, 0)
        self.layout.addWidget(self.laplacian_filter, 3, 1)

        self.layout.addWidget(self.slope, 4, 0)
        self.layout.addWidget(self.umbral_label, 4, 1)
        self.layout.addWidget(self.umbral_input, 4, 2)
        self.layout.addWidget(self.join_label, 4, 3)
        self.layout.addWidget(self.join_input, 4, 4)
        self.layout.addWidget(self.slope_evaluation, 4, 5)

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

    def onSobelClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = SobelFilter(r)
            filter_g = SobelFilter(g)
            filter_b = SobelFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            sobel_filter = SobelFilter(image)
            np_img = sobel_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Sobel Filter'
        )

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

    def onDirectionalClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = DirectionalFilter(r)
            filter_g = DirectionalFilter(g)
            filter_b = DirectionalFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            directional_filter = DirectionalFilter(image)
            np_img = directional_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Directional Filter'
        )

    def onLaplacianClick(self):
        zero_crosses = ZeroCrosses()

        image = self.parent.changes[-1]

        def process_color(color, zero_crosses):
            laplacian = LaplacianFilter(color)
            result = laplacian.apply()
            return zero_crosses.apply(result)

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]
            
            np_img = (
                process_color(r, zero_crosses),
                process_color(g, zero_crosses),
                process_color(b, zero_crosses)
            )
        else:
            np_img = process_color(image, zero_crosses)

        display_before_after(
            self.parent,
            np_img,
            f'Laplacian Method'
        )

    def onSlopeClick(self):
        zero_crosses = ZeroCrosses()

        self.umbral = int(self.umbral_input.text())
        self.join = self.join_input.text()

        image = self.parent.changes[-1]

        def process_color(color, zero_crosses):
            laplacian = LaplacianFilter(color)
            result = laplacian.apply()
            return zero_crosses.apply(result, umbral=self.umbral, join=self.join)
        
        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            np_img = (
                process_color(r, zero_crosses),
                process_color(g, zero_crosses),
                process_color(b, zero_crosses)
            )
        else:
            np_img = process_color(image, zero_crosses)

        display_before_after(
            self.parent,
            np_img,
            f'Laplacian with {self.join} and umbral:{self.umbral}'
        )
