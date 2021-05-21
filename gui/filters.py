from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
import time

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

ALL = "all"
VER = "0°"
HOR = "90°"
DIAG1 = "45°"
DIAG2 = "135°"


# Filter that does not apply anything to the image
class Filter():

    def __init__(self, image, L=3):
        self.image = image  # image is now a numpy array
        self.L = L

    # Must override this method
    def compute(self, pixels, x, y):
        return pixels[x][y]

    def f(i):
        print(i)

    def apply(self, normalize=False):
        start_time = time.time()

        original_pixels = self.image

        h = math.floor(self.L / 2)
        self.mid = h

        max_idx_width = self.image.shape[0] - 1
        max_idx_height = self.image.shape[1] - 1

        new_pixels = np.zeros(shape=self.image.shape)

        def process_pixel(index):
            x = index[0]
            y = index[1]

            if x - h < 0 or \
                    y - h < 0 or \
                    x + h > max_idx_width or \
                    y + h > max_idx_height:
                # We wont do anything at borders
                pass
            else:
                new_pixels[x][y] = self.compute(original_pixels, x, y)

            return None

        set(map(process_pixel, np.ndindex(self.image.shape)))

        if normalize:
            max_value = new_pixels.max()
            min_value = new_pixels.min()

            def process_normalize(index):
                x = index[0]
                y = index[1]
                new_pixels[x][y] = ((new_pixels[x][y] - min_value) * 255) / (max_value - min_value)

                return None

            set(map(process_normalize, np.ndindex(self.image.shape)))

        elapsed_time = time.time() - start_time
        print(f'ELAPSED TIME: {elapsed_time}')
        return new_pixels


class MeanFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                val = val + pixels[x + x_index, y + y_index]

        return val / (self.L ** 2)


class MedianFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        values = []

        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                values.append(
                    pixels[x + x_index, y + y_index]
                )

        values.sort()
        return values[self.L + 1]


class WeightedMedianFilter(Filter):

    def __init__(self, image):
        super().__init__(image, L=3)

        self.weighted_mask = [4, 2, 1]

    # Must override this method
    def compute(self, pixels, x, y):
        values = []

        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                # we can compute manhattan distance like this
                # because center point is always at (0,0)
                distance_to_center = self.distance(0, 0, x_index, y_index)
                # According to distance to center, we append value many times
                for times in range(self.weighted_mask[math.ceil(distance_to_center)]):
                    values.append(
                        pixels[x + x_index, y + y_index]
                    )

        # values has 16 elements
        values.sort()

        # returns avg of median since qty of elements is even
        return (float(values[7]) + float(values[8])) / 2

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class GaussianFilter(Filter):

    def __init__(self, image, sigma, L=None):
        if L is None:
            # Recommended sigma to represent
            # gaussian filter properly
            L = math.ceil(2 * sigma + 1)

        super().__init__(image, L=L)

        self.sigma = sigma

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                weight = self.gaussian(x_index, y_index)
                val = val + (weight * pixels[x + x_index][y + y_index])

        return val

    def gaussian(self, x, y):
        denominator = math.sqrt(2 * math.pi * (self.sigma ** 2))
        exponent = -1 * ((x ** 2) + (y ** 2)) / (self.sigma ** 2)
        return (1 / denominator) * math.exp(exponent)

    def __str__():
        return f'Gaussian, sigma:{self.sigma}, mask:{self.L}'


class EnhancementFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0

        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                weight = self.L ** 2 - 1 if x_index == 0 and y_index == 0 else -1
                val = val + (weight * pixels[x + x_index, y + y_index])

        val = val / (self.L ** 2)

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


class DirectionalFilter(Filter):

    def __init__(self, image, mode="all"):
        super().__init__(image, L=3)
        self.mode = mode
        self.vertical = [
            [1, 1, 1],
            [1, -2, 1],
            [-1, -1, -1]
        ]

        self.horizontal = [
            [-1, 1, 1],
            [-1, -2, 1],
            [-1, 1, 1]
        ]

        self.diag_45 = [
            [1, 1, 1],
            [-1, -2, 1],
            [-1, -1, 1]
        ]

        self.diag_135 = [
            [-1, -1, 1],
            [-1, -2, 1],
            [1, 1, 1]
        ]

    def compute(self, pixels, x, y):
        if self.mode == ALL:
            value_v, value_h = 0, 0
            value_45, value_135 = 0, 0
            for x_index in range(-1 * self.mid, self.mid + 1):
                for y_index in range(-1 * self.mid, self.mid + 1):
                    value_v += pixels[x + x_index, y + y_index] * self.vertical[x_index + 1][y_index + 1]
                    value_h += pixels[x + x_index, y + y_index] * self.horizontal[x_index + 1][y_index + 1]

                    value_45 += pixels[x + x_index, y + y_index] * self.diag_45[x_index + 1][y_index + 1]
                    value_135 += pixels[x + x_index, y + y_index] * self.diag_135[x_index + 1][y_index + 1]

            return math.sqrt(value_v ** 2 + value_h ** 2 + value_45 ** 2 + value_135 ** 2)
        else:
            value = 0
            for x_index in range(-1 * self.mid, self.mid + 1):
                for y_index in range(-1 * self.mid, self.mid + 1):
                    if self.mode == VER:
                        value += pixels[x + x_index, y + y_index] * self.vertical[x_index + 1][y_index + 1]
                    elif self.mode == HOR:
                        value += pixels[x + x_index, y + y_index] * self.horizontal[x_index + 1][y_index + 1]
                    elif self.mode == DIAG1:
                        value += pixels[x + x_index, y + y_index] * self.diag_45[x_index + 1][y_index + 1]
                    elif self.mode == DIAG2:
                        value += pixels[x + x_index, y + y_index] * self.diag_135[x_index + 1][y_index + 1]
                    else:
                        raise Exception(f"{self.mode} is not a valid mode for DiagonalFilter")

            return value


class SobelFilter(Filter):
    def __init__(self, image):
        super().__init__(image, L=3)

    def compute(self, pixels, x, y):
        x_value = 0
        y_value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                x_mult = 2 * y_index if x == 0 else y_index
                y_mult = 2 * x_index if y == 0 else x_index

                x_value += pixels[x + x_index, y + y_index] * x_mult
                y_value += pixels[x + x_index, y + y_index] * y_mult

        return math.sqrt(x_value ** 2 + y_value ** 2)


class LaplacianFilter(Filter):

    def __init__(self, image):
        super().__init__(image, L=3)
        self.mask = [
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ]

    def compute(self, pixels, x, y):
        value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                value += pixels[x + x_index, y + y_index] * self.mask[x_index + 1][y_index + 1]

        return value


class ZeroCrosses:

    def replace(self, n, m, umbral=None):
        if umbral:
            if (abs(n) + abs(m)) <= umbral: return 0
        if n > 0 and m < 0 or n < 0 and m > 0:
            return 255
        return 0

    def compute(self, image, umbral=None):
        result = np.zeros(image.shape)

        for x in range(image.shape[0]):
            for y in range(image.shape[1] - 1):
                n = image[x, y]
                m = image[x, y + 1]
                if (m == 0) and (y + 1 < image.shape[1] - 1):
                    m = image[x, y + 2]
                result[x, y] = self.replace(n, m, umbral)

        return result

    def apply(self, image, umbral=None, join='union'):

        horizontal = self.compute(image, umbral=umbral)
        vertical = self.compute(image.T, umbral=umbral).T

        if join == 'union':
            return self.join_union(vertical, horizontal)

        return self.join_intersection(vertical, horizontal)

    def join_union(self, vertical, horizontal):
        result = np.zeros(vertical.shape)

        for x in range(vertical.shape[0]):
            for y in range(vertical.shape[1]):
                result[x, y] = 255 if vertical[x, y] == 255 or horizontal[x, y] == 255 else 0

        return result

    def join_intersection(self, vertical, horizontal):
        result = np.zeros(vertical.shape)

        for x in range(vertical.shape[0]):
            for y in range(vertical.shape[1]):
                result[x, y] = 255 if vertical[x, y] == 255 and horizontal[x, y] == 255 else 0

        return result


class LOGFilter(Filter):

    def __init__(self, image, sigma, L=None):
        if L is None:
            # recommended mask side
            L = math.ceil(6 * sigma + 1)

        super().__init__(image, L=L)
        self.sigma = sigma

        h = int(math.floor(L / 2))

        self.mask = np.zeros((L, L)).astype('float64')
        for x_index in range(-1 * h, h + 1):
            for y_index in range(-1 * h, h + 1):
                self.mask[x_index + h][y_index + h] = self.log(x_index, y_index)

    def compute(self, pixels, x, y):
        value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                value += pixels[x + x_index, y + y_index] * self.mask[x_index + 1][y_index + 1]

        return value

    def log(self, x, y):
        a = math.sqrt(2 * math.pi) * math.pow(self.sigma, 3)
        b = -1 / a  # left term
        c = (x ** 2 + y ** 2) / (self.sigma ** 2)
        d = 2 - c  # middle term
        e = c / 2
        f = math.exp(-1 * e)  # right term
        return b * d * f


class SusanFilter(Filter):
    def __init__(self, image, mode, L=7):
        super().__init__(image, L=L)
        self.DELTA = 0.25
        self.LIMIT = 15
        self.mode = mode
        self.mask = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
        ]
        self.N = 37

    def compute(self, pixels, x, y):
        r0 = int(pixels[x, y])
        count = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                if self.mask[x_index + self.mid][y_index + self.mid] == 1 and \
                        abs(int(pixels[x + x_index, y + y_index]) - r0) < self.LIMIT:
                    count += 1

        s_value = 1.0 - float(count/self.N)
        if abs(s_value - 0.75) <= self.DELTA and self.mode in ["Corners", "All"]:
            return -255
        elif abs(s_value - 0.5) <= self.DELTA and self.mode in ["Borders", "All"]:
            return -128

        return pixels[x, y]  # Do not modify if its not border or corner
