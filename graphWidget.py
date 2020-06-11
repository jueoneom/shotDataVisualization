from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class GraphWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        plt.style.use('dark_background')
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        hLayout=QHBoxLayout()
        hLayout.addWidget(self.canvas)
        self.fig.clear()
        
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = X**2 + Y**2
        self.canvas.axes = self.fig.gca(projection='3d')
        # ax=self.fig.add_subplot(111,projection='3d')
        self.canvas.axes.scatter(X,Y,Z,color='white')
        # ax.plot_wireframe(X, Y, Z, color='white')
        # ax=plt.axes(projection='3d')
        

        self.canvas.axes.set_axis_off()
        self.setLayout(hLayout)
        self.canvas.draw()
