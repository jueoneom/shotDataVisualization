from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
from mpl_toolkits.mplot3d import Axes3D

class GraphWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        plt.style.use('dark_background')
        self.fig = plt.Figure(figsize=(10,7))
            
        self.canvas = FigureCanvas(self.fig)
        hLayout=QHBoxLayout()
        hLayout.addWidget(self.canvas)
        self.fig.clear()
        
        n=200
        G=self.generate_random_3Dgraph(n_nodes=200, radius=0.25, seed=1)
        pos = nx.get_node_attributes(G, 'pos')
        n = G.number_of_nodes()
        edge_max = max([G.degree(i) for i in range(n)])
        colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 

        self.canvas.axes = self.fig.gca(projection='3d')
        # # ax=self.fig.add_subplot(111,projection='3d')
        # self.canvas.axes.scatter(X,Y,Z,color='white')
        # # ax.plot_wireframe(X, Y, Z, color='white')
        # # ax=plt.axes(projection='3d')
        
        with plt.style.context(('ggplot')):
            
            for key, value in pos.items():
                xi = value[0]
                yi = value[1]
                zi = value[2]
                self.canvas.axes.scatter(xi, yi, zi, c=np.array([colors[key]]), s=20+20*G.degree(key), edgecolors='k', alpha=0.7)
            
            for i,j in enumerate(G.edges()):
                x = np.array((pos[j[0]][0], pos[j[1]][0]))
                y = np.array((pos[j[0]][1], pos[j[1]][1]))
                z = np.array((pos[j[0]][2], pos[j[1]][2]))
                print(j, x, y, z)
                self.canvas.axes.plot(x, y, z, c='white', alpha=0.5)
        self.canvas.axes.view_init(30, 0)
        # self.canvas.axes.set_axis_off()

        # self.canvas.axes.set_axis_off()
        self.setLayout(hLayout)
        self.canvas.draw()

  
    def generate_random_3Dgraph(self, n_nodes, radius, seed=None):
        if seed is not None:
            random.seed(seed)
        pos={i:(random.uniform(0,1),
        random.uniform(0,1), random.uniform(0,1)) for i in range(n_nodes)}
        G=nx.random_geometric_graph(n_nodes, radius, pos=pos)
        return G

