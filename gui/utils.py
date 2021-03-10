RAW = 'raw'
PGM = 'pgm'
PPM = 'ppm'

from PIL import Image
import re

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


def read_raw(filename):
    raw_data = open(filename, "rb").read()
    width, height = get_metadata(filename)
    return Image.frombytes('L', (width, height), raw_data)