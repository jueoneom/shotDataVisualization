import sys
import os
from file_management.load_file import read_excel
from math_functions.math_function import *
from dialogs.generate_dialog import *
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

SHOT_SIZE, SHOT_ANGLE, SUB_OBJ = 0, 1, 2
data_labels = {0: ("", "extreme close-up", "close-up", "middle", "full", "long", "extreme long"), 1: ("", "high", "eye", "low"), 2: ("", "obj", "sub")}

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
        self.addToolBar(NavigationToolbar(self.GraphWidget.canvas, self))

        self.loadFileBtn.clicked.connect(self.loadFile_clicked)
        self.makeGraphBtn.clicked.connect(self.generateGraph_clicked)
        self.makeGraphBtn_2.clicked.connect(self.make_graph)
        
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

    def check_axis(self):
        if not self.axis_checkbox.isChecked(): 
            self.GraphWidget.canvas.axes.set_axis_off()

    def check_color_standard(self):
        if self.color_radio_1.isChecked(): return (SHOT_SIZE, 6)
        elif self.color_radio_2.isChecked(): return (SHOT_ANGLE, 3)
        elif self.color_radio_3.isChecked(): return (SUB_OBJ, 2)


    def make_graph(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            generate_messagebox(self, '[경고 메시지]', '데이터를 불러오지 않아 예제 데이터를 출력합니다.')
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
            x_points = [data[SHOT_SIZE] * i for i, data in enumerate(self.data, 1)]
            y_points = [data[SHOT_ANGLE] * i for i, data in enumerate(self.data, 1)]
            z_points = [data[SUB_OBJ] * i for i, data in enumerate(self.data, 1)]
            color_data = self.check_color_standard()
            c_points = [data[color_data[0]] for data in self.data]
            
            if self.label_checkbox.isChecked():
                c_list = [plt.cm.rainbow(a) for a in np.linspace(0.0, 1.0, len(set(c_points)))]
                for i in range(len(c_list)):
                    self.GraphWidget.canvas.axes.scatter(0, 0, 0, c=c_list[i],  label='{}'.format(data_labels[color_data[0]][list(set(c_points))[i]]) )


            self.GraphWidget.canvas.axes.scatter(x_points, y_points, z_points, c = c_points, cmap = plt.cm.get_cmap('rainbow',color_data[1]) )
            self.GraphWidget.canvas.axes.plot(x_points, y_points, z_points, 'white')
        
        self.GraphWidget.canvas.axes.set_xlabel("shot-size")
        self.GraphWidget.canvas.axes.set_ylabel("shot-angle")
        self.GraphWidget.canvas.axes.set_zlabel("subj-obj")
        self.GraphWidget.canvas.axes.legend()
        self.GraphWidget.canvas.axes.view_init(30, 0)
        self.check_axis()
        self.GraphWidget.canvas.draw() 


    def generateGraph_clicked(self):
        self.GraphWidget.canvas.axes.clear()
        if not self.data:
            generate_messagebox(self, '[경고 메시지]', '데이터를 불러오지 않아 데이터를 출력할 수 없습니다.')
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
        self.check_axis()
        self.GraphWidget.canvas.draw() 


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    app.exec_()
    
