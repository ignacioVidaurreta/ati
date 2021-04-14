RAW = 'raw'
PGM = 'pgm'
PPM = 'ppm'

from PIL import Image
import re
import numpy as np
from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QFormLayout,
    QLabel,
    QLineEdit
)
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, QSize

METADATA_FILE="data/info.txt"
TRANSFORMATION_FOLDER = 'transformations'


def get_file_type(file):
    ext = file.split('.')[-1].lower()
    return ext

def read_image(filename):
    return Image.open(filename)

# img must be PIL Image
def save_image(img: Image, filepath):
    return img.save(filepath)

def get_metadata(filename):
    relative_name = filename.split("/")[-1]
    with open(METADATA_FILE, "r") as fd:
        lines = fd.readlines()[2:] # We don't care about the header or the blank line
        for line in lines:
            # A bit overloaded line: this removes repeated whitespaces,
            # removes the trailing newline and finally creates the array
            # with words separated by " "
            tmp = re.sub(" +", " ", line.rstrip()).split(" ")
            if tmp[0].lower() == relative_name.lower():
                return int(tmp[1]), int(tmp[2])

    raise Exception(f"Missing Metadata information for {filename} in {METADATA_FILE} ")

def read_raw(filename):
    raw_data = open(filename, "rb").read()
    width, height = get_metadata(filename)
    return Image.frombytes('L', (width, height), raw_data)

def save_raw(img: Image, filename, folder, height, width):
    # Process of saving image
    filepath = f'{folder}/{filename}'
    imagefile = open(filepath, "wb")
    bytesArray = bytearray(np.asarray(img))
    imagefile.write(bytesArray)
    imagefile.close()

    # Process of appending dimensios to info.txt
    with open('./data/info.txt', 'a') as f:
        f.write(f'{filename}   {width}   {height}\n')

def newButton(label, function):
    button = QPushButton(label)
    button.clicked.connect(function)
    return button

def newAxisButton(label, maxValue):
    axisLabel = QLabel(f'{label}: ')
    axisInput = QLineEdit()
    axisInput.setValidator(QIntValidator(0, maxValue))
    return axisLabel, axisInput

def crop_image(img, x, y, w, h):
    arr = np.array(img)
    img.show()
    x1, y1 = x + w, y + h
    img = Image.fromarray(arr[y:y1, x:x1])
    img.show()

def copy_crop_into_img(img, x, y, w, h):
    # This is the other image
    # the one you paste the square/rectangle on
    # (you will get the square/rectangle from self.parent.image)
    a = read_raw("data/GIRL.RAW")
    arr_from = np.array(img) # image to matrix
    arr_to  = np.array(a) # image to matrix
    x1, y1 = x + w, y + h
    arr_to[y:y1, x:x1] = arr_from[y:y1, x:x1] # This should be the whole image but JIC
    img.show()
    img = Image.fromarray(arr_to)
    img.show()

def compute_histogram(img, imageShape):
    pixels = img.load()

    # We initialize 256 bins in 0, this array will hold
    # relative frequencies
    histogram = np.zeros(256)

    # Computes relative frequencies
    for x,y in np.ndindex(img.size):
        current = histogram[pixels[x,y]]
        histogram[pixels[x,y]] = current + 1

    total = imageShape[0]*imageShape[1]
    histogram = histogram/total

    return histogram


# This can be either a matrix or a 3 element tuple
# (r,g,b) each one with a matrix inside
def numpy_to_pil_image(numpy_image):
    if len(numpy_image) == 3:
        r_pil = Image.fromarray(numpy_image[0].astype(np.uint8))
        g_pil = Image.fromarray(numpy_image[1].astype(np.uint8))
        b_pil = Image.fromarray(numpy_image[2].astype(np.uint8))
        result_pil_image = Image.merge("RGB", (r_pil, g_pil, b_pil))
    else:
        result_pil_image = Image.fromarray(numpy_image.astype(np.uint8))
    return result_pil_image

def numpy_to_pil_image(numpy_image):
    if len(numpy_image) == 3:
        r_pil = Image.fromarray(numpy_image[0].astype(np.uint8))
        g_pil = Image.fromarray(numpy_image[1].astype(np.uint8))
        b_pil = Image.fromarray(numpy_image[2].astype(np.uint8))
        result_pil_image = Image.merge("RGB", (r_pil, g_pil, b_pil))
    else:
        result_pil_image = Image.fromarray(numpy_image.astype(np.uint8))
    return result_pil_image
