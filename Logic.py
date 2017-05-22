import copy
import random

types_of_questions = ["expression", "equation"];

# This class describes a single variable used later in expressions
class Variable:
    def __init__(self, number=0, symbols=[]):
        if type(number) == type(3):
            self.number = abs(number)
        else:
            self.number = 1
        self.symbols = symbols

        if number >= 0:
            self.sign = "+"
        else:
            self.sign = "-"

        return

    def to_string(self, first_in_line="no"):
        text = ""

        if not(first_in_line == "yes" and self.sign == "+"):
            text += self.sign

        if not ((self.number is 1) and (len(self.symbols) is not 0)):
            text += str(self.number)

        for i in self.symbols:
            text = text + i

        return text

    def is_zero(self):
        return (self.number is 0) and (not self.symbols)

    def is_a_number(self):
        return not self.symbols

    def to_number(self):
        number = self.number
        if self.sign is "-":
            number *= -1

        return number

    def get_symbol(self):
        return self.symbols

    def is_identical(self, var):
        if type(var) is not Variable:
            return -1

        if self.to_number() != var.to_number():
            return -1

        for symbol in self.get_symbol():
            try:
                var.symbols.index(symbol)
            except:
                return -1
        else:
            return 1

# This class represents any expression. later used in a process and equations
class Expression:

    def __init__(self, heart=Variable(number=0)):
        self.heart = [heart]
        return

    def add_var(self, var, random_location="no"):
        if not(type(var) == Variable or type(var) == Friction):
            return

        if self.to_string() == "0":
            self.heart.pop(0)

        if random_location == "no":
            self.heart.append(var)
            return

        if len(self.heart) == 0:
            position = 0
        else:
            position = random.randrange(0, len(self.heart))

        self.heart.insert(position, var)
        return

    def to_string(self):
        text = ""
        first = "yes"
        for e in self.heart:
            if first == "yes" and type(e) == Variable:
                text += e.to_string(first_in_line="yes")
                first = "no :["
            else:
                if type(e) == Friction:
                    text += " + "
                text += e.to_string()
                text += " "
        return text

    def find_me_a_friction(self):
        frictions = []
        for var in self.heart:
            if type(var) == Friction:
                frictions.append(var)

        if len(frictions) is 0:
            return -1

        return random.choice(frictions)

    def find_me_a_number(self):
        numbers = []
        for var in self.heart:
            if type(var) == Variable:
                if var.is_a_number():
                    numbers.append(var.to_number())

        if len(numbers) is 0:
            return -1

        return random.choice(numbers)

    def remove_var(self, var):
        if not (type(var) is Variable or Friction):
            return -1

        for my_variable in self.heart:
            if var.is_identical(my_variable) == 1:
                self.heart.remove(my_variable)
                return 1
        return -1

    def find_me_a_var_of(self, symbols):
        list_of_vars = []
        for var in self.heart:
            if symbols == var.symbols:
                list_of_vars.append(var)
        if not list_of_vars:
            return -1
        return random.choice(list_of_vars)

    def find_me_a_symbol(self):
        var_list = []
        for var in self.heart:
            if not (var.is_a_number()):
                var_list.append(var)

        if len(var_list) == 0:
            return -1

        rand_var = random.choice(var_list)
        return rand_var.symbols

    def find_me_a_random_var(self):
        return self.find_me_a_var_of(self.find_me_a_symbol())

    def return_symbols(self):
        symbol_list = []
        for var in self.heart:
            if var not in symbol_list:
                symbol_list.append(var.get_symbol())

        return symbol_list

    def is_identical(self, expression):
        if type(expression) is not Expression:
            return -1

        temp_self  = copy.deepcopy(self)
        temp_other = list(expression.heart)

        if len(self.heart) != len(expression.heart):
            return -1

        for var in expression.heart:
            if temp_self.remove_var(var) == -1:
                return -1

        if not len(temp_self.heart) == 0:
            return -1

        return 1

    def is_var_in_expresssion(self, mystery):
        for variable in self.heart:
            if variable.is_identical(mystery) == 1:
                return 1
        return -1





# this class represents frictions, similar to variables.
class Friction:

    def __init__(self, numerator=Variable(), denominator=Variable()):

        self.numerator = numerator

        if denominator.number == 0 and denominator.symbols == []:
            denominator = 1  # divided by zero
        self.denominator = denominator

        return

    def to_string(self):
        text = "<"
        text += self.numerator.to_string(first_in_line="yes")
        text += " / "
        text += self.denominator.to_string(first_in_line="yes")
        text += ">"
        return text


class ExpressionProcess:

    def __init__(self, solution=Expression()):
        self.solution = solution
        self.process = [self.solution]

    def complicate_step(self, symbols, levels=1):
        last = copy.deepcopy(self.process[-1])
        dup = last

        for i in range(levels):
            rand_var_from_expression = last.find_me_a_var_of(symbols)
            if rand_var_from_expression == -1:
                return

            rand_number_to_subtract = random.randrange(1, 15, 2)

            number_to_add = rand_var_from_expression.to_number() - rand_number_to_subtract

            while number_to_add == 0:
                rand_number_to_subtract = random.randrange(1, 15, 2)

                number_to_add = rand_var_from_expression.to_number() - rand_number_to_subtract

            rand_var_to_subtract = Variable(number=rand_number_to_subtract, symbols=rand_var_from_expression.symbols)
            var_to_add = Variable(number=number_to_add, symbols=rand_var_from_expression.symbols)

            dup.remove_var(rand_var_from_expression)
            dup.add_var(rand_var_to_subtract, random_location="yes!")
            dup.add_var(var_to_add, random_location="yes!")

        self.process.append(dup)

    def to_string(self):
        text = ""
        rev = self.process[::-1]
        for e in rev:
            text += e.to_string()
            text += "\n"
        return text[:-1]

    def get_latest(self):
        return self.process[-1]

    def solution_to_sting(self):
        return self.solution.to_string()

    def get_symbols(self):
        return self.solution.return_symbols()


class ExpressionExercise:
    def __init__(self, complications=2, variables=1):

        if variables not in range(1,5):
            variables = 1

        free_var = Variable(number=random.randint(0, 10))
        solution = Expression(free_var)

        character_match = ["x", "y", "z", "a"]

        for index in range(1,variables+1):
            temp = Variable(number=random.randint(1, 10), symbols=[character_match[index-1]])
            solution.add_var(temp)

        self.pro = ExpressionProcess(solution=solution)

        self.pro.complicate_step([])
        for j in range(1,variables+1):
            self.pro.complicate_step([character_match[j-1]], levels=variables)

    def exercise_to_string(self):
        return self.pro.get_latest().to_string()

    def solution_to_string(self):
        return self.pro.solution_to_sting()

    def get_symbols(self):
        return self.pro.get_symbols()


class AmericanTest:

    def __init__(self, number_of_questions=10):

        self.question_array = []
        self.answer_matrix = [[0 for x in range(3)] for y in range(number_of_questions)]
        self.right_answers = []
        self.user_choice = [-1 for x in range(number_of_questions)]

        for i in range(number_of_questions):
            self.question_array.append(ExpressionExercise(complications=int(1 + i/6), variables=int(1+(i/4))))

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
        random_expression = Expression()

        for symbol in symbols:
            temp = Variable(number=random.randrange(1, 15, 2), symbols=symbol)
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



######################################################################################################
#####                   ###################################     #########            #################
#####                   #########           ############      ###########            #################
#########       ###############    ########    #######        ##############    ######################
#########       ##############                  ##########         #########    ######################
##########       #############      ##################           ###########    ######################
##########       ################          ##########    ###################    ######################
######################################################################################################
"""
eivar1 = Variable(number=3, symbols=["x", "y"])
eivar2 = Variable(number=-5)
eivar3 = Variable(number=-2, symbols=["x"])
eivar4 = Variable(number=4)
eivar5 = Variable()

f1 = Friction(numerator=eivar1, denominator=eivar2)
f2 = Friction(numerator=Variable(4), denominator=Variable(-3) )


bituy1.addVar(f2)
bituy1.addVar(eivar4)
bituy1.addVar(eivar3)
bituy1.addVar(f2)

ep = ExpressionProcess()

ep.complicate()
ep.complicate()
ep.complicate()

print ("e1: ", eivar1.toString(), "\ne2: ", eivar2.toString(), "\ne3: ", eivar3.toString(), "\ne4: ", eivar4.toString(), "\ne5: ", eivar5.toString())
print ("f1: ", f1.toString(), "\nf2: ", f2.toString())
print ("b1: ", bituy1.toString())
print (str(bituy1.findMeANumber()))
##print ("e3 empty: ", eivar3.isANumber(), "\ne4: ", eivar4.isANumber())


eivar1 = Variable(number=2, symbols=["x"])
eivar2 = Variable(number=1, symbols=["x"])
eivar3 = Variable(number=1)
print("e1: ", eivar1.toString(), "\ne2: ", eivar2.toString(),"\ne3: ", eivar3.toString())


eivar1 = Variable(number=3, symbols=["x", "y"])
eivar2 = Variable(number=-5)
eivar3 = Variable(number=-2, symbols=["x"])
eivar4 = Variable(number=4)
eivar5 = Variable()

bituy1 = Expression()
bituy1.addVar(eivar4)
bituy1.addVar(eivar3)
bituy1.addVar(eivar4)
print(bituy1.toString())
bituy1.removeVar(eivar3)
print(bituy1.toString())
"""
'''
eivar1 = Variable(number=3, symbols=["x", "y"])
eivar2 = Variable(number=-5)
eivar3 = Variable(number=-2, symbols=["x"])
eivar4 = Variable(number=4)
eivar5 = Variable()
eivar6 = Variable(number=3, symbols=["x"])

bituy1 = Expression(eivar1)
bituy1.add_var(eivar2)

ep = ExpressionProcess(solution=bituy1)
print(ep.to_string())
ep.complicate_step([], levels=5)
print(ep.to_string())
'''


##test = ExpressionAmericanTest()
'''
eivar1 = Variable(number=-2, symbols=["x"])
eivar2 = Variable(number=6, symbols=["y"])
eivar3 = Variable(number=-2)
bituy1 = Expression()
bituy1.add_var(eivar1)
bituy1.add_var(eivar2)
bituy1.add_var(eivar3)
print(bituy1.return_symbols())


test = AmericanTest()
print(test.test_to_string())
##print(test.solution_to_string())
print(str(test.calc_grade()))
'''
eivar1 = Variable(number=-2, symbols=["x"])
eivar2 = Variable(number=6, symbols=["y"])
eivar3 = Variable(number=-2)\

bituy1 = Expression()
bituy1.add_var(Variable(number=6, symbols=["xy"]))
bituy1.add_var(Variable(number=6, symbols=["xy"]))
bituy1.add_var(Variable(number=-2, symbols=["y", "x"]))
bituy1.add_var(Variable(number=-2, symbols=["y", "x"]))

bituy2 = Expression()
bituy2.add_var(Variable(number=6, symbols=["xy"]))
bituy2.add_var(Variable(number=6, symbols=["xy"]))
bituy2.add_var(Variable(number=-2, symbols=["y", "x"]))
bituy2.add_var(Variable(number=-2, symbols=["xx","y"]))

##print ( str( Variable(number=6, symbols=["y"]).get_symbol().index("y")))

##print(str(Variable(number=6, symbols=["x", "y"]).is_identical(Variable(number=6, symbols=["y", "yx"]))))

print ( str (bituy1.is_identical(bituy2)))