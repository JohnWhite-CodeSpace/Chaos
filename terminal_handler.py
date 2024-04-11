import sys
import re

import numpy as np
from PyQt5.QtCore import QRegExp


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
        elif commandNum == 2:
            print("2dplot")
        elif commandNum == 3:
            print("3dplot")
        elif commandNum == 4:
            print("plot Lorenz")
        elif commandNum == 5:
            print("plot Roessler")
        elif commandNum == 6:  # load plot
            self.main_frame.print_onto_text_edit("loading plot... \n")
            self.load_plot()
        elif commandNum == 7:  # load session
            self.main_frame.print_onto_text_edit("loading session... \n")
        elif commandNum == 8: # show equation
            self.main_frame.show_equation()
        elif commandNum == 9:  # save plot
            self.main_frame.print_onto_text_edit("saving plot...  \n")
            self.save_plot()
        elif commandNum == 10:  # save session
            self.main_frame.print_onto_text_edit("saving session...  \n")
        elif commandNum==11: # opcja clear terminal
            self.main_frame.clear_terminal()
        elif commandNum==12: # clear infopanel
            self.main_frame.clear_info()
        elif commandNum==13: # help
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

    # def get_User_Equation2d(self):
    #     equation = self.main_frame.get_user_Equation()
    #     if 'x' in equation and 'y' in equation:
    #
    #         if '^' in equation:
    def save_plot(self):
        file = open("saved_plots.txt", 'w')
        # lorenz parameters
        file.write(self.main_frame.lorenz_params1.text())
        file.write(",")
        file.write(self.main_frame.lorenz_params2.text())
        file.write(",")
        file.write(self.main_frame.lorenz_params3.text())
        file.write("\n")

        # lorenz start condition
        file.write(self.main_frame.init_l_condition1.text())
        file.write(",")
        file.write(self.main_frame.init_l_condition2.text())
        file.write(",")
        file.write(self.main_frame.init_l_condition3.text())
        file.write("\n")

        # roessler parameters
        file.write(self.main_frame.roessler_params1.text())
        file.write(",")
        file.write(self.main_frame.roessler_params2.text())
        file.write(",")
        file.write(self.main_frame.roessler_params3.text())
        file.write("\n")

        # roessler start condition
        file.write(self.main_frame.init_r_condition1.text())
        file.write(",")
        file.write(self.main_frame.init_r_condition2.text())
        file.write(",")
        file.write(self.main_frame.init_r_condition3.text())
        file.write("\n")

        # stop start step
        file.write(self.main_frame.step_start.text())
        file.write(",")
        file.write(self.main_frame.step_stop.text())
        file.write(",")
        file.write(self.main_frame.step_count.text())



        self.main_frame.print_onto_text_edit("saved plot for parameters")

    def load_plot(self):
        file = open("saved_plots.txt", 'r')
        tmp = file.read()
        txt = tmp.split("\n")

        if txt[0] == "":
            print("no lorenz parameters")
        else:
            tmp = txt[0].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.lorenz_params1.setText(tmp[0])
            self.main_frame.lorenz_params2.setText(tmp[1])
            self.main_frame.lorenz_params3.setText(tmp[2])

        if txt[1] == "":
            print("no lorenz starting conditions")
        else:
            tmp = txt[1].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.init_l_condition1.setText(tmp[0])
            self.main_frame.init_l_condition2.setText(tmp[1])
            self.main_frame.init_l_condition3.setText(tmp[2])

        if txt[2] == "":
            print("no roessler parameters")
        else:
            tmp = txt[2].split(',')
            print(tmp[0],tmp[1],tmp[2])
            self.main_frame.roessler_params1.setText(tmp[0])
            self.main_frame.roessler_params2.setText(tmp[1])
            self.main_frame.roessler_params3.setText(tmp[2])

        if txt[3] == "":
            print("no roessler starting conditions")
        else:
            tmp = txt[3].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.init_r_condition1.setText(tmp[0])
            self.main_frame.init_r_condition2.setText(tmp[1])
            self.main_frame.init_r_condition3.setText(tmp[2])

        if txt[4] == "":
            print("no step conditions")
        else:
            tmp = txt[4].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.step_start.setText(tmp[0])
            self.main_frame.step_stop.setText(tmp[1])
            self.main_frame.step_count.setText(tmp[2])

        file.close()

        self.main_frame.print_onto_text_edit("plot loaded succesfully")




