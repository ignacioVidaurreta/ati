RAW = 'raw'
PGM = 'pgm'
PPM = 'ppm'


def get_file_type(file):
    ext = file.split('.')[-1].lower()
    if ext not in [RAW, PGM, PPM]:
        #TODO: this should be nicer
        raise Exception('Wrong file extension. Must be .raw, .pgm or .ppm')
    return ext