import time

import keyboard
import sys

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
        if commandNum == 0:
            sys.exit()
        elif commandNum == 1:
            self.main_frame.redraw_figure()
        elif commandNum == 6:
            self.main_frame.show_equation()
        elif commandNum==9:
            self.main_frame.clear_terminal()
        elif commandNum==10:
            self.main_frame.clear_info()
        elif commandNum==11:
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





