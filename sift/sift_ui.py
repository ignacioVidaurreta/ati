import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from sift import run_sift

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(849, 607)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.chooseImage1Button = QtWidgets.QPushButton(self.centralwidget)
        self.chooseImage1Button.setGeometry(QtCore.QRect(40, 20, 121, 31))
        self.chooseImage1Button.setStyleSheet("background-color: rgb(135, 223, 232);")
        self.chooseImage1Button.setObjectName("chooseImage1Button")
        self.featuresInput = QtWidgets.QTextEdit(self.centralwidget)
        self.featuresInput.setGeometry(QtCore.QRect(40, 210, 191, 31))
        self.featuresInput.setObjectName("featuresInput")
        self.featuresLabel = QtWidgets.QLabel(self.centralwidget)
        self.featuresLabel.setGeometry(QtCore.QRect(40, 180, 91, 17))
        self.featuresLabel.setObjectName("featuresLabel")
        self.octaveLayersInput = QtWidgets.QTextEdit(self.centralwidget)
        self.octaveLayersInput.setGeometry(QtCore.QRect(40, 280, 191, 31))
        self.octaveLayersInput.setObjectName("octaveLayersInput")
        self.octaveLayersLabel = QtWidgets.QLabel(self.centralwidget)
        self.octaveLayersLabel.setGeometry(QtCore.QRect(40, 250, 131, 17))
        self.octaveLayersLabel.setObjectName("octaveLayersLabel")
        self.restartButton = QtWidgets.QPushButton(self.centralwidget)
        self.restartButton.setGeometry(QtCore.QRect(340, 490, 131, 31))
        self.restartButton.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(238, 238, 236);")
        self.restartButton.setObjectName("restartButton")
        self.chooseImage2Button = QtWidgets.QPushButton(self.centralwidget)
        self.chooseImage2Button.setGeometry(QtCore.QRect(40, 60, 121, 31))
        self.chooseImage2Button.setStyleSheet("background-color: rgb(135, 223, 232);")
        self.chooseImage2Button.setObjectName("chooseImage2Button")
        self.resultSiftText = QtWidgets.QTextEdit(self.centralwidget)
        self.resultSiftText.setGeometry(QtCore.QRect(340, 440, 431, 31))
        self.resultSiftText.setStyleSheet("background-color: rgb(211, 215, 207);")
        self.resultSiftText.setObjectName("resultSiftText")
        self.initSiftButton = QtWidgets.QPushButton(self.centralwidget)
        self.initSiftButton.setGeometry(QtCore.QRect(340, 400, 141, 25))
        self.initSiftButton.setStyleSheet("background-color: rgb(250, 176, 243);")
        self.initSiftButton.setObjectName("initSiftButton")
        self.contrastThresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.contrastThresholdLabel.setGeometry(QtCore.QRect(40, 320, 131, 17))
        self.contrastThresholdLabel.setObjectName("contrastThresholdLabel")
        self.contrastThresholdInput = QtWidgets.QTextEdit(self.centralwidget)
        self.contrastThresholdInput.setGeometry(QtCore.QRect(40, 350, 191, 31))
        self.contrastThresholdInput.setObjectName("contrastThresholdInput")
        self.edgeThresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.edgeThresholdLabel.setGeometry(QtCore.QRect(40, 390, 131, 17))
        self.edgeThresholdLabel.setObjectName("edgeThresholdLabel")
        self.edgeThresholdInput = QtWidgets.QTextEdit(self.centralwidget)
        self.edgeThresholdInput.setGeometry(QtCore.QRect(40, 420, 191, 31))
        self.edgeThresholdInput.setObjectName("edgeThresholdInput")
        self.sigmaLabel = QtWidgets.QLabel(self.centralwidget)
        self.sigmaLabel.setGeometry(QtCore.QRect(40, 460, 131, 17))
        self.sigmaLabel.setObjectName("sigmaLabel")
        self.sigmaInput = QtWidgets.QTextEdit(self.centralwidget)
        self.sigmaInput.setGeometry(QtCore.QRect(40, 490, 191, 31))
        self.sigmaInput.setObjectName("sigmaInput")
        self.ratioLabel = QtWidgets.QLabel(self.centralwidget)
        self.ratioLabel.setGeometry(QtCore.QRect(340, 180, 131, 17))
        self.ratioLabel.setObjectName("ratioLabel")
        self.ratioInput = QtWidgets.QTextEdit(self.centralwidget)
        self.ratioInput.setGeometry(QtCore.QRect(340, 210, 191, 31))
        self.ratioInput.setObjectName("ratioInput")
        self.percentageLabel = QtWidgets.QLabel(self.centralwidget)
        self.percentageLabel.setGeometry(QtCore.QRect(340, 250, 131, 17))
        self.percentageLabel.setObjectName("percentageLabel")
        self.percentageInput = QtWidgets.QTextEdit(self.centralwidget)
        self.percentageInput.setGeometry(QtCore.QRect(340, 280, 191, 31))
        self.percentageInput.setObjectName("percentageInput")
        self.siftParametersTitle = QtWidgets.QLabel(self.centralwidget)
        self.siftParametersTitle.setGeometry(QtCore.QRect(40, 140, 191, 17))
        self.siftParametersTitle.setObjectName("siftParametersTitle")
        self.decisionParametersTitle = QtWidgets.QLabel(self.centralwidget)
        self.decisionParametersTitle.setGeometry(QtCore.QRect(340, 140, 191, 17))
        self.decisionParametersTitle.setObjectName("decisionParametersTitle")
        self.file1text = QtWidgets.QTextEdit(self.centralwidget)
        self.file1text.setGeometry(QtCore.QRect(180, 20, 251, 31))
        self.file1text.setStyleSheet("background-color: rgb(211, 215, 207);")
        self.file1text.setObjectName("file1text")
        self.file2text = QtWidgets.QTextEdit(self.centralwidget)
        self.file2text.setGeometry(QtCore.QRect(180, 60, 251, 31))
        self.file2text.setStyleSheet("background-color: rgb(211, 215, 207);")
        self.file2text.setObjectName("file2text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 849, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # custom #
        self.set_functions()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chooseImage1Button.setText(_translate("MainWindow", "Choose Image 1"))
        self.featuresInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>"))
        self.featuresLabel.setText(_translate("MainWindow", "n features"))
        self.octaveLayersInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3</p></body></html>"))
        self.octaveLayersLabel.setText(_translate("MainWindow", "n octave layers"))
        self.restartButton.setText(_translate("MainWindow", "Restart"))
        self.chooseImage2Button.setText(_translate("MainWindow", "Choose Image 2"))
        self.initSiftButton.setText(_translate("MainWindow", "Run SIFT Analysis"))
        self.contrastThresholdLabel.setText(_translate("MainWindow", "contrast threshold"))
        self.contrastThresholdInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.04</p></body></html>"))
        self.edgeThresholdLabel.setText(_translate("MainWindow", "edge threshold"))
        self.edgeThresholdInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">10</p></body></html>"))
        self.sigmaLabel.setText(_translate("MainWindow", "sigma"))
        self.sigmaInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.6</p></body></html>"))
        self.ratioLabel.setText(_translate("MainWindow", "ratio"))
        self.ratioInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.7</p></body></html>"))
        self.percentageLabel.setText(_translate("MainWindow", "percentage"))
        self.percentageInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.25</p></body></html>"))
        self.siftParametersTitle.setText(_translate("MainWindow", "SIFT PARAMETERS"))
        self.decisionParametersTitle.setText(_translate("MainWindow", "DECISION PARAMETERS"))

    def set_functions(self):
        self.restartButton.clicked.connect(self.restart_program)
        self.chooseImage1Button.clicked.connect(self.upload_image_1)
        self.chooseImage2Button.clicked.connect(self.upload_image_2)
        self.initSiftButton.clicked.connect(self.run_sift_analysis)

    def restart_program(self):
        self.file1 = None
        self.file2 = None
        self.file1text.setText('')
        self.file2text.setText('')
        self.featuresInput.setText('0')
        self.octaveLayersInput.setText('3')
        self.contrastThresholdInput.setText('0.04')
        self.edgeThresholdInput.setText('10')
        self.sigmaInput.setText('1.6')
        self.ratioInput.setText('0.7')
        self.percentageInput.setText('0.25')
        self.resultSiftText.setText('')

    def upload_image_1(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Choose image")
        self.file1 = file
        self.file1text.setText(self.file1.split("/")[-1])

    def upload_image_2(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Choose image")
        self.file2 = file
        self.file2text.setText(self.file2.split("/")[-1])

    def run_sift_analysis(self):
        result = run_sift(
                int(self.featuresInput.toPlainText()),
                int(self.octaveLayersInput.toPlainText()),
                float(self.contrastThresholdInput.toPlainText()),
                float(self.edgeThresholdInput.toPlainText()),
                float(self.sigmaInput.toPlainText()),
                float(self.ratioInput.toPlainText()),
                float(self.percentageInput.toPlainText()),
                self.file1,
                self.file2)
        self.resultSiftText.setText(result)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
