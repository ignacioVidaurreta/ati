from PIL import Image
import numpy as np
import math

# Filter that does not apply anything to the image
class Filter():

    def __init__(self, image, L=3):
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

    def __init__(self, image):
        super().__init__(3, image)

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

        # TODO: check if taking the ceil is ok
        # returns avg of median since qty of elements is even
        return math.ceil((values[7]+values[8])/2)
    
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
                val = val + (weight * pixels[x+x_index, y+y_index])

        # TODO: check if taking the ceil is ok
        return int(math.ceil(val))
    
    def gaussian(self, x, y):
        denominator = math.sqrt(2*math.pi*(self.sigma ** 2))
        exponent = -1*((x ** 2) + (y ** 2))/(self.sigma ** 2)
        return (1/denominator) * math.exp(exponent)


class EnhancementFilter(Filter):
    
    # Must override this method
    def compute(self, pixels, x, y):
        val = 0
        
        for x_index in range(-1*self.mid, self.mid+1):
            for y_index in range(-1*self.mid, self.mid+1):
                weight = self.L ** 2 -1 if x_index == 0 and y_index == 0 else -1
                val = val + (weight * pixels[x+x_index, y+y_index])
    
        val = val/(self.L ** 2)

        # TODO: check if taking the ceil is ok
        return int(math.ceil(val))


image = Image.open('data/TEST.PGM')
image.show()

#mean_filter = MeanFilter(image)
#mean_result = mean_filter.apply()

#mean_result.show()

#median_filter = MedianFilter(image)
#median_result = median_filter.apply()

# weighted_filter = WeightedMedianFilter(image)
# weighted_result = weighted_filter.apply()

# weighted_result.show()

# gaussian_filter = GaussianFilter(image, 2, L=3)
# gaussian_result = gaussian_filter.apply()

# gaussian_result.show()

enhancement_filter = EnhancementFilter(image, L=3)
enhancement_result = enhancement_filter.apply()

enhancement_result.show()