import sys
import os
from loadFile import read_excel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx
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
        self.data=[]
        # self.figure=plt.Figure()
        # self.canvas=FigureCanvas(self.figure)
        self.addToolBar(NavigationToolbar(self.GraphWidget.canvas, self))

        self.loadFileBtn.clicked.connect(self.loadFile_clicked)
        self.makeGraphBtn.clicked.connect(self.makeGraph_clicked)
    
    @pyqtSlot()
    def loadFile_clicked(self):
        # QMessageBox.about(self, "message", "clicked")
        fname=QFileDialog.getOpenFileName()
        if fname[0]:
            fileName=os.path.basename(fname[0])
            self.fileNameLabel.setText(fileName)
            filePath=os.path.splitext(fname[0])
            if filePath[-1]=='.xlsx':
                self.data= read_excel(fname[0])
                print(self.data)


    @pyqtSlot()
    def makeGraph_clicked(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            return
        else:
            X = []
            Y = []
            Z=[]
            # X, Y = np.meshgrid(X, Y)
            # Z = X**2 + Y**3
            for i in range(len(self.data)):
                X.append(i)
                Y.append(self.data[i][0])
                Z.append(self.data[i][1])
            
            self.GraphWidget.canvas.axes.scatter(X,Y,Z,color='red')
            
            for i,j in enumerate(Y,Z):
                y=np.array(i,0,k)
                z=np.array(0,j,k)
                self.GraphWidget.canvas.axes.plot(X,y,z,color='white', alpha=0.5)

            
            
            # self.GraphWidget.canvas.axes.set_axis_off()
            self.GraphWidget.canvas.draw() 


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
