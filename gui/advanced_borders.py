from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox
)
from utils import (
    newButton,
    display_before_after,
)
from display import hdisplay
from filters import (
    GaussianFilter,
    PrewittFilter,
    SobelFilter,
)

class AdvancedBordersTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape


        # Harris Widgets
        self.harris = QLabel("Harris Method")
        self.harris.setStyleSheet("background-color: #ccccff")
        # self.t1_label, self.t1_input = QLabel("t1"), QLineEdit()
        # self.t1_input.setText("70")
        self.harris_btn = newButton("Apply", self.onHarrisClick)
        self.max_label, self.max_input = QLabel("Max:"), QLineEdit()
        self.max_input.setText("0.001")

        self.max_label2, self.max_input2 = QLabel("Avg:"), QLineEdit()
        self.max_input2.setText("100000000")

        # We add widgets to layout
        self.layout.addWidget(self.harris, 0, 0)
        self.layout.addWidget(self.harris_btn, 0, 5)
        self.layout.addWidget(self.max_label, 0, 1)
        self.layout.addWidget(self.max_input, 0, 2)
        self.layout.addWidget(self.max_label2, 0, 3)
        self.layout.addWidget(self.max_input2, 0, 4)
        self.setLayout(self.layout)


    def onHarrisClick(self):
        self.image = self.parent.changes[-1]

        if len(self.imageShape) == 3:
            print("ERROR, RGB IMAGE DETECTED")
            return

        prewitt_dx = PrewittFilter(self.image, mode="dx").apply()
        prewitt_dy = PrewittFilter(self.image, mode="dy").apply()


        i_xx = GaussianFilter(np.square(prewitt_dx), sigma=2, L=7).apply()
        i_yy = GaussianFilter(np.square(prewitt_dy), sigma=2, L=7).apply()

        i_xy = GaussianFilter(np.multiply(prewitt_dx, prewitt_dy), sigma=2, L=7).apply()

        k = 0.04
        R = (i_xx * i_yy - np.square(i_xy)) - k * np.square((i_xx + i_yy))

        Ravg = (R-np.min(R))/np.ptp(R)
        Ravg = Ravg.mean()
        max_val = float(self.max_input.text())
        max_val2 = float(self.max_input2.text())


        # Esta umbralización hay un problema, habría que superponerla con la imágen para que
        # muestre las esquinas. Según Juli con un valor > 0 vale para que sea esquina. Pero 0 no es
        # un buen valor porque hace las esquinas mnuy gruesas (ver la grabación de la última clase).
        # Podríamos poner el umbral como parámetro para probar

        #umbralized = np.array([list(map(lambda x: 255 if x > max_val*np.max(R) else 0, col)) for col in R])
        fig, ax = plt.subplots(ncols = 2)

        X = []
        Y = []

        X2 = []
        Y2 = []

        for x,y in np.ndindex(self.image.shape):
            if(R[x][y] > max_val2*Ravg):
                X.append(y)
                Y.append(x)
            if(R[x][y] > max_val*np.max(R)):
                X2.append(y)
                Y2.append(x)

        ax[0].imshow(self.parent.changes[-1], cmap='gray')
        ax[0].scatter(X2,Y2,1,c='green')
        ax[1].imshow(self.parent.changes[-1], cmap='gray')
        ax[1].scatter(X,Y,1,c='red')
        fig.show()

