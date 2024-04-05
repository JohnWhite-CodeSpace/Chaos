import sys
import re

<<<<<<< Updated upstream
=======
import numpy as np
from PyQt5.QtCore import QRegExp

import main

>>>>>>> Stashed changes
CommandList={}
class Term_handler():
    def __init__(self, main_frame):
        self.main_frame = main_frame


    def get_command(self, textedit, text):
        commandcheck = 0
        command = text.split('\n')
        foundcom = self.get_last_non_empty_line(command)
        if CommandList is not None:
            num=0
            while(num<=len(CommandList)-1):
                if(foundcom == CommandList[num][0]):
                    value = int(CommandList[num][1])
                    print(value)
                    self.check_command_type(value, textedit)
                    commandcheck=1
                    break
                num += 1
        if(commandcheck==0):
            self.main_frame.print_onto_text_edit(f"ERROR: There is no such command as '{foundcom}'!")


    def get_last_non_empty_line(self, lines):
        for line in reversed(lines):
            if line.strip():
                return line

    def check_command_type(self, commandNum, textedit):
        print("looking for method")
        if commandNum == 0: # exit
            sys.exit()

        elif commandNum == 1: # refresh
            self.main_frame.redraw_figure()
<<<<<<< Updated upstream
        elif commandNum == 2:
            print("2dplot")
        elif commandNum == 3:
            print("3dplot")
        elif commandNum == 7:
            self.main_frame.show_equation()
        elif commandNum==10:
            self.main_frame.clear_terminal()
        elif commandNum==11:
            self.main_frame.clear_info()
        elif commandNum==12:
=======

        elif commandNum == 5:  # load plot
            self.main_frame.print_onto_text_edit("loading plot... \n")
            self.load_plot()

        elif commandNum == 6:  # load session
            self.main_frame.print_onto_text_edit("loading session... \n")


        elif commandNum == 7: # show equation
            self.main_frame.show_equation()

        elif commandNum == 8:  # save plot
            self.main_frame.print_onto_text_edit("saving plot...  \n")
            self.save_plot()

        elif commandNum == 9:  # save session
            self.main_frame.print_onto_text_edit("saving session...  \n")

        elif commandNum==11: # opcja clear terminal
            self.main_frame.clear_terminal()

        elif commandNum==12: # clear infopanel
            self.main_frame.clear_info()

        elif commandNum==13: # help
>>>>>>> Stashed changes
            self.main_frame.print_onto_text_edit("List of console commands: \n")
            for i in CommandList:
                self.main_frame.print_onto_text_edit(CommandList[i][0])
                print(CommandList[i][0])
        else:
            print("some debug bullshit")
    def load_command_base(self):
        file = open("command_list.txt")
        linenum = 0
        while True:
            line = file.readline()
            if not line:
                print("Command List loaded!")
                print("List of commands:")
                for command in CommandList:
                    print(CommandList[command])
                break

            temparr = line.split("->")
            if len(temparr) >= 2:
                CommandList[linenum] = (
                    CommandList.get(linenum, ("", 0))[0] + temparr[0],
                    CommandList.get(linenum, ("", 0))[1] + int(temparr[1])
                )
                linenum += 1
            else:
                print(f"Ignoring invalid line: {line.strip()}")
        file.close()

<<<<<<< Updated upstream
    # def get_User_Equation2d(self):
    #     equation = self.main_frame.get_user_Equation()
    #     if 'x' in equation and 'y' in equation:
    #
    #         if '^' in equation:
=======
    def save_plot(self):
        file = open("saved_plots.txt", 'w')
        if len(self.main_frame.eq_handler.lorenz_constants) != 0:
            file.write(str(self.main_frame.eq_handler.lorenz_constants['rho']))
            file.write(",")
            file.write(str(self.main_frame.eq_handler.lorenz_constants['beta']))
            file.write(",")
            file.write(str(self.main_frame.eq_handler.lorenz_constants['sigma']))
            file.write("\n")

        if len(self.main_frame.eq_handler.roessler_constants) != 0:
            file.write(str(self.main_frame.eq_handler.roessler_constants['a']))
            file.write(",")
            file.write(str(self.main_frame.eq_handler.roessler_constants['b']))
            file.write(",")
            file.write(str(self.main_frame.eq_handler.roessler_constants['c']))

        self.main_frame.print_onto_text_edit("saved plot for parameters")

    def load_plot(self):
        file = open("saved_plots.txt", 'r')
        tmp = file.read()
        txt = tmp.split("\n")

        if txt[0] == "":
            print("no lorenz parameters")
        else:
            tmp = txt[0].split(',')

            print(float(tmp[0]),float(tmp[1]),float(tmp[2]))
            self.main_frame.eq_handler.set_lorenz_conditions(tmp[0],tmp[1],tmp[2])
>>>>>>> Stashed changes




<<<<<<< Updated upstream
=======
        if txt[1] == "":
            print("no roessler parameters")
        else:
            tmp = txt[1].split(',')
            print(float(tmp[0]),float(tmp[1]),float(tmp[2]))
            self.main_frame.eq_handler.set_roessler_conditions(tmp[0],tmp[1],tmp[2])

        self.main_frame.print_onto_text_edit("plot loaded succesfully")
>>>>>>> Stashed changes




