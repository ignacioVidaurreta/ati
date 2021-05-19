from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
import time

from filters import GaussianFilter

from display import hdisplay


class CannyCustomFilter:

    def __init__(self, image, L=3):
        self.image = image
        self.L = L

        # Start applying gaussian filter for smoothing the image
        gauss = GaussianFilter(self.image, 1)
        self.image = gauss.apply(normalize=False)

    def _discretize_angle(self, angle):
        PI_8 = math.pi / 8

        if angle < 0:
            angle += math.pi

        if abs(angle - 2 * PI_8) <= PI_8:
            discrete_angle = 45
        elif abs(angle - 4 * PI_8) <= PI_8:
            discrete_angle = 90
        elif abs(angle - 6 * PI_8) <= PI_8:
            discrete_angle = 135
        else:
            discrete_angle = 0

        return discrete_angle

    def compute(self, pixels, x, y):
        x_value = 0
        y_value = 0
        for x_index in range(-1 * self.mid, self.mid + 1):
            for y_index in range(-1 * self.mid, self.mid + 1):
                x_mult = 2 * y_index if x == 0 else y_index
                y_mult = 2 * x_index if y == 0 else x_index

                x_value += pixels[x + x_index, y + y_index] * x_mult
                y_value += pixels[x + x_index, y + y_index] * y_mult


        # Range is between -PI and PI.
        # https://www.w3schools.com/python/ref_math_atan2.asp#:~:text=The%20math.,is%20between%20PI%20and%20%2DPI.
        ret_val = math.atan2(y_value, x_value)
        angle = self._discretize_angle(ret_val)

        mod = math.sqrt(x_value ** 2 + y_value ** 2)

        return mod, angle

    def apply_sobel(self):
        start_time = time.time()

        original_pixels = self.image

        h = math.floor(self.L / 2)
        self.mid = h

        max_idx_width = self.image.shape[0] - 1
        max_idx_height = self.image.shape[1] - 1

        # https://stackoverflow.com/questions/40709519/initialize-64-by-64-numpy-of-0-0-tuples-in-python
        value = np.empty((), dtype=object)
        value[()] = (0, 0)
        new_pixels = np.full(self.image.shape, value, dtype=object)

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

        elapsed_time = time.time() - start_time
        print(f'ELAPSED TIME: {elapsed_time}')
        return new_pixels

    def _get_gradient(self, angle):
        if angle == 45:
            gradient = [(1, 1), (-1, -1)]
        elif angle == 90:
            gradient = [(0, 1), (0, -1)]
        elif angle == 135:
            gradient = [(-1, 1), (1, -1)]
        else:  # angle == 0
            gradient = [(-1, 0), (1, 0)]

        return gradient

    def _in_bounds(self, x, y, dx, dy):
        return (self.image.shape[1] > x + dx >= 0) and \
               (self.image.shape[0] > y + dy >= 0)

    def supress_non_maxima(self, angle_matrix):
        for x, y in np.ndindex(self.image.shape):
            mod, angle = angle_matrix[y][x]

            gradient = self._get_gradient(angle)

            flag = True
            for delta_x, delta_y in gradient:
                if self._in_bounds(x, y, delta_x, delta_y):
                    displaced_mod = angle_matrix[y + delta_y][x + delta_x][0]
                    if displaced_mod >= mod:
                        flag = False
                    if displaced_mod == mod:
                        angle_matrix[y][x] = (0, angle_matrix[y + delta_y][x + delta_x][1])

            self.image[y, x] = round(mod) if flag else 0

    def apply_hysteresis_threshold(self, t1, t2):
        deltas = [(i, j) for i in range(-1, 1 + 1) for j in range(-1, 1 + 1) if i != 0 or j != 0]
        for x, y in np.ndindex(self.image.shape):
            if self.image[y, x] <= t1:
                self.image[y, x] = 0
            elif self.image[y, x] >= t2:
                self.image[y, x] = 255
            else:
                self.image[y, x] = 0
                for delta_x, delta_y in deltas:
                    if ((self._in_bounds(x, y, delta_x, delta_y)) and
                            self.image[y + delta_y, x + delta_x] >= t2):
                        self.image[y, x] = 255
