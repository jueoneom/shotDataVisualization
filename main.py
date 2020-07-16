import sys
import os
from file_management.load_file import read_excel
from math_functions.math_function import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx


form_class=uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.left=10
        self.top=10
        self.title='샷 데이터 시각화 프로그램'
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
        self.makeGraphBtn.clicked.connect(self.generateGraph_clicked)
        self.makeGraphBtn_2.clicked.connect(self.make_graph)
        self.shotsize_chbox.stateChanged.connect(self.check_shotsize)
        self.shotangle_chbox.stateChanged.connect(self.check_shotsize)
   
    @pyqtSlot()
    def loadFile_clicked(self):
        fname=QFileDialog.getOpenFileName()
        if fname[0]:
            fileName=os.path.basename(fname[0])
            self.fileNameLabel.setText(fileName)
            filePath=os.path.splitext(fname[0])
            if filePath[-1]=='.xlsx':
                self.data= read_excel(fname[0])
                print(self.data)

    def check_shotsize(self, state):
        if state == Qt.Checked:
            print("a")
        else:
            print("b")

    def make_graph(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            error_msg = QMessageBox()
            error_msg.question(self, 'error message','데이터를 먼저 불러와주세요.', QMessageBox.Yes)

            z_line = np.linspace(0, 15, 1000)
            x_line = np.cos(z_line)
            y_line = np.sin(z_line)
            self.GraphWidget.canvas.axes.plot(x_line, y_line, z_line, 'gray')
            
     
            z_points = 15 * np.random.random(100)
            x_points = np.cos(z_points) + 0.1 * np.random.randn(100)
            y_points = np.sin(z_points) + 0.1 * np.random.randn(100)

            self.GraphWidget.canvas.axes.scatter(x_points, y_points, z_points, c=z_points, cmap='hsv')
            self.GraphWidget.canvas.axes.plot(x_points, y_points, z_points, 'white')
        else:
            x_points= [data[0] * i for i, data in enumerate(self.data, 1)]
            y_points= [data[1] * i for i, data in enumerate(self.data, 1)]
            z_points= [data[2] * i for i, data in enumerate(self.data, 1)]

            self.GraphWidget.canvas.axes.scatter(x_points, y_points, z_points, c=z_points, cmap='hsv')
            self.GraphWidget.canvas.axes.plot(x_points, y_points, z_points, 'white')
        
        self.GraphWidget.canvas.axes.view_init(30, 0)
        # self.GraphWidget.canvas.axes.set_axis_off()
        self.GraphWidget.canvas.draw() 


    def generateGraph_clicked(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            return
        LENGTH=len(self.data)
        shot_size = softmax(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
        shot_angle = softmax(np.array([1.0,2.0,3.0]))
        sub_obj = softmax(np.array([1.0, 2.0, 3.0, 4.0]))
        pos={i: (sigmoid(self.data[i][0]*shot_size[self.data[i][0]-1]),sigmoid(self.data[i][1]*shot_angle[self.data[i][1]-1]), sigmoid((self.data[i][2]+self.data[i][3]))) for i in range(len(self.data))}
         
        G = nx.random_geometric_graph(len(self.data), 0.25, pos=pos)
        
        pos = nx.get_node_attributes(G, 'pos')
        n = G.number_of_nodes()
        edge_max = max([G.degree(i) for i in range(n)])
        colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 
        

        with plt.style.context(('ggplot')):
             
            for key, value in pos.items():
                xi = value[0]
                yi = value[1]
                zi = value[2]
                self.GraphWidget.canvas.axes.scatter(xi, yi, zi, c=np.array([colors[key]]), s=20+20*G.degree(key), alpha=0.7)
            
            for i,j in enumerate(G.edges()):
                x = np.array((pos[j[0]][0], pos[j[1]][0]))
                y = np.array((pos[j[0]][1], pos[j[1]][1]))
                z = np.array((pos[j[0]][2], pos[j[1]][2]))
                print(j, x, y, z)
                self.GraphWidget.canvas.axes.plot(x, y, z, c='white', alpha=0.5)
        
                

        self.GraphWidget.canvas.axes.view_init(30, 0)
        # self.GraphWidget.canvas.axes.set_axis_off()
        self.GraphWidget.canvas.draw() 





if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
