import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setLayout(self.layout)
        self.setGeometry(200, 200, 800, 600)
    def initUI(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        cb = QComboBox()
        cb.addItem('Graph1')
        cb.addItem('Graph2')
        cb.activated[str].connect(self.onComboBoxChanged)
        layout.addWidget(cb)
        self.layout = layout
        self.onComboBoxChanged(cb.currentText())
    def onComboBoxChanged(self, text):
        if text == 'Graph1':
            self.doGraph1()

    def doGraph1(self):
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = X**2 + Y**2
        
        self.fig.clear()
        
        ax = self.fig.gca(projection='3d')
        # ax.plot_wireframe(X, Y, Z, color='black')
        self.canvas.draw() 
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()