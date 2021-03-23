from PIL import Image
import numpy as np
import math

# Filter that does not apply anything to the image
class Filter():

    def __init__(self, L, image):
        self.image = image
        self.imageShape = np.asarray(image).shape
        self.L = L

    # Must override this method
    def compute(self, pixels, x, y):
        return pixels[x,y]

    def apply(self):
        # Just in case we keep the original
        img = self.image.copy()
        pixels = img.load()

        h = math.floor(self.L/2)
        self.mid = h

        max_idx_width = self.imageShape[1]-1
        max_idx_height = self.imageShape[0]-1
        for x,y in np.ndindex(img.size):
            if x-h < 0 or \
               y-h < 0 or \
               x+h > max_idx_width or \
               y+h > max_idx_height:
                # We wont do anything at borders
                pass
            else:
                pixels[x,y] = self.compute(pixels, x, y)
        
        return img


class MeanFilter(Filter):

    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                val = val + pixels[x+x_index, y+y_index]
        val = val/(self.L ** 2)

        # # TODO: check if taking the ceil is ok
        return int(math.ceil(val))


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

image = Image.open('data/TEST.PGM')
image.show()

#mean_filter = MeanFilter(3, image)
#mean_result = mean_filter.apply()

#mean_result.show()

#median_filter = MedianFilter(5, image)
#median_result = median_filter.apply()

#median_result.show()