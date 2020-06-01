import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

form_class=uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.okBtn.clicked.connect(self.btn_clicked)
    
    def btn_clicked(self):
        QMessageBox.about(self, "message", "clicked")

if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
