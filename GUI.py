import tkinter as tk
import tkinter.messagebox

from PIL import ImageTk
from PIL import Image
import random
import os
import Engine as lg
import tkinter.font as font


class MainWindow:

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
        self.canvas.pack(fill="both",expand=1)

        self.upper_frame.pack(fill="x")

        self.middle_frame.pack(fill="x")
        self.down_frame.pack(fill="x")

        self.button_font = font.Font(family='Helvetica', size=25, weight='bold')
        self.button_font_small = font.Font(family='Helvetica', size=16)

        self.start_game_button = tk.Button(self.down_frame, text="Play!", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.exercise_button = tk.Button(self.down_frame, text="Exercise", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.about_button = tk.Button(self.down_frame, text="About", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)

        self.bottom_frame_main()

        self.game_config_game = -1
        self.game_config_number = -1
        self.game_config_question = -1

        self.go_button_game = tk.Button(self.down_frame, text="Go", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.return_button= tk.Button(self.down_frame, text="Return", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)

        self.go_button_game.bind("<Button-1>", self.start_game)
        self.return_button.bind("<Button-1>", self.return_to_main)

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
        self.five_q_button = tk.Button(self.canvas, text="5",width=3, font=self.button_font_small, bg="#525286", fg="white")
        self.ten_q_button = tk.Button(self.canvas, text="10", width=3, font=self.button_font_small, bg="#525286",
                                       fg="white")
        self.fifteen_q_button = tk.Button(self.canvas, text="15", width=3, font=self.button_font_small, bg="#525286",
                                       fg="white")
        self.twenty_q_button = tk.Button(self.canvas, text="20", width=3, font=self.button_font_small, bg="#525286",
                                       fg="white")


        self.question_type_listbox = tk.Listbox(self.canvas, selectmode="single", height=3, width=25)
        self.scrollbar = tk.Scrollbar(self.question_type_listbox)
        self.scrollbar.config(command=self.question_type_listbox.yview)
        self.question_type_listbox.config(yscrollcommand = self.scrollbar.set)
        self.question_type_listbox.insert(1, "Equation")
        self.question_type_listbox.insert(2, "Expression")

        self.question_type_listbox.bind("<Button-1>", self.question_type_change())

        ##self.question_type_listbox.bind("<Button-1>", self.cha

        self.resault_button = tk.Button(self.down_frame, text="Answers", height= 1, width=9, bg="#525286", fg="white", font=self.button_font)
        self.resault_button.bind("<Button-1>", self.calc_grade)

        self.five_q_button.bind("<Button-1>", lambda event, number=5: self.question_number_change(number))
        self.ten_q_button.bind("<Button-1>", lambda event, number=10: self.question_number_change(number))
        self.fifteen_q_button.bind("<Button-1>", lambda event, number=15: self.question_number_change(number))
        self.twenty_q_button.bind("<Button-1>", lambda event, number=20: self.question_number_change(number))

        self.new_worksheet_button = tk.Button(self.canvas, text="New", width=11, font=self.button_font_small, bg="#525286", fg="white")
        self.load_worksheet_button = tk.Button(self.canvas, text="Load", width=11, font=self.button_font_small, bg="#525286", fg="white")

        ##self.american_test_button.bind("<Button-1>", self.american_test_click)
        self.american_test_button.bind("<Button-1>", lambda event, string="american": self.game_type_change(string))
        self.regular_test_button.bind("<Button-1>", lambda event, string="regular": self.game_type_change(string))
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

        self.answer_mode = "no"




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
        self.five_q_button.place_forget()
        self.ten_q_button.place_forget()
        self.fifteen_q_button.place_forget()
        self.twenty_q_button.place_forget()
        self.question_type_listbox.place_forget()

        self.canvas.delete("all")

    def bottom_frame_main(self):
        self.clean_bottom_frame()
        self.start_game_button.pack(side="left", padx=(620 / 9))
        self.exercise_button.pack(side="left", padx=(620 / 9))
        self.about_button.pack(side="left", padx=(620 / 9))

    def clean_bottom_frame(self):
        self.start_game_button.pack_forget()
        self.exercise_button.pack_forget()
        self.about_button.pack_forget()
        try:
            self.go_button_game.pack_forget()
            self.return_button.pack_forget()
            self.resault_button.pack_forget()
        except:
            return

    def start_game_click(self, event):
        h = self.middle_frame.winfo_height()
        w = self.middle_frame.winfo_width()

        self.clean_middle_frame()
        self.bottom_frame_game_mode()

        print("here")
        self.american_test_button.place(y=h / 4, x=w / 5)
        self.regular_test_button.place(y=h / 4, x=2 * w / 5)

        self.five_q_button.place(y= h / 2, x= w/5)
        self.ten_q_button.place(y= h / 2, x= 1.5*w/5)
        self.fifteen_q_button.place(y= h / 2, x= 2*w/5)
        self.twenty_q_button.place(y= h / 2, x= 2.5*w/5)

        self.canvas.create_text(265, h/5,text="Game type", font="Helvetica 20")
        self.canvas.create_text(300, 2*h / 5 + 20, text="Question number", font="Helvetica 20")
        self.canvas.create_text(280, 3* h / 5+30, text="Question type", font="Helvetica 20")

        self.question_type_listbox.place(x=w/5, y=2*h/3 + 25)
        self.scrollbar.place(x=135)




    def exercise_click(self, event):
        h = self.middle_frame.winfo_height()
        w = self.middle_frame.winfo_width()

        self.clean_middle_frame()
        self.bottom_frame_main()

        self.new_worksheet_button.place(y=h / 2, x=w / 5)
        self.load_worksheet_button.place(y=h / 2, x=3 * w / 5)

    def about_click(self, event):

        self.clean_middle_frame()

    def american_test_begin(self, number_of_questions, qtype=lg.lg.ExpressionExercise):
        self.current_american_test = lg.AmericanTest(number_of_questions=number_of_questions, qtype=qtype)
        self.current_question = 0

        self.paint_american_question()

    def start_game(self, event):
        self.question_type_change()
        self.answer_mode = "no"
        ##s="instart\n"; s+="number= "; s+=str(self.game_config_number); s+="\ntype: "; s+=str(self.game_config_question)
        ##s+="\ngame= ";s+=str(self.game_config_game); print(s)
        if self.game_config_number is -1 or self.game_config_number is -1:
            return

        type = lg.lg.ExpressionExercise

        if self.game_config_question == "Equation":
            type = lg.lg.EquationExercise

        if self.game_config_game is "american":
            self.american_test_begin(self.game_config_number, qtype=type)

        self.update_down_frame_for_game_mode()

    def update_down_frame_for_game_mode(self):
        self.clean_bottom_frame()
        self.start_game_button.config(text="New")
        self.start_game_button.pack(side="left", padx=(620 / 9))
        self.exercise_button.pack(side="left", padx=(620 / 9))
        self.resault_button.pack(side="left", padx=(620 / 9))


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

        if self.answer_mode is "yes":
            for button in range(len(temp)):
                if button == self.current_american_test.user_choice[self.current_question]:
                    temp[button].config(bg="red")

                if button == self.current_american_test.right_answers[self.current_question]:
                    temp[button].config(bg="green")

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


    def show_conf_test_frame(self):
        self.clean_middle_frame()

    def game_type_change(self, type):
        if type is "american":
            self.game_config_game = "american"
            self.american_test_button.config(bg="white", fg="black")
            self.regular_test_button.config(bg="#525286", fg="white")

        if type is "regular":
            self.game_config_game = "regular"
            self.regular_test_button.config(bg="white", fg="black")
            self.american_test_button.config(bg="#525286", fg="white")

    def question_number_change(self, number):
        self.game_config_number = number
        temp_map = [5,10,15,20]

        button_list= [self.five_q_button,self.ten_q_button,self.fifteen_q_button, self.twenty_q_button]

        for button in button_list:
            button.config(bg="#525286", fg="white")

        button_list[temp_map.index(number)].config(bg="white", fg="black")

    def question_type_change(self):
        self.game_config_question = self.question_type_listbox.get("anchor")
        return

    def bottom_frame_game_mode(self):
        self.clean_bottom_frame()

        self.go_button_game.pack(side="left", padx=(620 / 9))
        self.return_button.pack(side="left", padx=(620 / 9))

    def return_to_main(self, event):
        self.clean_middle_frame()
        self.bottom_frame_main()

    def calc_grade(self, event):
        s="Your score: "; s+=str(self.current_american_test.calc_grade()); s+="/100"
        self.write_to_information_bar(s)
        self.answer_mode = "yes"
        self.paint_american_question()


##font=("Courier", 18)
root = tk.Tk()  # This is the main fram
root.withdraw()

current_window = tk.Toplevel(root)
current_window.geometry('{}x{}'.format(1000, 620))
current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)

m = MainWindow(current_window)


root.mainloop()  # keeps the window open