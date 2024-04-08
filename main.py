import sys
import matplotlib
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QPushButton
import terminal_handler as th
from terminal_handler import Term_handler
from equation_handler import Eq_Handler

matplotlib.use('Qt5Agg')


class MplCanvas3D2D(FigureCanvasQTAgg):
    def __init__(self, parents=None, width=20, height=20, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot3D(self, xarray, yarray, zarray):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d', position=[0.05, 0.05, 0.9, 0.9])
        xarray_flat = xarray.flatten()
        yarray_flat = yarray.flatten()
        zarray_flat = zarray.flatten()
        ax.plot(xarray_flat, yarray_flat, zarray_flat)
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
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.text_edit = None
        self.sc = None
        self.lorenz_params3 = None
        self.lorenz_params2 = None
        self.lorenz_params1 = None
        self.term_handler = Term_handler(self)
        self.eq_handler = Eq_Handler()
        th.Term_handler.load_command_base(self)
        self.equation = 0
        self.tempLor = []
        self.tempRoe = []
        self.X = []
        self.Y = []
        self.Z = []
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

        plot_button = QPushButton("Plot points")
        plot_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        load_data = QPushButton("Load from file")
        load_data.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        init_r_button = QPushButton("Rössler plot")
        init_r_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        init_r_button.pressed.connect(self.init_roessler)

        init_l_button = QPushButton("Lorenz plot")
        init_l_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        init_l_button.pressed.connect(self.init_lorenz)

        self.lorenz_params1 = QtWidgets.QLineEdit(self)
        self.lorenz_params1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lorenz_params2 = QtWidgets.QLineEdit(self)
        self.lorenz_params2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lorenz_params3 = QtWidgets.QLineEdit(self)
        self.lorenz_params3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        lorenz_label1 = QLabel("ρ:")
        lorenz_label1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_label2 = QLabel("β:")
        lorenz_label2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_label3 = QLabel("σ:")
        lorenz_label3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        lorenz_layout = QVBoxLayout()

        self.init_l_params = QLabel("Initial Lorenz args:")
        l_condition_layout = QHBoxLayout()
        self.init_l_condition1 = QtWidgets.QLineEdit(self)
        self.init_l_condition2 = QtWidgets.QLineEdit(self)
        self.init_l_condition3 = QtWidgets.QLineEdit(self)

        l_condition_layout.addWidget(self.init_l_condition1)
        l_condition_layout.addWidget(self.init_l_condition2)
        l_condition_layout.addWidget(self.init_l_condition3)

        menu_sublayout = QHBoxLayout()
        lorenz_layout1 = QHBoxLayout()
        lorenz_layout1.addWidget(lorenz_label1, 10)
        lorenz_layout1.addWidget(self.lorenz_params1, 90)
        lorenz_layout2 = QHBoxLayout()
        lorenz_layout2.addWidget(lorenz_label2, 10)
        lorenz_layout2.addWidget(self.lorenz_params2, 90)
        lorenz_layout3 = QHBoxLayout()
        lorenz_layout3.addWidget(lorenz_label3, 10)
        lorenz_layout3.addWidget(self.lorenz_params3, 90)
        lorenz_layout.addWidget(init_l_button)
        lorenz_layout.addLayout(lorenz_layout1)
        lorenz_layout.addLayout(lorenz_layout2)
        lorenz_layout.addLayout(lorenz_layout3)
        lorenz_layout.addWidget(self.init_l_params)
        lorenz_layout.addLayout(l_condition_layout)

        self.roessler_params1 = QtWidgets.QLineEdit(self)
        self.roessler_params1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.roessler_params2 = QtWidgets.QLineEdit(self)
        self.roessler_params2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.roessler_params3 = QtWidgets.QLineEdit(self)
        self.roessler_params3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        roessler_label1 = QLabel("a:")
        roessler_label1.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        roessler_label2 = QLabel("b:")
        roessler_label2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        roessler_label3 = QLabel("c:")
        roessler_label3.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.init_r_params = QLabel("Initial Rössler args:")
        r_condition_layout = QHBoxLayout()
        self.init_r_condition1 = QtWidgets.QLineEdit(self)
        self.init_r_condition2 = QtWidgets.QLineEdit(self)
        self.init_r_condition3 = QtWidgets.QLineEdit(self)

        r_condition_layout.addWidget(self.init_r_condition1)
        r_condition_layout.addWidget(self.init_r_condition2)
        r_condition_layout.addWidget(self.init_r_condition3)
        roessler_layout = QVBoxLayout()

        roessler_layout1 = QHBoxLayout()
        roessler_layout2 = QHBoxLayout()
        roessler_layout3 = QHBoxLayout()
        roessler_layout1.addWidget(roessler_label1, 10)
        roessler_layout1.addWidget(self.roessler_params1, 90)
        roessler_layout2.addWidget(roessler_label2, 10)
        roessler_layout2.addWidget(self.roessler_params2, 90)
        roessler_layout3.addWidget(roessler_label3, 10)
        roessler_layout3.addWidget(self.roessler_params3, 90)
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
        left_layout.addWidget(plot_button)
        left_layout.addWidget(load_data)
        left_layout.addWidget(info_label)
        left_layout.addWidget(self.info_edit)

        left.setLayout(left_layout)

        right = QFrame()
        right.setFrameShape(QFrame.StyledPanel)

        right_label = QLabel('Plot Panel:', right)
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(right_label)
        toolbar = NavigationToolbar(self.sc, self)
        right_layout.addWidget(toolbar)
        right_layout.addWidget(self.sc)
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

        vbox.addLayout(hbox_splitter, 80)
        vbox.addLayout(hbox_bottom, 20)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Chaos Simulator')

        self.text_edit.textChanged.connect(self.look_for_enter_key)

        # Just for testing 3D plotting:
        self.eq_handler.set_lorenz_conditions(28, 8 / 3, 10)
        self.tempLor = np.array([28, 8 / 3, 10])
        init_conditions = np.array([1.0, 1.0, 1.0])
        t_start = 0.0
        t_end = 40.0
        num_steps = 10000
        t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_lorenz(init_conditions, t_start, t_end, num_steps)
        self.X = xyz[:, 0]
        self.Y = xyz[:, 1]
        self.Z = xyz[:, 2]
        self.info_edit.setText(self.eq_handler.print_lorenz_eq(28, 8 / 3, 10))

        self.sc.plot3D(self.X, self.Y, self.Z)

    def look_for_enter_key(self):
        if self.text_edit.toPlainText().endswith('\n'):
            self.term_handler.get_command(self.text_edit, self.text_edit.toPlainText())

    def init_lorenz(self):
        self.info_edit.clear()
        if (self.lorenz_params1.text() != "" and self.lorenz_params2.text() != "" and self.lorenz_params3.text() != ""):
            self.eq_handler.set_lorenz_conditions(float(self.lorenz_params1.text()), float(self.lorenz_params2.text()),
                                                  float(self.lorenz_params3.text()))
            self.tempLor = np.array([float(self.lorenz_params1.text()), float(self.lorenz_params2.text()),
                                     float(self.lorenz_params3.text())])
            if (self.init_l_condition1.text() and self.init_l_condition2.text() and self.init_l_condition3.text()):
                init_conditions = np.array([float(self.init_l_condition1.text()), float(self.init_l_condition2.text()),
                                            float(self.init_l_condition3.text())])
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append(self.init_l_condition1.text())
                self.info_edit.append(self.init_l_condition2.text())
                self.info_edit.append(self.init_l_condition3.text())
            else:
                init_conditions = np.array([1.0, 1.0, 1.0])
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")

            t_start = 0.0
            t_end = 40.0
            num_steps = 10000
            t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_lorenz(init_conditions, t_start, t_end, num_steps)
            self.X = xyz[:, 0]
            self.Y = xyz[:, 1]
            self.Z = xyz[:, 2]

            self.info_edit.append(
                self.eq_handler.print_lorenz_eq(float(self.lorenz_params1.text()), float(self.lorenz_params2.text()),
                                                float(self.lorenz_params3.text())))
            self.sc.plot3D(self.X, self.Y, self.Z)
            self.equation = 0
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    def init_roessler(self):
        if self.roessler_params1.text != None and self.roessler_params2.text != None and self.roessler_params3.text != None:
            self.info_edit.clear()
            print(float(self.roessler_params1.text()))
            print(float(self.roessler_params2.text()))
            print(float(self.roessler_params3.text()))
            self.eq_handler.set_roessler_conditions(float(self.roessler_params1.text()),
                                                    float(self.roessler_params1.text()),
                                                    float(self.roessler_params1.text()))
            self.tempRoe = np.array([float(self.roessler_params1.text()), float(self.roessler_params1.text()),
                                     float(self.roessler_params1.text())])
            if self.init_r_condition1.text() and self.init_r_condition2.text() and self.init_r_condition3.text():
                init_conditions = np.array([float(self.init_r_condition1.text()), float(self.init_r_condition2.text()),
                                            float(self.init_r_condition3.text())])
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append(self.init_r_condition1.text())
                self.info_edit.append(self.init_r_condition2.text())
                self.info_edit.append(self.init_r_condition3.text())
            else:
                init_conditions = np.array([1.0, 1.0, 1.0])
                self.info_edit.append("Initial conditions set to:")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
                self.info_edit.append("1.0")
            t_start = 0.0
            t_end = 40.0
            num_steps = 10000
            t_values, xyz = self.eq_handler.runge_kutta_algorithm_4_roessler(init_conditions, t_start, t_end, num_steps)
            # debug and shit cuz roessler sometimes doesnt work - it depends on the parameter values
            # print(xyz[:, 0])
            # print(xyz[:, 1])
            # print(xyz[:, 2])
            self.X = xyz[:, 0]
            self.Y = xyz[:, 1]
            self.Z = xyz[:, 2]
            self.info_edit.append(self.eq_handler.print_roessler_eq(float(self.roessler_params1.text()),
                                                                    float(self.roessler_params2.text()),
                                                                    float(self.roessler_params3.text())))
            self.sc.plot3D(self.X, self.Y, self.Z)
            self.equation = 1
        else:
            self.info_edit.setText("ERROR: Empty parameter fields!\n")

    # def load_from_file(self):
    #
    # def save_to_file(self):
    def redraw_figure(self):
        self.sc.draw()
        self.sc.plot3D(self.X, self.Y, self.Z)

    # def set_init_conditions_roessler(self):

    # def set_init_conditions_lorenz(self):

    def print_onto_text_edit(self, text):
        self.info_edit.append(f"{text}")

    def clear_terminal(self):
        self.text_edit.clear()

    def clear_info(self):
        self.info_edit.clear()

    def get_user_Equation(self):
        return self.text_edit.toPlainText()

    def show_equation(self):
        if (self.equation == 0):
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_lorenz_eq(self.tempLor[0], self.tempLor[1], self.tempLor[2]))
        elif (self.equation == 1):
            self.info_edit.clear()
            self.info_edit.setText(self.eq_handler.print_roessler_eq(self.tempRoe[0], self.tempRoe[1], self.tempRoe[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())
