import sys
import os
from loadFile import read_excel
from graphWidget import GraphWidget
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



form_class=uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.left=10
        self.top=10
        self.title='shotDataVisualization'
        self.width=640
        self.height=400
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.label=self.fileNameLabel
        
        self.figure=plt.Figure()
        self.canvas=FigureCanvas(self.figure)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        
        self.loadFileBtn.clicked.connect(self.loadFile_clicked)
    
    @pyqtSlot()
    def loadFile_clicked(self):
        # QMessageBox.about(self, "message", "clicked")
        fname=QFileDialog.getOpenFileName()
        if fname[0]:
            fileName=os.path.basename(fname[0])
            self.fileNameLabel.setText(fileName)
            filePath=os.path.splitext(fname[0])
            if filePath[-1]=='.xlsx':
                print(read_excel(fname[0]))

    def update_graph(self):
        self.GraphWidget.canvas.axes.clear()
        
        self.GraphWidget.canvas.draw() 


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
