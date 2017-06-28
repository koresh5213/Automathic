import Logic as lg
import random

class AmericanTest:

    def __init__(self, qtype=lg.EquationExercise, number_of_questions=10):

        self.question_array = []
        self.answer_matrix = [[0 for x in range(3)] for y in range(number_of_questions)]
        self.right_answers = []
        self.user_choice = [-1 for x in range(number_of_questions)]

        for i in range(number_of_questions):

            self.question_array.append(qtype(diff=i))
            ##lg.ExpressionExercise(complications=int(1 + i/6), variables=int(1+(i/4)))

        for question in range (number_of_questions):
            for answer in range(3):
                ok = -1
                while ok == -1:
                    current_symbols = self.question_array[question].get_symbols()
                    self.answer_matrix[question][answer] = self.question_array[question].create_a_random_answer(current_symbols)

                    ok = 1
                    if self.question_array[question].get_solution().is_identical(self.answer_matrix[question][answer]) == 1:
                        ok = -1
                    for prev_ans in  range(answer):
                        if self.answer_matrix[question][prev_ans].is_identical(self.answer_matrix[question][answer])==1:
                            ok =-1
                    ##for compare in range(answer):



            self.right_answers.append(random.randrange(0, 4))


    def accept_answer(self, question, answer):
        self.user_choice[question] = answer

    def number_of_questions(self):
        return len(self.question_array)

    def calc_grade(self):
        factor = 100 / len(self.question_array)
        grade = 0;

        for question in range(len(self.question_array)):
            if self.right_answers[question] == self.user_choice[question]:
                grade+=factor

        return grade

    def test_to_string(self):
        s = "Test \n"
        for question in range(len(self.question_array)):
            s += ""; s +=str(question+1); s += ". ";
            s += self.question_array[question].exercise_to_string()
            s+="\n"
            s+= self.answer_to_string(question)
            s+="\n"

        return s

    def question_to_string(self, question_number):
        s=""; s += self.question_array[question_number].exercise_to_string(); s += "\n";

        return s

    def answer_to_string(self, question_number):
        s=""
        right_answer = self.right_answers[question_number]

        letters= ["a", "b", "c", "d"]
        wrong_answer_index = 0

        for i in range(4):
            if i == right_answer:
                s += "  "
                s += letters[i];
                s += ". ";
                s += self.question_array[question_number].solution_to_string();
                s += "\n";

            else:
                s += "  "
                s += letters[i]; s += ". "
                s += self.answer_matrix[question_number][wrong_answer_index].to_string()
                s += "\n"
                wrong_answer_index=wrong_answer_index+1
        return s

    def solution_to_string(self):
        s=""
        i=1
        for question in self.question_array:
            s += str(i); s+= ". ";
            s += str(self.right_answers[question]); s += "\n"
            i=i+1
        return s

    def get_question_class(self, question_number):
        try:
            return self.question_array[question_number]
        except:
            return -1;

    def to_pdf(self):
        from fpdf import FPDF
        pdf = FPDF()
        letter_list = ["a", "b", "c", "d"]
        pdf.add_page()
        pdf.set_font('Courier', 'B', 16)
        dx=180; dy=10; cy=20
        pdf.text(10, 10, "American test by: Automathica")
        for question in range(len(self.question_array)):
            if cy + 15 > 270:
                cy = 15
                pdf.add_page()
            cy=pdf.get_y()+15
            pdf.set_xy(10, cy)
            text = str(question+1); text+=". "
            text += self.question_array[question].exercise_to_string()
            pdf.multi_cell(dx, dy, text ,1,1)

            subtract = 0 ## indicates to the loop wether or not we passed right answer
            for answer in range(4):
                if cy + 10 > 270:
                    cy = 25
                cy=pdf.get_y()+4
                pdf.set_xy(20, cy)
                text = letter_list[answer]; text += ". "

                if answer == self.right_answers[question]:
                    text += self.question_array[question].pro.solution.to_string()
                    subtract = 1

                else:
                    text += self.answer_matrix[question][answer-subtract].to_string()
                pdf.multi_cell(dx, dy, text, 0, 1)

        pdf.output('tuto15.pdf', 'F')

