import sys
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

# With self.parent variable we can access information about the application
# - parent.image gives us access to image
#
#

# Some helper methods
def newButton(label, function):
    button = QPushButton(label)
    button.clicked.connect(function)
    return button

def newAxisButton(label, maxValue):
    axisLabel = QLabel(f'{label}: ')
    axisInput = QLineEdit()
    axisInput.setValidator(QIntValidator(0, maxValue))
    return axisLabel, axisInput

class PixelTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.image = np.asarray(self.parent.image)
        self.imageShape = self.image.shape

        # Widgets definition
        self.xLabel, self.xInput = newAxisButton('X', self.imageShape[0])
        self.yLabel, self.yInput = newAxisButton('Y', self.imageShape[1])
        self.valueLabel = QLabel(f'Value: ')
        self.valueInput = QLineEdit()

        # Buttons definitions
        self.setValue = newButton("SET", self.onSetValueClick)
        self.getValue = newButton("GET", self.onGetValueClick)
        self.restart = newButton("RESTART", self.onRestartClick)

        # We add widgets to layout
        self.layout.addWidget(self.xLabel, 0, 0)
        self.layout.addWidget(self.xInput, 0, 1)
        self.layout.addWidget(self.yLabel, 0, 2)
        self.layout.addWidget(self.yInput, 0, 3)
        if len(self.imageShape) == 3:
            self.layout.addWidget(self.yLabel, 0, 4)
            self.layout.addWidget(self.yInput, 0, 5)
        self.layout.addWidget(self.getValue, 1, 1)
        self.layout.addWidget(self.restart, 1, 3)
        self.layout.addWidget(self.valueLabel, 3,0)
        self.layout.addWidget(self.valueInput, 3,1)
        self.layout.addWidget(self.setValue, 3, 2)

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onGetValueClick(self):
        self.value = QLabel(f'{self.getPixel()}')
        self.layout.addWidget(self.value, 2, 0)

    def _parse_set_value(self):
        value_arr = self.valueInput.text().strip().split(" ")
        if len(value_arr) == 1:
            return int(value_arr[0])
        else:
            return int(value_arr[0]), int(value_arr[1]), int(value_arr[2])

    def onSetValueClick(self):
        img = self.parent.image
        value = self._parse_set_value()
        x,y = self._get_xy_coords()
        print(f"Setting pixel value to {value}")

        return img.putpixel((x,y), value)

    def onRestartClick(self):
        if hasattr(self, 'value'):
            self.layout.removeWidget(self.value)
            self.value.deleteLater()

    def _get_xy_coords(self):
        x = int(self.xInput.text())
        y = int(self.yInput.text())

        return x,y

    def getPixel(self):
        img = self.parent.image
        x,y = self._get_xy_coords()

        return img.getpixel((x,y))

    def putPixel(self):
        img = self.parent.image
        x, y, z = self._get_xyz_coords()
