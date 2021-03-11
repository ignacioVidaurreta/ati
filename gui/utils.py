RAW = 'raw'
PGM = 'pgm'
PPM = 'ppm'

from PIL import Image
import re
import numpy as np

METADATA_FILE="data/info.txt"

def get_file_type(file):
    ext = file.split('.')[-1].lower()
    if ext not in [RAW, PGM, PPM]:
        #TODO: this should be nicer
        raise Exception('Wrong file extension. Must be .raw, .pgm or .ppm')
    return ext

def read_pgm_ppm(filename):
    return Image.open(filename)

def save_pgm(file):
    pass

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

def get_pixel(img, x, y):
    return img.getpixel((x,y))

def set_pixel(img, x, y, value):
    return img.putpixel((x, y), value)

def crop_image(img, x, y, w, h):
    arr = np.array(img)
    img.show()
    x1, y1 = x + w, y + h
    img = Image.fromarray(arr[y:y1, x:x1])
    print(arr[y:y1, x:x1].shape)
    img.show()

def copy_crop_into_img(img, x, y, w, h):
    a = read_raw("data/GIRL.RAW")
    arr_from = np.array(img)
    arr_to  = np.array(a)
    x1, y1 = x + w, y + w
    arr_to[y:y1, x:x1] = arr_from[y:y1, x:x1] # This should be the whole image but JIC
    img.show()
    img = Image.fromarray(arr_to)
    img.show()
