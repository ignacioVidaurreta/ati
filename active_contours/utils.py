import cv2
import numpy as np
from PIL import Image
from constants import *

LOUT_COLOR = (0, 0, 255)

class DrawRectangleHandler:

    def __init__(self, image, filename):
        self.dragging = False
        self.recent_click = False
        self.x0 = -1
        self.y0 = -1
        self.x = -1
        self.y = -1
        self.image = image
        self.img_copy = image.copy()
        self.average = None

        cv2.namedWindow(winname=filename)
        cv2.setMouseCallback(filename, self.draw_rectangle)
        while cv2.waitKey(delay) != escape and self.average is None:
            cv2.imshow(filename, cv2.cvtColor(self.img_copy, cv2.COLOR_BGR2RGB))

    def check_x0_x(self):
        if self.x < self.x0:
            aux = self.x
            self.x = self.x0
            self.x0 = aux

    def check_y0_y(self):
        if self.y < self.y0:
            aux = self.y
            self.y = self.y0
            self.y0 = aux

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragging = True
            self.recent_click = True
            self.x0 = x
            self.y0 = y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.recent_click = False
                self.img_copy = self.image.copy()
                cv2.rectangle(self.img_copy, pt1=(self.x0, self.y0), pt2=(x, y), color=curve_color, thickness=1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            if self.recent_click:
                self.recent_click = False
                print(f"Selected pixel ({self.x0},{self.y0}) with value {self.image[self.x0][self.y0]}")
            else:
                cv2.rectangle(self.img_copy, pt1=(self.x0, self.y0), pt2=(x, y), color=curve_color, thickness=1)
                self.x = x
                self.y = y

                self.check_x0_x()
                self.check_y0_y()

                self.img_copy = self.image.copy()
                sample = self.img_copy[self.y0:y, self.x0:x]
                self.average = sample.mean(axis=0).mean(axis=0)


def get_initial_lin_lout(xs, ys):
    lin = []
    lout = []

    for x in xs:
        lout.append((ys[0] - 1, x))
        lout.append((ys[-1] + 1, x))
        lin.append((ys[0], x))
        lin.append((ys[-1], x))

    for y in ys:
        lout.append((y, xs[0] - 1))
        lout.append((y, xs[-1] + 1))
        if y != ys[0] and y != ys[-1]:
            lin.append((y, xs[0]))
            lin.append((y, xs[-1]))

    return lin, lout


def get_f(avg_color, epsilon, mode='bn'):
    def f(pixel):
        pixel = pixel[0] if mode == 'bn' else pixel
        return 1 if np.linalg.norm(pixel-avg_color) < epsilon else -1
    return f


def get_neighbours(x, shape):
    neighbours = []
    if x[0]-1 > 0:
        neighbours.append((x[0]-1, x[1]))
    if x[1]-1 > 0:
        neighbours.append((x[0], x[1]-1))
    if x[0]+1 < shape[0]:
        neighbours.append((x[0]+1, x[1]))
    if x[1] + 1 < shape[1]:
        neighbours.append((x[0], x[1]+1))
    return neighbours


def plot_current_image(im_arr, lin, lout, lin_color):
    iteration_image = im_arr.copy()
    for (y, x) in lin:
        iteration_image[y][x] = lin_color
    for (y, x) in lout:
        iteration_image[y][x] = LOUT_COLOR
    im = Image.fromarray(iteration_image).convert("RGBA")
    return im


def check_termination(im_arr, f, lin, lout):
    lin_r = sum(1 for _ in filter(lambda y: y < 0, list(map(lambda x: f(im_arr[x[0]][x[1]]), lin))))
    if lin_r > 0:
        return False
    lout_r = sum(1 for _ in filter(lambda y: y > 0, list(map(lambda x: f(im_arr[x[0]][x[1]]), lout))))
    if lout_r > 0:
        return False
    return True
