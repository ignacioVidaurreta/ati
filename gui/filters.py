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
    TRANSFORMATION_FOLDER
)

# Filter that does not apply anything to the image
class Filter():

    def __init__(self, image, L=3):
        self.image = image # image is now a numpy array
        self.L = L

    # Must override this method
    def compute(self, pixels, x, y):
        return pixels[x][y]


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

            for x,y in np.ndindex(self.image.shape):
                new_pixels[x][y] = ((new_pixels[x][y] - min_value) * 255)/(max_value-min_value)

        return new_pixels


class MeanFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                val = val + pixels[x+x_index, y+y_index]

        return val/(self.L ** 2)


class MedianFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        values = []

        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                values.append(
                    pixels[x+x_index, y+y_index]
                )

        values.sort()
        return values[self.L + 1]


class WeightedMedianFilter(Filter):

    def __init__(self, image):
        super().__init__(image, L=3)

        self.weighted_mask = [4,2,1]

    # Must override this method
    def compute(self, pixels, x, y):
        values = []

        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                # we can compute manhattan distance like this
                # because center point is always at (0,0)
                distance_to_center = self.distance(0, 0, x_index, y_index)
                # According to distance to center, we append value many times
                for times in range(self.weighted_mask[math.ceil(distance_to_center)]):
                    values.append(
                        pixels[x+x_index, y+y_index]
                    )

        # values has 16 elements
        values.sort()

        # returns avg of median since qty of elements is even
        return (float(values[7])+float(values[8]))/2

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(((x1-x2) ** 2) + ((y1-y2) ** 2))


class GaussianFilter(Filter):

    def __init__(self, image, sigma, L=None):
        if L is None:
            # Recommended sigma to represent
            # gaussian filter properly
            L = math.ceil(2*sigma+1)

        super().__init__(image, L=L)

        self.sigma = sigma

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                weight = self.gaussian(x_index, y_index)
                val = val + (weight * pixels[x+x_index][y+y_index])

        return val

    def gaussian(self, x, y):
        denominator = math.sqrt(2*math.pi*(self.sigma ** 2))
        exponent = -1*((x ** 2) + (y ** 2))/(self.sigma ** 2)
        return (1/denominator) * math.exp(exponent)

    def __str__():
        return f'Gaussian, sigma:{self.sigma}, mask:{self.L}'


class EnhancementFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0

        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                weight = self.L ** 2 -1 if x_index == 0 and y_index == 0 else -1
                val = val + (weight * pixels[x+x_index, y+y_index])

        val = val/(self.L ** 2)

        return val


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

    def display_and_save(self, np_img, legend, file_legend):
        if len(np_img) == 3:
            img = numpy_to_pil_image((np_img[0],np_img[1], np_img[2]))
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"{legend}"
            ])
        else:
            img = numpy_to_pil_image(np_img)
            hdisplay([self.parent.image, img], rows=1, cols=2, titles=[
                "Original Image",
                f"{legend}"
            ], cmap="gray")
        # Changes now has a numpy array
        self.parent.changes.append(np_img)
        # We save current PIL image for display
        self.parent.image = img
        self.parent.buttonUndo.setEnabled(True)


    def onGaussianClick(self):
        self.sigma = int(self.sigma_input.text())
        self.gaussian_L = int(self.gaussian_l_input.text())

        # IMAGE CHANGE 3
        # we will always load image when about to transform it
        # to make sure we are using last transformation
        image = self.parent.changes[-1]

        # IMAGE CHANGE 4
        # self.imageShape is still accessible since it's computed
        # with self.parent.image (PIL image). No need for update
        if len(self.image.shape) == 3:
            # IMAGE CHANGE 5
            # we will replace split with this access form for rgb
            r,g,b = image[0], image[1], image[2]

            filter_r = GaussianFilter(r, self.sigma, L=self.gaussian_L)
            filter_g = GaussianFilter(g, self.sigma, L=self.gaussian_L)
            filter_b = GaussianFilter(b, self.sigma, L=self.gaussian_L)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            # IMAGE CHANGE 6
            np_img = (r_result, g_result, b_result)

        else:
            gaussian_filter = GaussianFilter(image, self.sigma, L=self.gaussian_L)
            result_image = gaussian_filter.apply(normalize=True)
            # IMAGE CHANGE 7
            np_img = result_image

        # IMAGE CHANGE 8
        # check out this method since it does all the updates needed in parent widget
        self.display_and_save(
            np_img,
            f'Gaussian, \u03C3:{self.sigma}, mask side:{self.gaussian_L}',
            f'filter_gaussian_{self.sigma}_{self.gaussian_L}')

    def onMeanClick(self):
        self.mean_L = int(self.mean_l_input.text())

        image = self.parent.changes[-1]

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = MeanFilter(r, L=self.mean_L)
            filter_g = MeanFilter(g, L=self.mean_L)
            filter_b = MeanFilter(b, L=self.mean_L)

            r_result = filter_r.apply()
            g_result = filter_g.apply()
            b_result = filter_b.apply()

            np_img = (r_result, g_result, b_result)
        else:
            mean_filter = MeanFilter(image, L=self.mean_L)
            np_img = mean_filter.apply()

        self.display_and_save(
            np_img,
            f'Mean Filter, mask side:{self.mean_L}',
            f'filter_mean_{self.mean_L}')

    def onMedianClick(self):
        self.median_L = int(self.median_l_input.text())

        image = self.parent.changes[-1]

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = MedianFilter(r, L=self.median_L)
            filter_g = MedianFilter(g, L=self.median_L)
            filter_b = MedianFilter(b, L=self.median_L)

            r_result = filter_r.apply()
            g_result = filter_g.apply()
            b_result = filter_b.apply()

            np_img = (r_result, g_result, b_result)
        else:
            median_filter = MedianFilter(image, L=self.median_L)
            np_img = median_filter.apply()

        self.display_and_save(
            np_img,
            f'Median Filter, mask side:{self.median_L}',
            f'filter_median_{self.median_L}')


    def onEnhancementClick(self):
        self.enhancement_L = int(self.enhancement_l_input.text())

        image = self.parent.changes[-1]

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = EnhancementFilter(r, L=self.enhancement_L)
            filter_g = EnhancementFilter(g, L=self.enhancement_L)
            filter_b = EnhancementFilter(b, L=self.enhancement_L)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            enhancement_filter = EnhancementFilter(image, L=self.enhancement_L)
            np_img = enhancement_filter.apply(normalize=True)

        self.display_and_save(
            np_img,
            f'Enhancement Filter, mask side:{self.enhancement_L}',
            f'filter_enhancement_{self.enhancement_L}')

    def onWeightedMedianClick(self):
        image = self.parent.changes[-1]

        if len(self.image.shape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = WeightedMedianFilter(r)
            filter_g = WeightedMedianFilter(g)
            filter_b = WeightedMedianFilter(b)

            r_result = filter_r.apply()
            g_result = filter_g.apply()
            b_result = filter_b.apply()

            np_img = (r_result, g_result, b_result)
        else:
            weighted_median_filter = WeightedMedianFilter(image)
            np_img = weighted_median_filter.apply()

        self.display_and_save(
            np_img,
            f'Weighted Median Filter, mask side:{3}',
            f'filter_weighted_median')
