# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton

#X Y Width Height

class Ui_Dialog(QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 500)
        Dialog.setAcceptDrops(True)
        self.buttonOpen = QtWidgets.QPushButton(Dialog)
        self.buttonOpen.setText("Upload Image")
        self.buttonOpen.setGeometry(QtCore.QRect(230, 40, 112, 25))
        self.buttonOpen.clicked.connect(self.uploadImage)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(230, 90, 112, 25))
        self.pushButton.setObjectName("pushButton")
        #self.label = QtWidgets.QLabel(Dialog)
        #self.label.setGeometry(QtCore.QRect(20, 40, 101, 17))
        #self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(245, 130, 112, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(245, 160, 112, 23))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "File Uploader"))
        self.pushButton.setText(_translate("Dialog", "Analyze Image"))
        #self.label.setText(_translate("Dialog", "Select Image:"))
        self.radioButton.setText(_translate("Dialog", "By pixel"))
        self.radioButton_2.setText(_translate("Dialog", "By square"))

    def uploadImage(self):
        global img
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PGM (*.pgm);;PPM (*.ppm);;RAW (*.raw);;PNG (*.png)", options=options)
        img = cv2.imread(file)
        if img is not None:
            cv2.imshow("Selected Image", img)

#from qgis import gui

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

