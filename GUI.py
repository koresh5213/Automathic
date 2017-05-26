import tkinter as tk
import tkinter.messagebox

from PIL import ImageTk
from PIL import Image
import random
import os
import Engine as lg
import tkinter.font as font


class MainWindow2:

    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        master.configure(background='#232357') ## blue background

        self.upper_frame = tk.Frame(master, height=100, bg="#612D68")      ##welcome message
        self.middle_frame = tk.Frame(master, height=400)     ##where the canvas
        self.down_frame = tk.Frame(master, height=120, bg='#232357')

        self.upper_frame.pack_propagate(0)
        self.middle_frame.pack_propagate(0) ## Makes that buttonns dont change the height
        self.down_frame.pack_propagate(0)

        self.canvas = tk.Canvas(self.middle_frame)
        self.canvas.pack(fill="both")

        self.upper_frame.pack(fill="x")

        self.middle_frame.pack(fill="x")
        self.down_frame.pack(fill="x")

        self.button_font = font.Font(family='Helvetica', size=25, weight='bold')
        self.button_font_small = font.Font(family='Helvetica', size=16)

        self.start_game_button = tk.Button(self.down_frame, text="Play!", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.exercise_button = tk.Button(self.down_frame, text="Exercise", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.about_button = tk.Button(self.down_frame, text="About", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)

        self.start_game_button.pack(side="left", padx=(620/9))
        self.exercise_button.pack(side="left", padx=(620/9))
        self.about_button.pack(side="left", padx=(620/9))

        self.information_bar = tk.Text(self.middle_frame, height=1 )
        self.write_to_information_bar("Welcome to Automathica!")

        self.welcome_label = tk.Label(self.upper_frame, text="Automathica")
        self.welcome_label.config(font=("Courier", 30))
        self.welcome_label.pack(fill="y")

        self.start_game_button.bind("<Enter>", lambda event, string="Start a new game!": self.write_to_information_bar(string))
        self.exercise_button.bind("<Enter>", lambda event, string="Create a brand new worksheet, or load and solve pre-created one": self.write_to_information_bar(string))
        self.about_button.bind("<Enter>", lambda event, string="Find out who is behind all of this": self.write_to_information_bar(string))

        self.exercise_button.bind("<Button-1>", self.exercise_click)
        self.start_game_button.bind("<Button-1>", self.start_game_click)
        self.about_button.bind("<Button-1>", self.about_click)

        self.american_test_button = tk.Button(self.canvas, text="American", width=11, font=self.button_font_small, bg="#525286", fg="white")
        self.regular_test_button = tk.Button(self.canvas, text="Regular", width=11, font=self.button_font_small, bg="#525286", fg="white")
        self.new_worksheet_button = tk.Button(self.canvas, text="New", width=11, font=self.button_font_small, bg="#525286", fg="white")
        self.load_worksheet_button = tk.Button(self.canvas, text="Load", width=11, font=self.button_font_small, bg="#525286", fg="white")

        self.american_test_button.bind("<Button-1>", self.american_test_click)
        self.regular_test_button.bind("<Button-1>", self.regular_test_click)
        self.american_test_button.bind("<Enter>", lambda event, string="Start american test, select the correct answer": self.write_to_information_bar(string))
        self.regular_test_button.bind("<Enter>", lambda event, string="Start regular test, enter the answer": self.write_to_information_bar(string))
        self.new_worksheet_button.bind("<Enter>", lambda event, string="Create a new worksheet, exoprt to pdf or Automathica format": self.write_to_information_bar(string))
        self.load_worksheet_button.bind("<Enter>", lambda event, string="If you have Automathica format file": self.write_to_information_bar(string))

        self.american_answer_a = tk.Button(self.middle_frame, text="a", width=2, height=1, font=self.button_font_small,bg="black", fg="white")
        self.american_answer_a.bind("<Button-1>",lambda event, answer=0: self.chose_answer(answer) )
        self.american_answer_b = tk.Button(self.middle_frame, text="b", width=2, height=1, font=self.button_font_small,bg="black", fg="white")
        self.american_answer_b.bind("<Button-1>", lambda event, answer=1: self.chose_answer(answer))
        self.american_answer_c = tk.Button(self.middle_frame, text="c", width=2, height=1, font=self.button_font_small,bg="black", fg="white")
        self.american_answer_c.bind("<Button-1>", lambda event, answer=2: self.chose_answer(answer))
        self.american_answer_d = tk.Button(self.middle_frame, text="d", width=2, height=1, font=self.button_font_small,bg="black", fg="white")
        self.american_answer_d.bind("<Button-1>", lambda event, answer=3: self.chose_answer(answer))

        self.next_button = tk.Button(self.middle_frame, text="Next", width=4, height=1, font=self.button_font_small)
        self.next_button.bind("<Button-1>", self.next_question)
        self.prev_button = tk.Button(self.middle_frame, text="Prev", width=4, height=1, font=self.button_font_small)
        self.prev_button.bind("<Button-1>", self.prev_question)

        self.current_american_test = lg.AmericanTest()
        self.current_question = -1



    def write_to_information_bar(self, string):
        self.information_bar.config(state="normal")
        self.information_bar.delete("1.0", "end")
        self.information_bar.insert("1.0", string)

        self.information_bar.pack(side="bottom", fill="x")
        self.information_bar.tag_add("all", "1.0")
        self.information_bar.tag_config("all", justify="center")

        self.information_bar.config(state="disabled")

    def clean_middle_frame(self):
        self.american_test_button.place_forget()
        self.regular_test_button.place_forget()
        self.new_worksheet_button.place_forget()
        self.load_worksheet_button.place_forget()
        self.american_answer_a.place_forget()
        self.american_answer_b.place_forget()
        self.american_answer_c.place_forget()
        self.american_answer_d.place_forget()
        self.next_button.place_forget()
        self.prev_button.place_forget()

        self.canvas.delete("all")

    def start_game_click(self, event):
        h = self.middle_frame.winfo_height()
        w = self.middle_frame.winfo_width()

        self.clean_middle_frame()

        self.american_test_button.place(y=h / 2, x=w / 5)
        self.regular_test_button.place(y=h / 2, x=3 * w / 5)

    def exercise_click(self, event):
        h = self.middle_frame.winfo_height()
        w = self.middle_frame.winfo_width()

        self.clean_middle_frame()

        self.new_worksheet_button.place(y=h / 2, x=w / 5)
        self.load_worksheet_button.place(y=h / 2, x=3 * w / 5)

    def about_click(self, event):
        self.clean_middle_frame()

    def american_test_click(self, event):
        self.current_american_test = lg.AmericanTest()
        self.current_question = 0

        self.paint_american_question()

    def regular_test_click(self,event):
        current_test = lg.AmericanTest()

        self.paint_american_question()

    def chose_answer(self, answer):
        self.current_american_test.accept_answer(self.current_question, answer)
        self.light_answer_buttons()

    def light_answer_buttons(self):
        temp = [self.american_answer_a, self.american_answer_b, self.american_answer_c, self.american_answer_d]

        for button in range(len(temp)):
            if button == self.current_american_test.user_choice[self.current_question]:
                temp[button].config(bg="orange")

            else:
                temp[button].config(bg="black")

    def paint_american_question(self):
        test = self.current_american_test
        question_number = self.current_question
        self.clean_middle_frame()

        self.american_question_font = font.Font(family='Helvetica', size=20)

        self.canvas.create_text(20, 20, text=str(self.current_question + 1), font=self.button_font)

        self.canvas.create_text(500, 100, text=test.question_to_string(question_number),
                                font=self.american_question_font)
        self.canvas.create_text(500, 200, text=test.answer_to_string(question_number),
                                font="Ariel 12")

        self.american_answer_a.place(x=1000 / 6, y=260)
        self.american_answer_b.place(x=1000 / 6 * 2, y=260)
        self.american_answer_c.place(x=1000 / 6 * 3, y=260)
        self.american_answer_d.place(x=1000 / 6 * 4, y=260)

        self.next_button.place(x= 1000/2, y = 320)
        self.prev_button.place(x=1000 / 2 -100, y=320)
        self.light_answer_buttons()

    def next_question(self, event):
        if self.current_question == -1 or self.current_question == self.current_american_test.number_of_questions() -1:
            return

        try:
            self.current_question = self.current_question + 1
            self.paint_american_question()
            self.score()
        except:
            pass

    def prev_question(self, event):
        if self.current_question == -1 or self.current_question == 0:
            return

        try:
            self.current_question = self.current_question - 1
            self.paint_american_question()
            self.score()
        except:
            pass

    ##def american_question_parameter_page(self):


    def score(self):
        print(str(self.current_american_test.calc_grade()))


##font=("Courier", 18)
root = tk.Tk()  # This is the main fram
root.withdraw()

current_window = tk.Toplevel(root)
current_window.geometry('{}x{}'.format(1000, 620))
current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)

m = MainWindow2(current_window)


root.mainloop()  # keeps the window open
