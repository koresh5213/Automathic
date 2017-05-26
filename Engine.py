import Logic as lg
import random

class AmericanTest:

    def __init__(self, qtype=lg.ExpressionExercise, number_of_questions=10):

        self.question_array = []
        self.answer_matrix = [[0 for x in range(3)] for y in range(number_of_questions)]
        self.right_answers = []
        self.user_choice = [-1 for x in range(number_of_questions)]

        for i in range(number_of_questions):
            self.question_array.append(lg.ExpressionExercise(complications=int(1 + i/6), variables=int(1+(i/4))))

        for question in range (number_of_questions):
            for answer in range(3):
                current_symbols = self.question_array[question].get_symbols()
                self.answer_matrix[question][answer] = self.create_a_random_asnwer(current_symbols)
                temp_expression = self.create_a_random_asnwer(current_symbols)
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

    def create_a_random_asnwer(self, symbols):
        random_expression = lg.Expression()

        for symbol in symbols:
            temp = lg.Variable(number=random.randrange(1, 15, 2), symbols=symbol)
            random_expression.add_var(temp)

        return random_expression

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
