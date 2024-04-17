import sys

import matplotlib
import numpy as np
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
    Class repsonsible for the User interface of the application

    Attributes
        term_handler - TerminalHandler class object used for command execution \n
        text_edit - text send from terminal to Term_handler \n
        sc - MplCanvas2D3D class object

        eq_handler - EquationHandler class object used for numerical calculations of
        Lorenz and Roessler attractors equation \n
        self.eq_type_flag - flag distinguishing between Lorenz (equation=0) and Roessler (equation=1)
        attractors display \n
        lor_tmp - array of temporary parameter values of Lorenz attractor \n
        lor_tmp - array of temporary parameter values of Roessler attractor\n
        X,Y,Z -  XYZ coordinates used for attractor plotting \n

        lor_params_rho, lor_params_beta, lor_params_sigma - textfields representing Lorenz attractor parameters \n
        roe_params_a, roe_params_b, roe_params_c - textfields representing Roessler attractor parameters\n

        lor_init_condition_rho, lor_init_condition_beta, lor_init_condition_sigma - textfields representing Lorenz
        attractor starting conditions \n
        self.roe_init_condition_a, self.roe_init_condition_b, self.roe_init_condition_c - textfields representing
        Lorenz attractor starting conditions \n

        step_start - textfield representing starting step \n
        step_stop - textfield representing last step \n
        step_count - textfield representing number of steps \n

    Methods
        initUI(self) - function initializes user interface setting up layouts, buttons and other widgets\n
        look_for_enter_key(self) - listens to commands entered into terminal passing them to Term_handler class methods\n
        init_lorenz(self) - initializes equation handler, displays information about equations and parameters, draws 3D plots of Lorenz equations\n
        init_roessler(self) - initializes equation handler, displays information about equations and parameters, draws 3D plots of Lorenz equations \n
        draw_noise_plots((self, t_num, X, Y, Z) -  plots X, Y & Z noise in 2D as a function of time steps \n
        redraw_figure(self) -  redraws the attractor plot \n
        print_onto_text_edit(self, text) -  prints given text in the info_edit panel of the UI \n
        clear_terminal(self) - clears all text from the terminal \n
        clear_info(self) - clears all text from info_edit panel \n
        show_equation(self) - prints Roessler or Lorenz equation onto info_edit panel

    """

    def __init__(self):
        super(MainFrame, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.term_edit = None

        self.main_plot_canvas = MplCanvas3D2D()
        self.x_noise_canvas = MplCanvas3D2D()
        self.y_noise_canvas = MplCanvas3D2D()
        self.z_noise_canvas = MplCanvas3D2D()

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
        self.lor_tmp = []
        self.roe_tmp = []
        self.X = []
        self.Y = []
        self.Z = []
        self.initUI()

    def initUI(self):
        """
        Function initializes user interface setting up layouts, buttons and other widgets.
        It also displays and draws a number of plots related to Lorenz and Roessler attractors.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        hbox_splitter = QHBoxLayout()
        hbox_bottom = QHBoxLayout()

        left = QFrame()
        left.setFrameShape(QFrame.StyledPanel)

        # Buttons
        left_label = QLabel('Options:', left)

        plot_button = QPushButton("Plot points")
        plot_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        load_button = QPushButton("Load from file")
        load_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        load_button.pressed.connect(self.term_handler.load_plot)

        save_button = QPushButton("Save to file")
        save_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        save_button.pressed.connect(self.term_handler.save_plot)

        roe_init_button = QPushButton("Rössler plot")
        roe_init_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        roe_init_button.pressed.connect(self.init_roessler)

        lor_init_button = QPushButton("Lorenz plot")
        lor_init_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lor_init_button.pressed.connect(self.init_lorenz)

        # Lorenz parameters textfields and labels
        self.lor_params_rho = QtWidgets.QLineEdit(self)
        self.lor_params_rho.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lor_params_beta = QtWidgets.QLineEdit(self)
        self.lor_params_beta.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lor_params_sigma = QtWidgets.QLineEdit(self)
        self.lor_params_sigma.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        lor_label_rho = QLabel("ρ:")
        lor_label_rho.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lor_label_beta = QLabel("β:")
        lor_label_beta.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lor_label_sigma = QLabel("σ:")
        lor_label_sigma.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_layout = QVBoxLayout()

        self.init_l_params = QLabel("Initial Lorenz args:")
        lor_condition_layout = QHBoxLayout()
        self.lor_init_condition_rho = QtWidgets.QLineEdit(self)
        self.lor_init_condition_beta = QtWidgets.QLineEdit(self)
        self.lor_init_condition_sigma = QtWidgets.QLineEdit(self)

        lor_condition_layout.addWidget(self.lor_init_condition_rho)
        lor_condition_layout.addWidget(self.lor_init_condition_beta)
        lor_condition_layout.addWidget(self.lor_init_condition_sigma)

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

        lor_layout_rho = QHBoxLayout()
        lor_layout_rho.addWidget(lor_label_rho, 10)
        lor_layout_rho.addWidget(self.lor_params_rho, 90)
        lor_layout_beta = QHBoxLayout()
        lor_layout_beta.addWidget(lor_label_beta, 10)
        lor_layout_beta.addWidget(self.lor_params_beta, 90)
        lor_layout_sigma = QHBoxLayout()
        lor_layout_sigma.addWidget(lor_label_sigma, 10)
        lor_layout_sigma.addWidget(self.lor_params_sigma, 90)
        lorenz_layout.addWidget(lor_init_button)
        lorenz_layout.addLayout(lor_layout_rho)
        lorenz_layout.addLayout(lor_layout_beta)
        lorenz_layout.addLayout(lor_layout_sigma)
        lorenz_layout.addWidget(self.init_l_params)
        lorenz_layout.addLayout(lor_condition_layout)

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
        roe_condition_layout = QHBoxLayout()
        self.roe_init_condition_a = QtWidgets.QLineEdit(self)
        self.roe_init_condition_b = QtWidgets.QLineEdit(self)
        self.roe_init_condition_c = QtWidgets.QLineEdit(self)

        roe_condition_layout.addWidget(self.roe_init_condition_a)
        roe_condition_layout.addWidget(self.roe_init_condition_b)
        roe_condition_layout.addWidget(self.roe_init_condition_c)
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
        roessler_layout.addWidget(roe_init_button)
        roessler_layout.addLayout(roessler_layout1)
        roessler_layout.addLayout(roessler_layout2)
        roessler_layout.addLayout(roessler_layout3)
        roessler_layout.addWidget(self.init_r_params)
        roessler_layout.addLayout(roe_condition_layout)

        menu_sublayout = QHBoxLayout()
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
        left_layout.addWidget(load_button)
        left_layout.addWidget(save_button)
        left_layout.addWidget(plot_button)
        left_layout.addWidget(info_label)
        left_layout.addWidget(self.info_edit)

        left.setLayout(left_layout)

        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)

        right_label = QLabel('Plot Panel:', right)
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(right_label, 1)
        toolbar = NavigationToolbar(self.main_plot_canvas, self)
        right_layout.addWidget(toolbar, 4)

        right_plot_layout = QHBoxLayout();

        noise_layout = QVBoxLayout()
        noise_layout.addWidget(self.x_noise_canvas)
        noise_layout.addWidget(self.y_noise_canvas)
        noise_layout.addWidget(self.z_noise_canvas)

        right_plot_layout.addLayout(noise_layout, 30)
        right_layout.addLayout(right_plot_layout)

        right_plot_layout.addWidget(self.main_plot_canvas, 70)

        right.setLayout(right_layout)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(4, 1)

        hbox_splitter.addWidget(splitter)

        self.term_edit = QTextEdit()
        term_label = QLabel("Terminal:", self)
        term_layout = QVBoxLayout()
        term_layout.addWidget(term_label)
        term_layout.addWidget(self.term_edit)
        hbox_bottom.addLayout(term_layout)

        vbox.addLayout(hbox_splitter, 85)
        vbox.addLayout(hbox_bottom, 15)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Chaos Simulator')

        self.term_edit.textChanged.connect(self.look_for_enter_key)

        # Just for testing 3D plotting /// eq_handler call

        # Just for testing 3D plotting:
        self.eq_handler.set_lorenz_conditions(28, 8 / 3, 10)
        self.lor_tmp = [28, 8 / 3, 10]
        init_conditions = [1.0, 1.0, 1.0]
        t_start = 0.0
        t_end = 40.0
        num_steps = 10000
        t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_lorenz(init_conditions, t_start, t_end, num_steps)
        self.X = xyz[:, 0]
        self.Y = xyz[:, 1]
        self.Z = xyz[:, 2]
        self.info_edit.setText(self.eq_handler.print_lorenz_eq(28, 8 / 3, 10))

        self.main_plot_canvas.plot3D(self.X, self.Y, self.Z)
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
        Listens to commands entered into terminal passing them to Term_handler class methods
        """
        if self.term_edit.toPlainText().endswith('\n'):
            self.term_handler.get_command(self.term_edit, self.term_edit.toPlainText())

    def init_lorenz(self):
        """
        Initializes equation handler from textfield parameters, displays information about step, equations and parameters
        and draws 3D plots of Lorenz equations.
        """
        self.info_edit.clear()
        if self.lor_params_rho.text() and self.lor_params_beta.text() and self.lor_params_sigma.text():
            print(float(self.lor_params_rho.text()))
            print(float(self.lor_params_beta.text()))
            print(float(self.lor_params_sigma.text()))
            self.eq_handler.set_lorenz_conditions(float(self.lor_params_rho.text()), float(self.lor_params_beta.text()),
                                                  float(self.lor_params_sigma.text()))
            self.lor_tmp = np.array([float(self.lor_params_rho.text()), float(self.lor_params_beta.text()),
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
            self.main_plot_canvas.plot3D(self.X, self.Y, self.Z)
            self.eq_type_flag = 0
            t = np.linspace(t_start, t_end, num_steps)
            self.draw_noise_plots(t, self.X, self.Y, self.Z)
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    def init_roessler(self):
        """
        Initializes equation handler from textfield parameters, displays information about step, equations and parameters
        and draws 3D plots of Lorenz equations.
        """
        if self.roe_params_a.text() and self.roe_params_b.text() and self.roe_params_c.text():
            self.info_edit.clear()
            self.eq_handler.set_roessler_conditions(float(self.roe_params_a.text()),
                                                    float(self.roe_params_b.text()),
                                                    float(self.roe_params_c.text()))
            self.roe_tmp = np.array([float(self.roe_params_a.text()), float(self.roe_params_b.text()),
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
            self.main_plot_canvas.plot3D(self.X, self.Y, self.Z)
            self.eq_type_flag = 1
            t = np.linspace(t_start, t_end, num_steps)
            self.draw_noise_plots(t, self.X, self.Y, self.Z)
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    def draw_noise_plots(self, t_num, X, Y, Z):
        """
        Plots X, Y & Z noise in 2D as a function of time steps
        :param t_num: time steps array
        :param X: x coordinates array
        :param Y: y coordinates array
        :param Z: z coordinates array
        """
        self.x_noise_canvas.plot2D(t_num, X, 'Time steps', 'X', 'red')
        self.y_noise_canvas.plot2D(t_num, Y, 'Time steps', 'Y', 'green')
        self.z_noise_canvas.plot2D(t_num, Z, 'Time steps', 'Z', 'orange')

    def redraw_figure(self):
        """
        Redraws the attractor plot
        """
        self.main_plot_canvas.draw()
        self.main_plot_canvas.plot3D(self.X, self.Y, self.Z)

    def print_onto_info_edit(self, text):
        """
        Prints given text in the info_edit panel of the UI
        :param text: text to be displayed in UI
        :type text: str
        """
        self.info_edit.append(f"{text}")

    def clear_terminal(self):
        """
        Clears all text from the terminal
        """
        self.term_edit.clear()

    def clear_info(self):
        """
        Clears all text from info_edit panel
        """
        self.info_edit.clear()

    def show_equation(self):
        """
        Prints Roessler or Lorenz equation onto info_edit panel
        """
        if self.eq_type_flag == 0: # Lorenz equation
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_lorenz_eq(self.lor_tmp[0], self.lor_tmp[1], self.lor_tmp[2]))
        elif self.eq_type_flag == 1: # Roessler equation
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_roessler_eq(self.roe_tmp[0], self.roe_tmp[1], self.roe_tmp[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())