import copy
import random

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

    def multiply(self, mul): ##mul is also from type expression
        if self.sign == mul.sign:
            self.sign = "+"
        else:
            self.sign = "-"

        self.number = self.number * mul.number

        self.symbols = list(set(self.symbols).union(mul.symbols))



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

######################################################################

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

    def multiply(self, mul): ##mul is type Variable
        for current in self.heart:
            current.multiply(mul)


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

    def solution_to_string(self, full="no"):

        if (full=="yes"):
            return self.pro.to_string()

        return self.pro.solution_to_sting()

    def get_symbols(self):
        return self.pro.get_symbols()

##############################################################################

class Equation:
    def __init__(self, sideA= Expression, sideB=Expression):
        self.sideA = sideA
        self.sideB = sideB

    def to_string(self):
        s=""
        s+=self.sideA.to_string()
        s+=" = "
        s+=self.sideB.to_string()
        return s

    def multiply(self, mul): ##mul is from type variable
        self.sideA.multiply(mul)
        self.sideB.multiply(mul)


class EquationProcess:
    def __init__(self, solution=Equation()):
        self.solution = solution
        self.process = [self.solution]

    def complicate_step(self):
        last = copy.deepcopy(self.process[-1])
        dup = last

        dup.multiply(lg.Variable(number = 4))

        self.process.append(dup)

    def to_string(self):
        s= ""
        rev = self.process[::-1]
        for equation in rev:
            s+=equation.to_string(); s+=" \n"

        return s

class EquationExercise:
    def __init__(self, complications=2):

        temp_expression = lg.Expression(heart=lg.Variable(number=1, symbols=["x"]))
        temp_expression2 = lg.Expression(heart=lg.Variable(number=random.randrange(-10, 10, 2)))

        self.solution = Equation(sideA=temp_expression, sideB=temp_expression2)

        self.pro = EquationProcess(solution=self.solution)
        self.pro.complicate_step()

    def solution_to_string(self, full="no"):
        if full == "yes":
            return self.pro.to_string()

        return self.solution.to_string()
