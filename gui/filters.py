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

        max_idx_width = self.image.shape[0]-1
        max_idx_height = self.image.shape[1]-1

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
