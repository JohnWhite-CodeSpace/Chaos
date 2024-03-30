import keyboard
import sys
CommandList={}
class Term_handler():
    def __init__(self, main_frame):
        self.main_frame = main_frame

    def get_command(self, textedit, text):
        print('getting command')
        command = text.strip().split('\n')
        print(command[-1])
        print('split')
        if CommandList is not None:
            print("iterate")
            num=0
            while(command[-1] != CommandList[num][0]):
                print(f"iteration index: {num} looking for command {command[-1]}")
                num += 1
            print("condition met")
            print(f"Command list index: {CommandList[num][1]}")
        value = int(CommandList[num][1])
        print("Function gets here")
        print(value)
        self.check_command_type(value, textedit)

    def check_command_type(self, commandNum, textedit):
        print("looking for method")
        if commandNum == 0:
            print("Exiting")
            self.exit_command()
        elif commandNum == 1:
            print("Refreshing")
            # self.refresh_command()

        elif commandNum==9:
            print("Clear terminal")
            self.clear_terminal(textedit)
        else:
            print("some bs")

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
    #
    def exit_command(self):
        sys.exit()
    def refresh_command(self):
        print("shit on my tits")

    #def plot_command(self):

    #def load_file_command(self):

    #def show_eq_command(self):

    #def save_session_command(self):

    #def get_equation(self):

    def clear_terminal(self, textedit):
        textedit.clear()





