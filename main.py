import sys

import matplotlib
import numpy as np
import terminal_handler as th
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QPushButton
from equation_handler import EquationHandler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from terminal_handler import TerminalHandler

matplotlib.use('Qt5Agg')


class MplCanvas3D2D(FigureCanvasQTAgg):
    """
    Class is a version of a basic PyQT FigureCanvas with modified plotting function meant for Lorenz and Roessler
    attractors plotting.

    Atributes
        figure - graph of given size and format

    Methods
        plot3D - Plots XYZ points on a 3D graph based on supplied arrays of coordinates
        plot2D - Plots XY points on 2D graph based on supplied arrays of coordinates
    """
    def __init__(self, width=20, height=20, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot3D(self, xarray, yarray, zarray):
        """
        Plots XYZ points on a 3D graph based on supplied arrays of coordinates
        :param xarray: x coordinates array
        :param yarray: y coordinates array
        :param zarray: z coordinates array
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d', position=[0.05, 0.05, 0.9, 0.9])
        ax.plot(xarray, yarray, zarray)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.draw()

    def plot2D(self, xarray, yarray, xlabel, ylabel, color):
        """
        Plots XY points on 2D graph based on supplied arrays of coordinates
        :param xarray: x coordinates array
        :param yarray: y coordinates array
        :param xlabel: label of OX axis
        :param ylabel: label of OY axis
        :param color: color of the plot
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.15, 0.2, 0.8, 0.8])
        ax.plot(xarray, yarray, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        self.draw()


class MainFrame(QMainWindow):
    """
    Attributes
        term_handler - TerminalHandler class object used for command execution \n
        text_edit - text send from terminal to Term_handler \n
        sc - MplCanvas2D3D class object \n

        eq_handler - EquationHandler class object used for numerical calculations of Lorenz and Roessler attractors equation \n
        equation - flag distinguishing between Lorenz (equation=0) and Roessler (equation=1) attractors display \n
        tempLor - \n
        tempRoe \n
        X,Y,Z \n

        lorenz_params_rho, lorenz_params_beta, lorenz_params_sigma \n
        roessler_params1, roessler_params2, roessler_params3 \n
        init_l_condition1, init_l_condition2, init_l_condition3 \n
        init_r_condition1, init_r_condition2, init_r_condition3 \n

        step_start \n
        step_stop \n
        step_count \n
    """

    def __init__(self):
        super(MainFrame, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.text_edit = None
        self.sc = None

        self.term_handler = TerminalHandler(self)

        self.eq_handler = EquationHandler()
        TerminalHandler.load_command_base(self)

        # lorenz parameter textfields
        self.lor_params_rho = None
        self.lor_params_beta = None
        self.lor_params_sigma = None
        self.roe_params_a = None
        self.roe_params_b = None
        self.roe_params_c = None

        # lorenz start condition textfields
        self.lor_init_condition_rho = None
        self.lor_init_condition_beta = None
        self.lor_init_condition_sigma = None
        self.roe_init_condition_a = None
        self.roe_init_condition_b = None
        self.roe_init_condition_c = None

        self.step_start = None
        self.step_stop = None
        self.step_count = None

        self.eq_type_flag = 0
        self.tempLor = []
        self.tempRoe = []
        self.X = []
        self.Y = []
        self.Z = []
        self.initUI()

    def initUI(self):
        """
        Function initializes user interface setting up layouts, button and other widgets.
        It also displays and draws a number of plots related to Lorenz and Roessler attractors.
        """
        self.sc = MplCanvas3D2D()
        self.scNoise1 = MplCanvas3D2D()
        self.scNoise2 = MplCanvas3D2D()
        self.scNoise3 = MplCanvas3D2D()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        hbox_splitter = QHBoxLayout()
        hbox_bottom = QHBoxLayout()

        left = QFrame()
        left.setFrameShape(QFrame.StyledPanel)

        # buttons
        left_label = QLabel('Options:', left)

        plot_button = QPushButton("Plot points")
        plot_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        load_data = QPushButton("Load from file")
        load_data.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        load_data.pressed.connect(self.term_handler.load_plot)

        save_data = QPushButton("Save to file")
        save_data.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        save_data.pressed.connect(self.term_handler.save_plot)

        init_r_button = QPushButton("Rössler plot")
        init_r_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        init_r_button.pressed.connect(self.init_roessler)

        init_l_button = QPushButton("Lorenz plot")
        init_l_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        init_l_button.pressed.connect(self.init_lorenz)

        self.lor_params_rho = QtWidgets.QLineEdit(self)
        self.lor_params_rho.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lor_params_beta = QtWidgets.QLineEdit(self)
        self.lor_params_beta.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lor_params_sigma = QtWidgets.QLineEdit(self)
        self.lor_params_sigma.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        lorenz_label1 = QLabel("ρ:")
        lorenz_label1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_label2 = QLabel("β:")
        lorenz_label2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_label3 = QLabel("σ:")
        lorenz_label3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_layout = QVBoxLayout()

        self.init_l_params = QLabel("Initial Lorenz args:")
        l_condition_layout = QHBoxLayout()
        self.lor_init_condition_rho = QtWidgets.QLineEdit(self)
        self.lor_init_condition_beta = QtWidgets.QLineEdit(self)
        self.lor_init_condition_sigma = QtWidgets.QLineEdit(self)

        l_condition_layout.addWidget(self.lor_init_condition_rho)
        l_condition_layout.addWidget(self.lor_init_condition_beta)
        l_condition_layout.addWidget(self.lor_init_condition_sigma)

        steps_layout = QHBoxLayout()

        steps_label = QLabel("t0, tn and N step values:")
        self.step_start = QtWidgets.QLineEdit(self)
        t0_layout = QHBoxLayout()
        step_start_label = QLabel("t0:")
        self.step_stop = QtWidgets.QLineEdit(self)
        tn_layout = QHBoxLayout()
        step_stop_label = QLabel('tn:')
        n_layout = QHBoxLayout()
        self.step_count = QtWidgets.QLineEdit(self)
        step_count_label = QLabel('N:')

        t0_layout.addWidget(step_start_label)
        t0_layout.addWidget(self.step_start)

        tn_layout.addWidget(step_stop_label)
        tn_layout.addWidget(self.step_stop)

        n_layout.addWidget(step_count_label)
        n_layout.addWidget(self.step_count)

        steps_layout.addLayout(t0_layout)
        steps_layout.addLayout(tn_layout)
        steps_layout.addLayout(n_layout)

        menu_sublayout = QHBoxLayout()
        lorenz_layout1 = QHBoxLayout()
        lorenz_layout1.addWidget(lorenz_label1, 10)
        lorenz_layout1.addWidget(self.lor_params_rho, 90)
        lorenz_layout2 = QHBoxLayout()
        lorenz_layout2.addWidget(lorenz_label2, 10)
        lorenz_layout2.addWidget(self.lor_params_beta, 90)
        lorenz_layout3 = QHBoxLayout()
        lorenz_layout3.addWidget(lorenz_label3, 10)
        lorenz_layout3.addWidget(self.lor_params_sigma, 90)
        lorenz_layout.addWidget(init_l_button)
        lorenz_layout.addLayout(lorenz_layout1)
        lorenz_layout.addLayout(lorenz_layout2)
        lorenz_layout.addLayout(lorenz_layout3)
        lorenz_layout.addWidget(self.init_l_params)
        lorenz_layout.addLayout(l_condition_layout)

        self.roe_params_a = QtWidgets.QLineEdit(self)
        self.roe_params_a.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.roe_params_b = QtWidgets.QLineEdit(self)
        self.roe_params_b.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.roe_params_c = QtWidgets.QLineEdit(self)
        self.roe_params_c.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        roessler_label1 = QLabel("a:")
        roessler_label1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        roessler_label2 = QLabel("b:")
        roessler_label2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        roessler_label3 = QLabel("c:")
        roessler_label3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.init_r_params = QLabel("Initial Rössler args:")
        r_condition_layout = QHBoxLayout()
        self.roe_init_condition_a = QtWidgets.QLineEdit(self)
        self.roe_init_condition_b = QtWidgets.QLineEdit(self)
        self.roe_init_condition_c = QtWidgets.QLineEdit(self)

        r_condition_layout.addWidget(self.roe_init_condition_a)
        r_condition_layout.addWidget(self.roe_init_condition_b)
        r_condition_layout.addWidget(self.roe_init_condition_c)
        roessler_layout = QVBoxLayout()

        roessler_layout1 = QHBoxLayout()
        roessler_layout2 = QHBoxLayout()
        roessler_layout3 = QHBoxLayout()
        roessler_layout1.addWidget(roessler_label1, 10)
        roessler_layout1.addWidget(self.roe_params_a, 90)
        roessler_layout2.addWidget(roessler_label2, 10)
        roessler_layout2.addWidget(self.roe_params_b, 90)
        roessler_layout3.addWidget(roessler_label3, 10)
        roessler_layout3.addWidget(self.roe_params_c, 90)
        roessler_layout.addWidget(init_r_button)
        roessler_layout.addLayout(roessler_layout1)
        roessler_layout.addLayout(roessler_layout2)
        roessler_layout.addLayout(roessler_layout3)
        roessler_layout.addWidget(self.init_r_params)
        roessler_layout.addLayout(r_condition_layout)

        menu_sublayout.addLayout(lorenz_layout)
        menu_sublayout.addLayout(roessler_layout)
        info_label = QLabel("Equation info:", left)
        self.info_edit = QTextEdit()
        self.info_edit.setFont(QFont('Times', 12))
        self.info_edit.setReadOnly(True)

        left_layout = QVBoxLayout(left)
        left_layout.setSpacing(5)
        left_layout.addWidget(left_label)
        left_layout.addLayout(menu_sublayout)
        left_layout.addWidget(steps_label)
        left_layout.addLayout(steps_layout)
        left_layout.addWidget(load_data)
        left_layout.addWidget(save_data)
        left_layout.addWidget(plot_button)
        left_layout.addWidget(info_label)
        left_layout.addWidget(self.info_edit)

        left.setLayout(left_layout)

        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)

        right_label = QLabel('Plot Panel:', right)
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(right_label, 1)
        toolbar = NavigationToolbar(self.sc, self)
        right_layout.addWidget(toolbar, 4)
        right_layout.addWidget(self.sc, 60)

        noise_layout = QHBoxLayout()
        noise_layout.addWidget(self.scNoise1)
        noise_layout.addWidget(self.scNoise2)
        noise_layout.addWidget(self.scNoise3)

        right_layout.addLayout(noise_layout, 35)

        right.setLayout(right_layout)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(4, 1)

        hbox_splitter.addWidget(splitter)

        self.text_edit = QTextEdit()
        term_label = QLabel("Terminal:", self)
        term_layout = QVBoxLayout()
        term_layout.addWidget(term_label)
        term_layout.addWidget(self.text_edit)
        hbox_bottom.addLayout(term_layout)

        vbox.addLayout(hbox_splitter, 85)
        vbox.addLayout(hbox_bottom, 15)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Chaos Simulator')

        self.text_edit.textChanged.connect(self.look_for_enter_key)

        # Just for testing 3D plotting /// eq_handler call

        # Just for testing 3D plotting:
        self.eq_handler.set_lorenz_conditions(28, 8 / 3, 10)
        self.tempLor = [28, 8 / 3, 10]
        init_conditions = [1.0, 1.0, 1.0]
        t_start = 0.0
        t_end = 40.0
        num_steps = 10000
        t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_lorenz(init_conditions, t_start, t_end, num_steps)
        self.X = xyz[:, 0]
        self.Y = xyz[:, 1]
        self.Z = xyz[:, 2]
        self.info_edit.setText(self.eq_handler.print_lorenz_eq(28, 8 / 3, 10))

        self.sc.plot3D(self.X, self.Y, self.Z)
        self.lor_params_rho.setText('28')
        self.lor_params_beta.setText('2.6666666')
        self.lor_params_sigma.setText('10')
        self.roe_params_a.setText('0.1')
        self.roe_params_b.setText('0.1')
        self.roe_params_c.setText('14')
        self.roe_init_condition_a.setText('1.0')
        self.roe_init_condition_b.setText('1.0')
        self.roe_init_condition_c.setText('1.0')
        self.lor_init_condition_rho.setText('1.0')
        self.lor_init_condition_beta.setText('1.0')
        self.lor_init_condition_sigma.setText('1.0')
        self.step_start.setText('0')
        self.step_stop.setText('50')
        self.step_count.setText('10000')

    def look_for_enter_key(self):
        """
        Listens to commands entered into terminal passing thwem to Term_handler class methods
        """
        if self.text_edit.toPlainText().endswith('\n'):
            self.term_handler.get_command(self.text_edit, self.text_edit.toPlainText())

    def init_lorenz(self):
        """
        Initializes Lorenz equation handler from textfields, displays information about step, equations and parameters
        and finally draws 3D plots of Lorenz equations.
        """
        self.info_edit.clear()
        if self.lor_params_rho.text() and self.lor_params_beta.text() and self.lor_params_sigma.text():
            print(float(self.lor_params_rho.text()))
            print(float(self.lor_params_beta.text()))
            print(float(self.lor_params_sigma.text()))
            self.eq_handler.set_lorenz_conditions(float(self.lor_params_rho.text()), float(self.lor_params_beta.text()),
                                                  float(self.lor_params_sigma.text()))
            self.tempLor = np.array([float(self.lor_params_rho.text()), float(self.lor_params_beta.text()),
                                     float(self.lor_params_sigma.text())])
            if self.lor_init_condition_rho.text() and self.lor_init_condition_beta.text() and self.lor_init_condition_sigma.text():
                init_conditions = [float(self.lor_init_condition_rho.text()), float(self.lor_init_condition_beta.text()),
                                   float(self.lor_init_condition_sigma.text())]
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append(self.lor_init_condition_rho.text())
                self.info_edit.append(self.lor_init_condition_beta.text())
                self.info_edit.append(self.lor_init_condition_sigma.text())
            else:
                init_conditions = np.array([1.0, 1.0, 1.0])
                self.lor_init_condition_rho.setText('1.0')
                self.lor_init_condition_beta.setText('1.0')
                self.lor_init_condition_sigma.setText('1.0')
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
            if self.step_start.text() and self.step_stop.text() and self.step_count.text():
                t_start = int(self.step_start.text())
                t_end = int(self.step_stop.text())
                num_steps = int(self.step_count.text())
            else:
                self.step_start.setText('0')
                self.step_stop.setText('50')
                self.step_count.setText('10000')
                t_start = 0
                t_end = 50
                num_steps = 10000
            t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_lorenz(init_conditions, t_start, t_end, num_steps)
            self.X = xyz[:, 0]
            self.Y = xyz[:, 1]
            self.Z = xyz[:, 2]

            self.info_edit.append(
                self.eq_handler.print_lorenz_eq(float(self.lor_params_rho.text()), float(self.lor_params_beta.text()),
                                                float(self.lor_params_sigma.text())))
            self.sc.plot3D(self.X, self.Y, self.Z)
            self.eq_type_flag = 0
            t = np.linspace(t_start, t_end, num_steps)
            self.draw_noise_plots(t, self.X, self.Y, self.Z)
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    def init_roessler(self):
        """
        Initializes Roessler equation handler from textfields, displays information about step, equations and parameters
        and finally draws 3D plots of Lorenz equations.
        """
        if self.roe_params_a.text() and self.roe_params_b.text() and self.roe_params_c.text():
            self.info_edit.clear()
            self.eq_handler.set_roessler_conditions(float(self.roe_params_a.text()),
                                                    float(self.roe_params_b.text()),
                                                    float(self.roe_params_c.text()))
            self.tempRoe = np.array([float(self.roe_params_a.text()), float(self.roe_params_b.text()),
                                     float(self.roe_params_c.text())])

            if self.roe_init_condition_a.text() and self.roe_init_condition_b.text() and self.roe_init_condition_c.text():
                init_conditions = [float(self.roe_init_condition_a.text()),
                                   float(self.roe_init_condition_b.text()),
                                   float(self.roe_init_condition_c.text())]
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append(self.roe_init_condition_a.text())
                self.info_edit.append(self.roe_init_condition_b.text())
                self.info_edit.append(self.roe_init_condition_c.text())
            else:
                init_conditions = [1.0, 1.0, 1.0]
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
                self.roe_init_condition_a.setText('1.0')
                self.roe_init_condition_b.setText('1.0')
                self.roe_init_condition_c.setText('1.0')
            if self.step_start.text() and self.step_stop.text() and self.step_count.text():
                t_start = int(self.step_start.text())
                t_end = int(self.step_stop.text())
                num_steps = int(self.step_count.text())
            else:
                t_start = 0
                t_end = 400
                num_steps = 10000
                self.step_start.setText('0')
                self.step_stop.setText('400')
                self.step_count.setText('10000')
            t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_roessler(init_conditions, t_start, t_end, num_steps)

            self.X = xyz[:, 0]
            self.Y = xyz[:, 1]
            self.Z = xyz[:, 2]
            self.info_edit.append(self.eq_handler.print_roessler_eq(float(self.roe_params_a.text()),
                                                                    float(self.roe_params_b.text()),
                                                                    float(self.roe_params_c.text())))
            self.sc.plot3D(self.X, self.Y, self.Z)
            self.eq_type_flag = 1
            t = np.linspace(t_start, t_end, num_steps)
            self.draw_noise_plots(t, self.X, self.Y, self.Z)
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    # def load_from_file(self):
    #
    # def save_to_file(self):

    def draw_noise_plots(self, t_num, X, Y, Z):
        """
        Plots X, Y & Z noise in 2D as a function of time steps
        :param t_num: time steps array
        :param X: x coordinates array
        :param Y: y coordinates array
        :param Z: z coordinates array
        """
        self.scNoise1.plot2D(t_num, X, 'Time steps', 'X', 'red')
        self.scNoise2.plot2D(t_num, Y, 'Time steps', 'Y', 'green')
        self.scNoise3.plot2D(t_num, Z, 'Time steps', 'Z', 'orange')

    def redraw_figure(self):
        """

        :return:
        """
        self.sc.draw()
        self.sc.plot3D(self.X, self.Y, self.Z)

    def print_onto_text_edit(self, text):
        """
        prints
        :param text:
        """
        self.info_edit.append(f"{text}")

    def clear_terminal(self):
        """"
        """
        self.text_edit.clear()

    def clear_info(self):
        """

        :return:
        """
        self.info_edit.clear()

    def get_user_Equation(self):
        return self.text_edit.toPlainText()

    def show_equation(self):
        """

        """
        if self.eq_type_flag == 0:
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_lorenz_eq(self.tempLor[0], self.tempLor[1], self.tempLor[2]))
        elif self.eq_type_flag == 1:
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_roessler_eq(self.tempRoe[0], self.tempRoe[1], self.tempRoe[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())