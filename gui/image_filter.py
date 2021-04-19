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
from utils import (
    newButton, 
    numpy_to_pil_image,
    compute_histogram, 
    TRANSFORMATION_FOLDER,
    display_before_after
)
from filters import (
    MeanFilter,
    MedianFilter,
    WeightedMedianFilter,
    GaussianFilter,
    EnhancementFilter
)

class FilterTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Gaussian Widgets
        self.gaussian = QLabel("GAUSSIAN FILTER")
        self.gaussian.setStyleSheet("background-color: #d4ebf2")
        self.sigma_label, self.sigma_input = QLabel("Sigma"), QLineEdit()
        self.sigma_input.setText('1')
        self.auto_mask = newButton("Automatic Mask", self.onAutoMaskClick)
        self.gaussian_l, self.gaussian_l_input = QLabel("Mask Side"), QLineEdit()
        self.gaussian_filter = newButton("Apply", self.onGaussianClick)

        # Mean Widgets
        self.mean = QLabel("MEAN FILTER")
        self.mean.setStyleSheet("background-color: #d4ebf2")
        self.mean_l, self.mean_l_input = QLabel("Mask Side"), QLineEdit()
        self.mean_filter = newButton("Apply", self.onMeanClick)

        # Median Widgets
        self.median = QLabel("MEDIAN FILTER")
        self.median.setStyleSheet("background-color: #d4ebf2")
        self.median_l, self.median_l_input = QLabel("Mask Side"), QLineEdit()
        self.median_filter = newButton("Apply", self.onMedianClick)

        # Enhancement Widgets
        self.enhancement = QLabel("ENHANCEMENT FILTER")
        self.enhancement.setStyleSheet("background-color: #d4ebf2")
        self.enhancement_l, self.enhancement_l_input = QLabel("Mask Side"), QLineEdit()
        self.enhancement_filter = newButton("Apply", self.onEnhancementClick)

        # Weighted Median Widgets
        self.weighted_median = QLabel("WEIGHTED MEDIAN FILTER")
        self.weighted_median.setStyleSheet("background-color: #d4ebf2")
        self.weighted_median_filter = newButton("Apply", self.onWeightedMedianClick)

        # We add widgets to layout
        self.layout.addWidget(self.gaussian, 0, 0)
        self.layout.addWidget(self.sigma_label, 0, 1)
        self.layout.addWidget(self.sigma_input, 0, 2)
        self.layout.addWidget(self.auto_mask, 0, 3)
        self.layout.addWidget(self.gaussian_l, 0, 5)
        self.layout.addWidget(self.gaussian_l_input, 0, 5)
        self.layout.addWidget(self.gaussian_filter, 0, 6)

        self.layout.addWidget(self.mean, 1, 0)
        self.layout.addWidget(self.mean_l, 1, 1)
        self.layout.addWidget(self.mean_l_input, 1, 2)
        self.layout.addWidget(self.mean_filter, 1, 3)

        self.layout.addWidget(self.median, 2, 0)
        self.layout.addWidget(self.median_l, 2, 1)
        self.layout.addWidget(self.median_l_input, 2, 2)
        self.layout.addWidget(self.median_filter, 2, 3)

        self.layout.addWidget(self.enhancement, 3, 0)
        self.layout.addWidget(self.enhancement_l, 3, 1)
        self.layout.addWidget(self.enhancement_l_input, 3, 2)
        self.layout.addWidget(self.enhancement_filter, 3, 3)

        self.layout.addWidget(self.weighted_median, 4, 0)
        self.layout.addWidget(self.weighted_median_filter, 4, 1)

        self.setLayout(self.layout)

    def onAutoMaskClick(self):
        self.sigma = int(self.sigma_input.text())
        self.L = 2*self.sigma+1
        self.gaussian_l_input.setText(str(self.L))

    def onGaussianClick(self):
        self.sigma = int(self.sigma_input.text())
        self.gaussian_L = int(self.gaussian_l_input.text())

        # IMAGE CHANGE 3
        # makes sure we are using last transformation
        image = self.parent.changes[-1]

        def process_color(color):
            gaussian = GaussianFilter(color, self.sigma, L=self.gaussian_L)
            return gaussian.apply(normalize=True)

        # IMAGE CHANGE 4
        np_img = tuple(map(process_color, image)) if len(image) == 3 else process_color(image)

        # IMAGE CHANGE 5
        # check out this method since it does all the updates needed in parent widget
        display_before_after(
            self.parent,
            np_img,
            f'Gaussian, \u03C3:{self.sigma}, mask side:{self.gaussian_L}'
        )

    def onMeanClick(self):
        self.mean_L = int(self.mean_l_input.text())

        image = self.parent.changes[-1]

        def process_color(color):
            mean_filter = MeanFilter(color, L=self.mean_L)
            return mean_filter.apply()

        np_img = tuple(map(process_color, image)) if len(image) == 3 else process_color(image)
    
        display_before_after(
            self.parent,
            np_img,
            f'Mean Filter, mask side:{self.mean_L}'
        )

    def onMedianClick(self):
        self.median_L = int(self.median_l_input.text())

        image = self.parent.changes[-1]

        def process_color(color):
            mean_filter = MedianFilter(color, L=self.median_L)
            return mean_filter.apply()

        np_img = tuple(map(process_color, image)) if len(image) == 3 else process_color(image)

        display_before_after(
            self.parent,
            np_img,
            f'Median Filter, mask side:{self.median_L}'
        )


    def onEnhancementClick(self):
        self.enhancement_L = int(self.enhancement_l_input.text())

        image = self.parent.changes[-1]

        def process_color(color):
            mean_filter = EnhancementFilter(color, L=self.enhancement_L)
            return mean_filter.apply(normalize=True)

        np_img = tuple(map(process_color, image)) if len(image) == 3 else process_color(image)

        display_before_after(
            self.parent,
            np_img,
            f'Enhancement Filter, mask side:{self.enhancement_L}'
        )

    def onWeightedMedianClick(self):
        image = self.parent.changes[-1]
        
        def process_color(color):
            mean_filter = WeightedMedianFilter(color)
            return mean_filter.apply()

        np_img = tuple(map(process_color, image)) if len(image) == 3 else process_color(image)

        display_before_after(
            self.parent,
            np_img,
            f'Weighted Median Filter, mask side:{3}'
        )
