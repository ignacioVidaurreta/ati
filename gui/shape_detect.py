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
    numpy_to_pil_image,
    TRANSFORMATION_FOLDER
)
from display import hdisplay
from filters import (
    GaussianFilter,
    PrewittFilter,
    SobelFilter,
    DirectionalFilter,
    LaplacianFilter,
    ZeroCrosses,
    LOGFilter,
    VER,
    HOR,
    DIAG1,
    DIAG2,
    SusanFilter
)

from canny import CannyCustomFilter

class ShapeDetectTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape

        # Prewitt Widgets
        self.prewitt = QLabel("Prewitt Method")
        self.prewitt.setStyleSheet("background-color: #ccccff")
        self.prewitt_filter = newButton("Apply", self.onPrewittClick)

        # Sobel Widgets
        self.sobel = QLabel("Sobel Method")
        self.sobel.setStyleSheet("background-color: #ccccff")
        self.sobel_filter = newButton("Apply", self.onSobelClick)

        # Directional Widgets
        self.directional = QLabel("Directional Method")
        self.directional.setStyleSheet("background-color: #ccccff")
        self.directional_filter = newButton("Apply", self.onDirectionalClick)

        self.exploded_directional = QLabel("Exploded Directional Method")
        self.exploded_directional.setStyleSheet("background-color: #ccccff")
        self.exploded_directional_filter = newButton("Apply", self.onExplodedDirectionalClick)

        # Laplacian Widgets
        self.laplacian = QLabel("Laplacian Method")
        self.laplacian.setStyleSheet("background-color: #ccccff")
        self.laplacian_filter = newButton("Apply", self.onLaplacianClick)

        # Slope Widgets
        self.slope = QLabel("Laplacian with Slope")
        self.slope.setStyleSheet("background-color: #ccccff")
        self.umbral_label, self.umbral_input = QLabel("Umbral"), QLineEdit()
        self.join_label, self.join_input = QLabel("Join"), QLineEdit('union')
        self.umbral_input.setText('100')
        self.slope_evaluation = newButton("Apply", self.onSlopeClick)

        # LOG Widgets
        self.log = QLabel("Laplacian of Gaussian")
        self.log.setStyleSheet("background-color: #ccccff")
        self.log_filter = newButton("Apply", self.onLOGClick)
        self.sigma_label, self.sigma_input = QLabel("Sigma"), QLineEdit('1')
        self.auto_mask = newButton("Automatic Mask", self.onAutoMaskClick)
        self.log_mask, self.log_mask_input = QLabel("Mask Side"), QLineEdit()
        self.log_umbral_label, self.log_umbral_input = QLabel("Umbral"), QLineEdit('0')

        # We add widgets to layout
        self.layout.addWidget(self.prewitt, 0, 0)
        self.layout.addWidget(self.prewitt_filter, 0, 1)

        self.layout.addWidget(self.sobel, 1, 0)
        self.layout.addWidget(self.sobel_filter, 1, 1)

        self.layout.addWidget(self.directional, 2, 0)
        self.layout.addWidget(self.directional_filter, 2, 1)

        self.layout.addWidget(self.exploded_directional, 2, 2)
        self.layout.addWidget(self.exploded_directional_filter, 2, 3)

        self.layout.addWidget(self.laplacian, 3, 0)
        self.layout.addWidget(self.laplacian_filter, 3, 1)

        self.layout.addWidget(self.slope, 4, 0)
        self.layout.addWidget(self.umbral_label, 4, 1)
        self.layout.addWidget(self.umbral_input, 4, 2)
        self.layout.addWidget(self.join_label, 4, 3)
        self.layout.addWidget(self.join_input, 4, 4)
        self.layout.addWidget(self.slope_evaluation, 4, 5)

        self.layout.addWidget(self.log, 5, 0)
        self.layout.addWidget(self.log_umbral_label, 5, 1)
        self.layout.addWidget(self.log_umbral_input, 5, 2)
        self.layout.addWidget(self.sigma_label, 5, 3)
        self.layout.addWidget(self.sigma_input, 5, 4)
        self.layout.addWidget(self.auto_mask, 5, 5)
        self.layout.addWidget(self.log_mask, 5, 6)
        self.layout.addWidget(self.log_mask_input, 5, 7)
        self.layout.addWidget(self.log_filter, 5, 8)

        self.setLayout(self.layout)

    def onPrewittClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = PrewittFilter(r)
            filter_g = PrewittFilter(g)
            filter_b = PrewittFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            prewitt_filter = PrewittFilter(image)
            np_img = prewitt_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Prewitt Filter'
        )

    def onSobelClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = SobelFilter(r)
            filter_g = SobelFilter(g)
            filter_b = SobelFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            sobel_filter = SobelFilter(image)
            np_img = sobel_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Sobel Filter'
        )

    def onPrewittClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = PrewittFilter(r)
            filter_g = PrewittFilter(g)
            filter_b = PrewittFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            prewitt_filter = PrewittFilter(image)
            np_img = prewitt_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Prewitt Filter'
        )

    def onDirectionalClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            filter_r = DirectionalFilter(r)
            filter_g = DirectionalFilter(g)
            filter_b = DirectionalFilter(b)

            r_result = filter_r.apply(normalize=True)
            g_result = filter_g.apply(normalize=True)
            b_result = filter_b.apply(normalize=True)

            np_img = (r_result, g_result, b_result)
        else:
            directional_filter = DirectionalFilter(image)
            np_img = directional_filter.apply(normalize=True)

        display_before_after(
            self.parent,
            np_img,
            f'Directional Filter'
        )

    def onExplodedDirectionalClick(self):
        image = self.parent.changes[-1]
        modes = [VER, HOR, DIAG1, DIAG2]
        created_images = []
        for mode in modes:
            if len(self.imageShape) == 3:

                r,g,b = image[0], image[1], image[2]

                filter_r = DirectionalFilter(r, mode=mode)
                filter_g = DirectionalFilter(g, mode=mode)
                filter_b = DirectionalFilter(b, mode=mode)

                r_result = filter_r.apply(normalize=True)
                g_result = filter_g.apply(normalize=True)
                b_result = filter_b.apply(normalize=True)

                np_img = (r_result, g_result, b_result)
            else:
                directional_filter = DirectionalFilter(image, mode=mode)
                np_img = directional_filter.apply(normalize=True)

            created_images.append(np_img)

        cmap = None if self.imageShape == 3 else "gray"
        hdisplay(created_images, rows=2, cols=2, titles=modes, cmap=cmap)

    def onLaplacianClick(self):
        zero_crosses = ZeroCrosses()

        image = self.parent.changes[-1]

        def process_color(color, zero_crosses):
            laplacian = LaplacianFilter(color)
            result = laplacian.apply()
            return zero_crosses.apply(result)

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            np_img = (
                process_color(r, zero_crosses),
                process_color(g, zero_crosses),
                process_color(b, zero_crosses)
            )
        else:
            np_img = process_color(image, zero_crosses)

        display_before_after(
            self.parent,
            np_img,
            f'Laplacian Method'
        )

    def onSlopeClick(self):
        zero_crosses = ZeroCrosses()

        self.umbral = int(self.umbral_input.text())
        self.join = self.join_input.text()

        image = self.parent.changes[-1]

        def process_color(color, zero_crosses):
            laplacian = LaplacianFilter(color)
            result = laplacian.apply()
            return zero_crosses.apply(result, umbral=self.umbral, join=self.join)

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            np_img = (
                process_color(r, zero_crosses),
                process_color(g, zero_crosses),
                process_color(b, zero_crosses)
            )
        else:
            np_img = process_color(image, zero_crosses)

        display_before_after(
            self.parent,
            np_img,
            f'Laplacian with {self.join} and umbral:{self.umbral}'
        )

    def onLOGClick(self):
        self.sigma = int(self.sigma_input.text())
        self.log_L = int(self.log_mask_input.text())
        self.umbral = int(self.log_umbral_input.text())

        zero_crosses = ZeroCrosses()
        image = self.parent.changes[-1]

        def process_color(color):
            log_filter = LOGFilter(color, self.sigma)
            result = log_filter.apply()
            return zero_crosses.apply(result, umbral=self.umbral, join='union')

        if len(self.imageShape) == 3:

            r,g,b = image[0], image[1], image[2]

            np_img = (
                process_color(r),
                process_color(g),
                process_color(b)
            )
        else:
            np_img = process_color(image)

        display_before_after(
            self.parent,
            np_img,
            f'LOG, \u03C3:{self.sigma}, mask side:{self.log_L}'
        )

    def onAutoMaskClick(self):
        self.sigma = int(self.sigma_input.text())
        self.L = 6*self.sigma+1
        self.log_mask_input.setText(str(self.L))


class ModernShapeDetectTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.layout = QGridLayout(parent)

        self.imageShape = np.asarray(self.parent.image).shape

        # SUSAN Widgets
        self.susan = QLabel("Susan Method")
        self.susan.setStyleSheet("background-color: #ccccff")
        self.susan_cb = QComboBox()
        self.susan_cb.addItems(["Borders", "Corners", "All"])
        self.susan_filter = newButton("Apply", self.onSusanClick)

        # Canny Widgets
        self.canny = QLabel("Canny Method")
        self.canny.setStyleSheet("background-color: #ccccff")
        self.canny_filter = newButton("Apply", self.onCannyClick)

        # We add widgets to layout
        self.layout.addWidget(self.canny, 0, 0)
        self.layout.addWidget(self.canny_filter, 0, 1)
        self.layout.addWidget(self.susan, 1, 0)
        self.layout.addWidget(self.susan_cb, 1, 1)
        self.layout.addWidget(self.susan_filter, 1, 2)

        self.setLayout(self.layout)

    def onSusanClick(self):
        image = self.parent.changes[-1]

        if len(self.imageShape) == 3:
            print("ERROR: Showing Color image instead of B&W image")
        else:
            susan_filter = SusanFilter(image, self.susan_cb.currentText())
            np_img = susan_filter.apply(normalize=False)

            img = Image.fromarray(np_img).convert("RGB").copy()
            pixels = img.load()
            for x, y in np.ndindex(img.size):
                if np_img[x][y] == -255:
                    pixels[y, x] = (255, 0, 0)
                elif np_img[x][y] == -128:
                    pixels[y, x] = (0, 255, 0)

            # display_before_after(
            #     self.parent,
            #     np_img,
            #     f'Susan Filter'
            # )
            img.show()

    def onCannyClick(self):
        self.image = self.parent.changes[-1]

        if len(self.imageShape) == 3:
            print("ERROR, RGB IMAGE DETECTED")
        else:

            # We apply the Sobel Filter but a custom version.
            # With the code as it is now, we would need to apply it 2 times, one
            # for the magnitude matrix and one for the angle matrix, so instead
            # we rewrite it to have a matrix of tuples
            canny = CannyCustomFilter(self.image)

            angle_matrix = canny.apply_sobel()
            canny.supress_non_maxima(angle_matrix)
            t1 = 70
            t2 = 150
            canny.apply_hysteresis_threshold(angle_matrix, t1, t2)

            display_before_after(
                self.parent,
                canny.image,
                f"Canny Method"
            )
