import re
import sys
CommandList = {}

class TerminalHandler:
    """
    Class used for execution and management of commands from text passed by terminal.

    Attributes
        main_frame - UI class object used for outside function execution

    Methods
        get_command(self, textedit, text) - determines if text matches any know command and assigns it value.\n
        get_last_non_empty_line(self, lines) - cuts empty lines from user input.\n
        check_command_type(self, commandNum, textedit) - determines what command should be executed.\n
        load_command_base(self) - loads commands from .txt file\n
        save_plot(self) - saves plot parameters to .txt file\n
        load_plot(self) - loads plot parameters from .txt file\n
    """
    def __init__(self, main_frame):
        """
        Initializes Term_handler class object while passing an external main_frame argument for command execution in the MainFrame UI.

        :param main_frame: UI class object used for outside function execution
        :type main_frame: MainFrame
        """
        self.main_frame = main_frame

    def get_command(self, textedit, text):
        """
        Determines if text matches any know commmand and assigns it its enum value based on loaded CommandList

        :param textedit: does nothing
        :param text: string to evaluate
        :type text: string
        :return: void
        """
        commandcheck = 0
        command = text.split('\n')
        foundcom = self.get_last_non_empty_line(command)
        if CommandList is not None:
            num = 0
            while num <= len(CommandList) - 1:
                if foundcom == CommandList[num][0]:
                    value = int(CommandList[num][1])
                    print(value)
                    self.check_command_type(value, textedit)
                    commandcheck = 1
                    break
                num += 1
        if commandcheck == 0:
            self.main_frame.print_onto_info_edit(f"ERROR: There is no such command as '{foundcom}'!")

    def get_last_non_empty_line(self, lines):
        """
        Cuts empty lines from user input.

        :param lines: input text from terminal
        :type lines: str
        :return: last non-empty line
        :rtype: str
        """

        for line in reversed(lines):
            if line.strip():
                return line

    def check_command_type(self, commandNum, textedit):
        """
        Determines what command should be executed based on signal send by get_command()

        :param commandNum: signal send by get_command()
        :type commandNum: int
        :param textedit: does nothing
        """

        print("looking for method")
        if commandNum == 0:  # exit
            sys.exit()
        elif commandNum == 1:  # refresh
            self.main_frame.redraw_figure()
        elif commandNum == 2:  # plot 2d
            print("2dplot")
        elif commandNum == 3:  # plot 3d
            print("3dplot")
        elif commandNum == 4:  # plot lorenz
            print("plot Lorenz")
        elif commandNum == 5:  # plot roessler
            print("plot Roessler")
        elif commandNum == 6:  # load plot
            self.main_frame.print_onto_info_edit("loading plot... \n")
            self.load_plot()
        elif commandNum == 7:  # load session
            self.main_frame.print_onto_info_edit("loading session... \n")
        elif commandNum == 8:  # show equation
            self.main_frame.show_equation()
        elif commandNum == 9:  # save plot
            self.main_frame.print_onto_info_edit("saving plot...  \n")
            self.save_plot()
        elif commandNum == 10:  # save session
            self.main_frame.print_onto_info_edit("saving session...  \n")
        elif commandNum == 11:  # clear terminal
            self.main_frame.clear_terminal()
        elif commandNum == 12:  # clear infopanel
            self.main_frame.clear_info()
        elif commandNum == 13:  # help
            self.main_frame.print_onto_info_edit("List of console commands: \n")
            for i in CommandList:
                self.main_frame.print_onto_info_edit(CommandList[i][0])
                print(CommandList[i][0])
        else:
            print("no such command")

    def load_command_base(self):
        """
        Loads available commands from command_list.txt and transforms into an enum following pattern:\n
        [enum string]->[enum iterator]
        """
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
        """
        Saves given parameters from textfields to a saved_plots.txt file.

        The parameters come from lorenz and roessler parameters & start
        conditions, as well as stop, start & step conditions, they are as saved as:
        ______________________________________________\n
        rho,beta,sigma\n
        initial X,initial Y, initial Z (for Lorenz)\n
        a,b,c\n
        initial X,initial Y, initial Z (for Roessler)\n
        stary,stop,step\n
        ______________________________________________
        """

        file = open("saved_plots.txt", 'w')
        # lorenz parameters
        file.write(self.main_frame.lor_params_rho.text())
        file.write(",")
        file.write(self.main_frame.lor_params_beta.text())
        file.write(",")
        file.write(self.main_frame.lor_params_sigma.text())
        file.write("\n")

        # lorenz start condition
        file.write(self.main_frame.lor_init_condition_rho.text())
        file.write(",")
        file.write(self.main_frame.lor_init_condition_beta.text())
        file.write(",")
        file.write(self.main_frame.lor_init_condition_sigma.text())
        file.write("\n")

        # roessler parameters
        file.write(self.main_frame.roe_params_a.text())
        file.write(",")
        file.write(self.main_frame.roe_params_b.text())
        file.write(",")
        file.write(self.main_frame.roe_params_c.text())
        file.write("\n")

        # roessler start condition
        file.write(self.main_frame.roe_init_condition_a.text())
        file.write(",")
        file.write(self.main_frame.roe_init_condition_b.text())
        file.write(",")
        file.write(self.main_frame.roe_init_condition_c.text())
        file.write("\n")

        # stop start step
        file.write(self.main_frame.step_start.text())
        file.write(",")
        file.write(self.main_frame.step_stop.text())
        file.write(",")
        file.write(self.main_frame.step_count.text())

        file.close()

        self.main_frame.print_onto_info_edit("saved plot for parameters")

    def load_plot(self):
        """
        Loads parameters from a previously saved saved_plots.txt file.

        The parameters are saved in "0,0,0 /n" format by .save_plot()
        and can be used to recall previous results of the program.
        """

        file = open("saved_plots.txt", 'r')
        tmp = file.read()
        txt = tmp.split("\n")

        # load lorenz parameters
        if txt[0] == "":
            print("no lorenz parameters")
        else:
            tmp = txt[0].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.lor_params_rho.setText(tmp[0])
            self.main_frame.lor_params_beta.setText(tmp[1])
            self.main_frame.lor_params_sigma.setText(tmp[2])

        # load lorenz conditions
        if txt[1] == "":
            print("no lorenz starting conditions")
        else:
            tmp = txt[1].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.lor_init_condition_rho.setText(tmp[0])
            self.main_frame.lor_init_condition_beta.setText(tmp[1])
            self.main_frame.lor_init_condition_sigma.setText(tmp[2])

        # load roessler parameters
        if txt[2] == "":
            print("no roessler parameters")
        else:
            tmp = txt[2].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.roe_params_a.setText(tmp[0])
            self.main_frame.roe_params_b.setText(tmp[1])
            self.main_frame.roe_params_c.setText(tmp[2])

        # load roessler conditions
        if txt[3] == "":
            print("no roessler starting conditions")
        else:
            tmp = txt[3].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.roe_init_condition_a.setText(tmp[0])
            self.main_frame.roe_init_condition_b.setText(tmp[1])
            self.main_frame.roe_init_condition_c.setText(tmp[2])

        # load step conditions
        if txt[4] == "":
            print("no step conditions")
        else:
            tmp = txt[4].split(',')
            print(tmp[0], tmp[1], tmp[2])
            self.main_frame.step_start.setText(tmp[0])
            self.main_frame.step_stop.setText(tmp[1])
            self.main_frame.step_count.setText(tmp[2])

        file.close()
        self.main_frame.print_onto_info_edit("plot loaded successfully")


