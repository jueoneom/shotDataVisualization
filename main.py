import sys
import os
from file_management.load_file import read_excel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
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
    @pyqtSlot()
    def makeGraph_clicked(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            return
        else:
            # X = []
            # Y = []
            # Z=[]
            X = np.arange(-5, 5, 0.25)
            Y = np.arange(-5, 5, 0.25)
            X, Y = np.meshgrid(X, Y)
            Z = X**2 + Y**3
            # for i in range(len(self.data)):
            #     X.append(i)
            #     Y.append(self.data[i][0])
            #     Z.append(self.data[i][1])
        
        self.GraphWidget.canvas.axes.plot_wireframe(X, Y, Z, color='white')
            # G = nx.erdos_renyi_graph(500, 0.5, seed=123, directed=False)
            # pos = nx.get_node_attributes(G, 'pos')
            # n=G.number_of_nodes()
            # edge_max = max([G.degree(i) for i in range(n)])
            # colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 
            
            # with plt.style.context(('ggplot')):
            #     for key, value in pos.items():
            #         xi = value[0]
            #         yi = value[1]
            #         zi = value[2]
            #         self.canvas.axes.scatter(xi, yi, zi, c=colors[key], s=20+20*G.degree(key), edgecolors='k', alpha=0.7)

        self.GraphWidget.canvas.axes.set_axis_off()
        self.GraphWidget.canvas.draw() 

    def check_shotsize(self, state):
        if state == Qt.Checked:
            print("a")
        else:
            print("b")



    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def softmax(self, x):
        e_x = np.exp(x-np.max(x))
        return e_x / e_x.sum()

    def generateGraph_clicked(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            return
        LENGTH=len(self.data)
        shot_size = self.softmax(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
        shot_angle = self.softmax(np.array([1.0,2.0,3.0]))
        sub_obj = self.softmax(np.array([1.0, 2.0, 3.0, 4.0]))
        pos={i: (self.sigmoid(self.data[i][0]*shot_size[self.data[i][0]-1]),self.sigmoid(self.data[i][1]*shot_angle[self.data[i][1]-1]), self.sigmoid((self.data[i][2]+self.data[i][3]))) for i in range(len(self.data))}
        # pos={i: (shot_size[self.data[i][0]-1],shot_angle[self.data[i][1]-1], sub_obj[self.data[i][2]-1+self.data[i][3]-1]) for i in range(len(self.data))}
        # pos={i: (self.sigmoid(self.data[i-LENGTH][0]),self.sigmoid(self.data[i-LENGTH][1]), self.sigmoid(self.data[i-LENGTH][2]+(self.data[i-LENGTH][3])*3)) for i in range(LENGTH, LENGTH*2)}
        
    
            

         
        G = nx.random_geometric_graph(len(self.data), 0.25, pos=pos)
        # G=nx.geographical_threshold_graph(20,50,pos=pos)
        # nx.draw_networkx_nodes(temp,pos,node_size=400,alpha=1.0,node_shape='o',node_color='white')
        # nx.draw_networkx_edges(temp, pos, width=1, alpha=0.8, edge_color='crimson')
        
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
    
