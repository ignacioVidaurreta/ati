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
from utils import newButton, newAxisButton

# With self.parent variable we can access information about the application
# - parent.image gives us access to image
#
#

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
        self.valueInput.setValidator(QIntValidator(0, 255))
        
        self.pixelSetError = QLabel('You need to select coordinates first')
        
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

        self.layout.addWidget(self.getValue, 1, 0)

        #self.layout.addWidget(self.placholder, 2, 0)
        
        self.layout.addWidget(self.valueLabel, 3,0)
        self.layout.addWidget(self.valueInput, 3,1)
        self.layout.addWidget(self.setValue, 3, 2)
        
        self.layout.addWidget(self.pixelSetError, 4, 0)

        self.layout.addWidget(self.restart, 5, 0)
        
        self.pixelSetError.hide()

        self.setLayout(self.layout)

    # Convention: on[ButtonName]Click
    def onGetValueClick(self):
        self.value = QLabel(f'{self.getPixel()}')
        self.layout.addWidget(self.value, 1, 1)

    def _parse_set_value(self):
        value_arr = self.valueInput.text().strip().split(" ")
        if len(value_arr) == 1:
            return int(value_arr[0])
        else:
            return int(value_arr[0]), int(value_arr[1]), int(value_arr[2])

    def onSetValueClick(self):
        self.pixelSetError.hide()
        img = self.parent.image
        try:
            value = self._parse_set_value()
            x,y = self._get_xy_coords()
            print(f"Setting pixel value to {value}")
            
            return img.putpixel((x,y), value)
    
        except:
            self.pixelSetError.show()
            print('Pixel cannot be set.')


    def onRestartClick(self):
        self.pixelSetError.hide()
        self.valueInput.setText(None)
        if hasattr(self, 'value'):
            self.layout.removeWidget(self.value)
            self.value.deleteLater()
            self.xInput.setText(None)
            self.yInput.setText(None)
            if self.imageShape == 3:
                self.zInput.setText(None)

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
