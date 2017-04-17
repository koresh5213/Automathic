import copy
import random


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
            return

        for my_variable in self.heart:
            if var.to_string() == my_variable.to_string():
                self.heart.remove(my_variable)
                break
        return

    def find_me_a_var_of(self, symbols):
        list_of_vars = []
        for var in self.heart:
            if symbols == var.symbols:
                list_of_vars.append(var)
        if symbols == -1:
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

    def complicate_step(self, method=0, levels=1):
        last = copy.deepcopy(self.process[-1])
        dup = last

        if method not in (1, 2):
            method = random.randint(1, 2)


        if method == 1:
            for i in range(levels):
                rand_number_from_expression = Variable(number=last.find_me_a_number())
                rand_number_to_subtract = random.randrange(1, 15, 2)
                number_to_add = rand_number_from_expression.to_number() - rand_number_to_subtract

                dup.remove_var(rand_number_from_expression)
                dup.add_var(Variable(number=rand_number_to_subtract), random_location="yes!")
                dup.add_var(Variable(number=number_to_add), random_location="yes!")

        if method == 2:
            for i in range(levels):
                rand_var_from_expression = last.find_me_a_random_var()
                while rand_var_from_expression == -1:
                    rand_var_from_expression = last.find_me_a_random_var()

                rand_number_to_subtract = random.randrange(1, 15, 2)
                rand_var_to_subtract = Variable(number=rand_number_to_subtract, symbols=rand_var_from_expression.symbols)

                number_to_add = rand_var_from_expression.to_number() - rand_number_to_subtract
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


class Exercise:
    def __init__(self, complications=2):
        rand_starting_var = random.randint(0, 10)
        rand_number_in_var = random.randint(0, 10)
        var1 = Variable(number=rand_starting_var, symbols=["x"])
        var2 = Variable(number=rand_number_in_var)

        exp = Expression(var1)
        exp.add_var(var2)

        self.pro = ExpressionProcess(solution=exp)
        for i in range(complications):
            self.pro.complicate()

    def exercise_to_string(self):
        return self.pro.get_latest().to_string()

    def solution_to_string(self):
        return self.pro.to_string()



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
ep.complicate_step(method=2, levels=5)
print(ep.to_string())
print(bituy1.find_me_a_var_of([]).to_string())


