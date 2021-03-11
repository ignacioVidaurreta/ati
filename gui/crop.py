import sys
import numpy as np
import cv2
import pandas as pd
from PIL import Image

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
from utils import newButton, newAxisButton


class CropTab(QWidget):
    AVG_PIX_TEXT="Average Pixel:"
    TOT_PIX_TEXT="Total Pixels:"
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.img = self.image.copy()
        self.imageShape = self.image.shape
        self.inspectImage = newButton("INSPECT", self.onInspectImageClick)

        # Results labels
        self.averagePixelLabel = QLabel(self.AVG_PIX_TEXT)
        self.totalPixelsLabel = QLabel(self.TOT_PIX_TEXT)
        self.layout.addWidget(self.inspectImage, 2, 1)
        self.layout.addWidget(self.averagePixelLabel, 0,0)
        self.layout.addWidget(self.totalPixelsLabel, 1,0)
        self.setLayout(self.layout)

        # Initial variables
        self.x0 = -1
        self.y0 = -1
        self.dragging=False
        self.recentClick = False


    def onInspectImageClick(self):
        #abrir ventana aparte para dibujar sobre imagen
        cv2.namedWindow(winname = "Selected Image")
        cv2.setMouseCallback("Selected Image", self.drag_rectangle)
        while True:
            cv2.imshow("Selected Image", self.img)

            #Sale al apretar esc
            if cv2.waitKey(20) == 27:
                break
        cv2.destroyAllWindows()

    def drag_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragging = True
            self.recentClick = True
            self.x0 = x
            self.y0 = y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.recentClick = False
                # Use a clean copy of image to draw over it
                self.img = self.image.copy()
                cv2.rectangle(self.img, pt1 =(self.x0, self.y0),
                            pt2 =(x, y),
                            color =(0, 255, 0),
                            thickness = 2)

        # Give the information when the user stops drawing
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            if self.recentClick:
                print(f"Selected pixel X: {self.x0} Y: {self.y0} - Value: {self.img[self.x0, self.y0]}")
                self.recentClick = False
                return
            cv2.rectangle(self.img, pt1=(self.x0, self.y0),
                        pt2 =(x, y),
                        color =(0, 255, 0),
                        thickness = 2)
            #obtengo el sample, me fijo de que lado vino la seleccion
            if(y<self.y0):
                aux = y
                y = self.y0
                self.y0 = aux
            if(x<self.x0):
                aux = x
                x = self.x0
                self.x0 = aux
            sample = self.img[self.y0:y, self.x0:x]

            average = sample.mean(axis=0).mean(axis=0)
            average = average.astype(int)
            pixels = abs((x - self.x0)*(y - self.y0))
            self.totalPixelsLabel.setText(f"{self.TOT_PIX_TEXT} {pixels}")
            if len(self.imageShape) == 3:
                RGB = (average[2], average[1], average[0])
                self.averagePixelLabel.setText(f"{self.AVG_PIX_TEXT} {RGB}")
                # Show average color
                pixel = Image.new(mode = "RGB", size = (100,100), color = RGB)
            else:
                self.averagePixelLabel.setText(f"{self.AVG_PIX_TEXT} {average}")
                pixel = Image.new(mode = "L", size =(100, 100), color=int(average))

            pixel.show()