CommandList={}
class Term_handler():

    def __init__(self):
        super(Term_handler, self).__init__()
    def get_command(self, command):
        print("something")

    def load_command_base(self):
        file = open("command_list.txt")
        linenum = 1
        while True:
            line = file.readline()
            temparr = line.split("->")
            CommandList[linenum] = CommandList.get(linenum,("",""))
            CommandList[linenum](
                CommandList[linenum][0] + temparr[0],
                CommandList[linenum][1] + temparr[1]
            )
            linenum+=1

            if not line:
                break

    #def exit_command(self):

    #def refresh_command(self):

    #def plot_command(self):

    #def load_file_command(self):

    #def show_eq_command(self):

    #def save_session_command(self):




