from tkinter import *
from functools import partial  # To prevent unwanted windows
import pandas


class Rounds:

    def __init__(self, root):

        # Set up GUI Frame
        self.rounds_frame = Frame(root, padx=10, pady=10)
        self.rounds_frame.grid()

        self.rounds_heading = Label(self.rounds_frame,
                                    text="Fear or Fail",
                                    font=("Arial", "30", "bold",)
                                    )
        self.rounds_heading.grid(row=0)

        instructions = "Please enter enter the number of rounds you want to play between 1-113 below, then press play"

        self.rounds_instructions = Label(self.rounds_frame,
                                         text=instructions,
                                         wraplength=300, width=60,
                                         justify="left", font="11")
        self.rounds_instructions.grid(row=1, pady=20)

        self.rounds_error = Label(self.rounds_frame, text="",
                                  fg="#9C0000", font="bold")
        self.rounds_error.grid(row=3)

        self.start_frame = Frame(self.rounds_frame, padx=10, pady=10)
        self.start_frame.grid()

        self.entry_rounds_frame = Entry(self.start_frame,
                                        width=9, font=("Arial", "19"))
        self.entry_rounds_frame.grid(row=4, column=0, pady=5)

        self.start_button = Button(self.start_frame, width=12, text="Play",
                                   font=("Arial", "12", "bold",), bg="#429E9D",
                                   command=self.rounds_check)
        self.start_button.grid(row=4, column=1, pady=5)

        # Conversion, help and statistics
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=5)

        self.help_button = Button(self.button_frame, width=12, text="Help",
                                  bg="#FFCC99", font=("Arial", "12", "bold"),
                                  command=self.to_help)
        self.help_button.grid(row=5, column=0, padx=10, pady=10)

        self.statistics_button = Button(self.button_frame, width=12, text="Statistics",
                                        bg="#CCE5FF", font=("Arial", "12", "bold"))
        self.statistics_button.grid(row=5, column=1, padx=10, pady=10)

    def check_rounds(self, min_value, max_value):
        error = "Please enter the number of rounds rounds \n you want to play between 1 - 113"

        try:
            response = self.entry_rounds_frame.get()
            response = int(response)

            if response < min_value or response > max_value:
                self.rounds_error.config(text=error, fg="#9C0000")
            else:
                self.rounds_error.config(text="You chose to play {} rounds".format(response), fg="#32CD32")
                return response

        except ValueError:
            self.rounds_error.config(text=error, fg="#9C0000")

    def rounds_check(self):
        num_rounds = self.check_rounds(1, 113)
        if num_rounds:
            self.to_play(num_rounds)

    def to_help(self):
        DisplayHelp(self)

    def to_play(self, num_rounds):
        self.play_box = Toplevel()
        Quiz(self.play_box, num_rounds)

        # hide root window (i.e., hide rounds choice window).
        root.withdraw()


class Quiz:

    def __init__(self, play_box, num_rounds):
        self.play_box = play_box

        # if users press the cross at the top, closes help and
        # releases help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        # Variables used to work out statistics when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(num_rounds)

        # Initially set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)
        # Set up GUI Frame
        self.rounds_frame = Frame(self.play_box, padx=10, pady=10)
        self.rounds_frame.grid()

        self.rounds_heading = Label(self.rounds_frame,
                                    text="Round {} of {}".format(self.rounds_played, self.rounds_wanted),
                                    font=("Arial", "30", "bold",)
                                    )
        self.rounds_heading.grid(row=0)

        instructions = "QUESTION GOES HERE"

        self.rounds_instructions = Label(self.rounds_frame,
                                         text=instructions,
                                         wraplength=300, width=60,
                                         justify="left", font="11")
        self.rounds_instructions.grid(row=1, pady=10)

        self.start_frame = Frame(self.rounds_frame, padx=10, pady=10)
        self.start_frame.grid(row=1)

        self.buttons = []

        # Create buttons using a loop
        for i in range(4):
            button = Button(self.start_frame, width=15, height=2, text=f"ANS {i + 1}",
                            font=("Arial", "12", "bold",), bg="#484770", fg="#FFFFFF")
            button.grid(row=i // 2 + 2, column=i % 2, pady=5, padx=10)
            self.buttons.append(button)

        # help and statistics and next buttons
        self.button_frame = Frame(self.play_box, padx=10, pady=10)
        self.button_frame.grid(row=4)

        self.help_button = Button(self.button_frame, width=12, text="Help",
                                  bg="#FFCC99", font=("Arial", "12", "bold"),
                                  command=self.to_help)
        self.help_button.grid(row=4, column=0, padx=10, pady=10)

        self.statistics_button = Button(self.button_frame, width=12, text="Statistics",
                                        bg="#CCE5FF", font=("Arial", "12", "bold"))
        self.statistics_button.grid(row=4, column=1, padx=10, pady=10)

        self.next_button = Button(self.button_frame, width=16, text="Next Round",
                                  bg="#D5E8D4", font=("Arial", "12", "bold"))
        self.next_button.grid(row=4, column=2, padx=10, pady=10)

    def close_play(self):
        # reshow root (i.e., choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_help(self):
        DisplayHelp(self.play_box)


class DisplayHelp:

    def __init__(self, play_box):
        # setup dialogue box and background colour
        background = "#ffe6cc"

        self.help_box = Toplevel(play_box)

        # disable help button
        play_box.help_button.config(state=DISABLED)

        # if users press cross at top, closes help and
        # releases help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, play_box))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Help", bg=background,
                                        font=("Arial", "23", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Fear or Fail is a super spectacular quiz. You will be given " \
                    "4 options to choose from for each question, simply click the " \
                    "answer you want to choose, and you will be told whether you are " \
                    "right or wrong, and which answer the correct one is." \
                    "\n\n" \
                    "In order to start, simply enter the number of rounds you want to play " \
                    "between 1 and 113 rounds in the field below, and press enter or start to begin the quiz." \
                    "\n\n" \
                    "*Please note that Fear or Fail is not responsible for any harm that comes to the " \
                    "participant in the event they do not get a perfect score"

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     play_box))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue
    def close_help(self, play_box):
        # Put help button back to normal...
        play_box.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Fear or Fail")
    Rounds()
    root.mainloop()
