import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def hdisplay(images,rows, cols, titles, cmap=None):
    width=10
    height=10
    axes=[]
    fig=plt.figure()
    plt.axis('off')
    counter = 1
    for image,title in zip(images, titles):
        arr = np.asarray(image)
        axes.append(fig.add_subplot(rows, cols, counter))
        subplot_title=(title)
        axes[-1].set_title(subplot_title)
        plt.imshow(arr) if cmap is None else plt.imshow(arr, cmap=cmap)
        counter+=1

    plt.show()
