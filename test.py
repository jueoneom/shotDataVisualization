import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

form_class=uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.figure=Figure(figsize=(6,7))
        self.canvas=FigureCanvas(self.figure)
        self.toolBar=NavigationToolbar(self.canvas, self)
        # self.okBtn.clicked.connect(self.btn_clicked)
    
    def btn_clicked(self):
        QMessageBox.about(self, "message", "clicked")

if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
