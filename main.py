import sys
import os.path
import threading
import time
import keyboard
import scipy as sp
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QApplication, \
    QStyleFactory, QTextEdit, QWidget


class MplCanvas3D2D(FigureCanvasQTAgg):
    def __init__(self, parents = None, width=15, height=15, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)
    def plot3D(self, xarray, yarray, zarray):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d',position=[0.05, 0.05, 0.9, 0.9])
        xarray_flat = xarray.flatten()
        yarray_flat = yarray.flatten()
        zarray_flat = zarray.flatten()
        ax.plot_trisurf(xarray_flat, yarray_flat, zarray_flat, color='red', alpha=0.6, edgecolor='red',
                        linewidth=0.1, antialiased=True, shade=1)
        ax.plot(xarray_flat, yarray_flat, zarray_flat, 'ok')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.draw()

    def plot2D(self, xarray, yarray):
        self.figure.clear()
        axe = self.figure.add_subplot(111)
        xarray_flat = xarray.flatten()
        yarray_flat = yarray.flatten()
        axe.plot(xarray_flat, yarray_flat, 'ok')
        axe.plot(xarray_flat, yarray_flat, 'r-')
        axe.set_xlabel('X')
        axe.set_ylabel('Y')
        self.draw()


class MainFrame(QMainWindow):

    def __init__(self):
        super(MainFrame, self).__init__()

        self.initUI()

    def initUI(self):
        self.sc = MplCanvas3D2D()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        hbox_splitter = QHBoxLayout()
        hbox_bottom = QHBoxLayout()

        left = QFrame()
        left.setFrameShape(QFrame.StyledPanel)

        left_label = QLabel('Options:', left)
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(left_label)
        left.setLayout(left_layout)

        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)

        right_label = QLabel('Plot Panel:', right)
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.sc)
        right.setLayout(right_layout)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)

        hbox_splitter.addWidget(splitter)

        text_edit = QTextEdit()
        term_label = QLabel("Terminal",self)
        hbox_bottom.addWidget(term_label)
        hbox_bottom.addWidget(text_edit)

        vbox.addLayout(hbox_splitter)
        vbox.addLayout(hbox_bottom)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Chaos Simulator')

        #Just for testing #D plotting:

        x = np.linspace(-5, 5, 20)
        y = np.linspace(-5, 5, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.cos(np.sqrt(X ** 2 + Y ** 2))

        self.sc.plot3D(X, Y, Z)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())