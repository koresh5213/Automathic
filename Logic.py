import copy
import random

def string_to_expression(string):
    final_expression = Expression()
    print (hex(id(final_expression.heart[0].symbols)))
    current_var = -1; current_number=0; current_symbols=""
    for current in string:
        if current is "+" or current is "-":
            if current_var is not -1:
                final_expression.add_var(current_var)

            current_symbols=""
            current_number=0
            current_var = Variable()
            current_var.sign = current

        if current.isdigit():
            if current_var is -1:
                current_var = Variable()
            current_number*= 10
            current_number+=int(current)
            current_var.number = current_number

        print (hex(id(current_var.symbols)))

        if current.isalpha():
            current_var.add_symbol(current)

        ##if not (current.isdigit() or current.isalpha()):
        ##    return -1

    if current_var is not -1:
        final_expression.add_var(current_var)

    return final_expression



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

        for symbol in var.get_symbol():
            try:
                self.symbols.index(symbol)
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

    def add_number(self, num): ##num is from type int
        a = self.number
        if self.sign is "-":
            a = a * -1

        sum = a + num

        self.number = abs(sum)
        if sum >= 0:
            self.sign = "+"
        else:
            self.sign = "-"

    def add_symbol(self, symbol):
        self.symbols.append(symbol)


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

    def to_string(self, first="yes"):
        text = ""
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
            if var.symbols == symbols and var.symbols not in list_of_vars:
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
    def __init__(self, diff=5):

        complications = int(diff / 6 + 1)
        variables = int(diff / 4 + 1)

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

    def get_solution(self):
        return self.pro.process[0]

    def create_a_random_answer(self, symbols):
        random_expression = Expression()

        for symbol in symbols:
            temp = Variable(number=random.randrange(1, 15, 2), symbols=symbol)
            random_expression.add_var(temp)

        return random_expression

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

    def var_add(self, add, side="a"): ##add is from type variable
        if side is "a":
            var = self.sideA.find_me_a_var_of(add.get_symbol())
            if var is -1:
                return
            var.add_number(add.to_number())
            self.sideB.add_var(add, random_location="yes")
        else:
            var = self.sideB.find_me_a_var_of(add.get_symbol())
            if var is -1:
                return
            self.sideA.add_var(add, random_location="yes")
            self.sideB.find_me_a_var_of(add.get_symbol()).add_number(add.to_number())

    def simple_add(self, add):
        self.sideA.add_var(add, random_location="yes")
        self.sideB.add_var(add, random_location="yes")

    def is_identical(self, other):
        if (self.sideA.is_identical(other.sideA) is 1) and (self.sideB.is_identical(other.sideB) is 1):
            return 1

        if (self.sideA.is_identical(other.sideB) is 1) and (self.sideB.is_identical(other.sideA) is 1):
            return 1

        return -1


    def find_me_a_symbol(self):
        return self.sideA.find_me_a_symbol()



class EquationProcess:
    def __init__(self, solution=Equation()):
        self.solution = solution
        self.process = [self.solution]

    def complicate_step(self, complications=1, method=1, side="a"):
        last = copy.deepcopy(self.process[-1])
        dup = last

        for i in range(complications):
            if method is 1: ##multiply both sections in the same number
                number = random.choice([2,3,5,7])
                dup.multiply(Variable(number = number))

            if method is 2: ##add variable
                symbol = self.solution.find_me_a_symbol()
                number = 0
                while number is 0:
                    number = random.randrange(-10,10)
                dup.var_add(Variable(number=number, symbols=symbol), side=side)

            if method is 3: ##simple addition
                number = 0
                while number is 0:
                    number = random.randrange(-10, 10)
                dup.simple_add(Variable(number=number))

            if method is 4:
                number = 0
                symbol = self.solution.find_me_a_symbol()
                while number is 0:
                    number = random.randrange(-10, 10)
                dup.simple_add(Variable(number=number, symbols=symbol))

        self.process.append(dup)

    def to_string(self):
        s= ""
        rev = self.process[::-1]
        for equation in rev:
            s+=equation.to_string(); s+=" \n"

        return s

    def eq_to_string(self):
        return self.process[-1].to_string()

    def get_symbols(self):
        symbols = []
        temp_a = self.solution.sideA.return_symbols()
        temp_b = self.solution.sideB.return_symbols()

        for symbol in temp_a+temp_b:
            if symbol not in symbols:
                symbols.append(symbol)

        symbols.remove([])

        return symbols

class EquationExercise:
    def __init__(self, diff=2):

        symbols = ["x", "x", "y", "z", "a", "b"]
        symbol = symbols[random.randrange(0, len(symbols))]

        temp_expression = Expression(heart=Variable(number=1, symbols=symbol))
        temp_expression2 = Expression(heart=Variable(number=random.randrange(-10, 10, 2)))

        self.solution = Equation(sideA=temp_expression, sideB=temp_expression2)

        self.pro = EquationProcess(solution=self.solution)
        self.pro.complicate_step(method=3, complications=1)
        self.pro.complicate_step(method=4, complications=1)
        self.pro.complicate_step(method=2, complications=1)
        ##self.pro.complicate_step(method=1, complications=1)

    def exercise_to_string(self):
        return self.pro.eq_to_string()

    def solution_to_string(self, full="no"):
        if full == "yes":
            return self.pro.to_string()

        return self.solution.to_string()

    def get_solution(self):
        return self.pro.solution

    def create_a_random_answer(self, symbols):
        side_a = Expression(heart=Variable(number=1, symbols=symbols))
        side_b = Expression(heart=Variable(number=random.randrange(-10,10)))

        answer = Equation(sideA=side_a, sideB=side_b)
        return answer

    def get_symbols(self):
        return self.pro.get_symbols()

def simple_pdf():
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Courier', 'B', 16)
    pdf.cell(40, 10, '1!',1,1)
    pdf.cell(40, 10, '2!',1,1)
    pdf.cell(40, 10, '3!',1,1)
    pdf.output('tuto5.pdf', 'F')

'''
ex  = EquationExercise()
##print(ex.pro.eq_to_string())
expr = Expression()
expr.add_var(Variable(number=2, symbols=["x","t"]))
expr.add_var(Variable(number=-1, symbols=[]))
print(expr.to_string())
print(expr.find_me_a_var_of([]).to_string())

ex1 = string_to_expression("2a-120x")
print(ex1.to_string())
ex2 = string_to_expression("-120+2323")
print(ex2.to_string())
print(str(ex1.is_identical(ex2)))

ee = EquationExercise()
print (ee.exercise_to_string())
print (ee.solution_to_string())


##tester
var1 = Variable(number=3)
var2 = Variable()
var3 = Variable(number=-13)
var4 = Variable(number=3, symbols=["n"])
var5 = Variable(number=3, symbols=["x", "y"])


ex = Expression()
ex.add_var(var1)
ex.add_var(var2)
ex.add_var(var3)
ex.add_var(var4)
ex.add_var(var5)

ex1 = Expression(var1)
ex2 = Expression(var4)
ex3 = Expression(var3)

eq1 = Equation(sideA=Expression(Variable(number=1, symbols=["x"])), sideB=ex1)
eq2 = Equation(sideA=ex2, sideB=ex3)

list = [var1, var2, var3, var4, var5, ex, ex1, ex2, ex3,  eq1, eq2]

s=""
for i in list:
    s+=i.to_string(); s+="\n"
print(s)
'''
