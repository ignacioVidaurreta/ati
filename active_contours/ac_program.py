import numpy as np
import time
from PIL import Image
from utils import (
    DrawRectangleHandler,
    get_initial_lin_lout,
    get_f, get_neighbours,
    plot_current_image,
    check_termination
)

def initialize(filename, epsilon):
    mode = 'color'

    image = Image.open(filename)
    if len(np.asarray(image).shape) < 3:
        mode = 'bn'

    im_arr = np.asarray(image.convert("RGB"))
    handler = DrawRectangleHandler(im_arr, filename)

    average = handler.average
    if mode == 'bn':
        average = average[0]

    xs = np.arange(handler.x0, handler.x+1, step=1)
    ys = np.arange(handler.y0, handler.y+1, step=1)

    # [STEP 1] mark initial region with a rectangle and define lin and lout

    # [REMEMBER] image is accessed img[y][x]
    # [REMEMBER] both lin and lout are (x,y) points
    lin, lout = get_initial_lin_lout(xs, ys)

    # im_arr shape is [columns, rows, channel]
    # mask is filled with background value
    mask = np.full(shape=(im_arr.shape[0], im_arr.shape[1]), fill_value=3)

    for y in ys:
        for x in xs:
            # point is lin
            if (y, x) in lin:
                mask[y][x] = -1
            # point is inside lin
            elif ys[0] < y < ys[-1] and xs[0] < x < xs[-1]:
                mask[y][x] = -3

    for (y, x) in lout:
        mask[y][x] = 1

    f = get_f(avg_color=average, epsilon=epsilon, mode=mode)

    return average, lin, lout, mask, f, im_arr

def process_frame(lin, lout, mask, f, im_arr, iterations, processed_images, lin_color, full=False):
    t0 = time.process_time()
    for i in range(iterations):

        temporary_louts = []
        temporary_lins = []

        def process_lout_item(x):
            if f(im_arr[x[0]][x[1]]) > 0:  # means pixel is under epsilon distance from avg
                lout.remove(x)
                lin.append(x)  # so it should be lin
                mask[x[0]][x[1]] = -1  # i think this was missing on explanation
                for y in get_neighbours(x, im_arr.shape):
                    if mask[y[0]][y[1]] == 3:  # each neighbour that was background
                        mask[y[0]][y[1]] = 1  # is now lout
                        temporary_louts.append(y)  # so we will append it to lout later

        # [STEP 2]
        for item in lout:
            process_lout_item(item)
        lout.extend(temporary_louts)

        # *** Definition of lin ***
        # x / mask(x) < 0 and exists neigh y such as mask(y) > 0
        def check_if_still_lin(x):
            if mask[x[0]][x[1]] < 0:  # was in lin array
                t = filter(lambda b: b, [mask[y[0]][y[1]] > 0 for y in get_neighbours(x, im_arr.shape)])
                if sum(1 for _ in t) > 0:
                    return  # x verifies lin definition
            lin.remove(x)
            mask[x[0]][x[1]] = -3  # is now object

        # [STEP 3]
        for item in lin:
            check_if_still_lin(item)

        def process_lin_item(x):
            if f(im_arr[x[0]][x[1]]) < 0:  # means pixel is above epsilon distance from avg
                lin.remove(x)
                lout.append(x)  # so it should be lout
                mask[x[0]][x[1]] = 1  # i think this was missing on explanation
                for y in get_neighbours(x, im_arr.shape):
                    if mask[y[0]][y[1]] == -3:  # each neighbour that was object
                        mask[y[0]][y[1]] = -1  # is now lin
                        temporary_lins.append(y)  # so we will append it to lin later

        # [STEP 4]
        for item in lin:
            process_lin_item(item)
        lin.extend(temporary_lins)

        # *** Definition of lout ***
        # x / mask(x) > 0 and exists neigh y such as mask(y) < 0
        def check_if_still_lout(x):
            if mask[x[0]][x[1]] > 0:  # was in lout array
                t = filter(lambda b: b, [mask[y[0]][y[1]] < 0 for y in get_neighbours(x, im_arr.shape)])
                if sum(1 for b in t) > 0:
                    return  # x verifies lin definition
            lout.remove(x)
            mask[x[0]][x[1]] = 3  # is now background

        # [STEP 5]
        for item in lout:
            check_if_still_lout(item)

        if check_termination(im_arr, f, lin, lout):
            break

        if full:
            tmp_image = plot_current_image(im_arr, lin, [], lin_color)
            processed_images.append(tmp_image)

    final_image = plot_current_image(im_arr, lin, [], lin_color)
    processed_images.append(final_image)

    elapsed_time = time.process_time() - t0

    return elapsed_time, lin, lout, mask


def process_video(directory, filenames, lin, lout, mask, f, iterations, processed_images, times, lin_color):

    for filename in filenames:
        filepath = f'{directory}/{filename}'
        im_arr = np.asarray(Image.open(filepath).convert("RGB"))
        elapsed_time, lin, lout, mask = process_frame(
            lin, lout, mask, f, im_arr,
            iterations,
            processed_images,
            lin_color=lin_color,
            full=False
        )
        times.append(elapsed_time)
