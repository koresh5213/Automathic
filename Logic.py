import copy

class Variable:
    def __init__(self, number=1, symbols=[]):

        self.number = abs(number)
        self.symbols = symbols

        if(number>=0):
            self.sign = "+"
        else:
            self.sign = "-"

        return

    def toString(self, firstInLine="no"):

        text= ""

        if not(firstInLine=="yes" and self.sign=="+"):
            text += self.sign

        text += str(self.number)
        for i in self.symbols:
            text = text + i

        return text


class Expression:

    def __init__(self, heart=Variable(number=1)):
        self.heart = [heart]
        return

    def addVar(self, var):
        if type(var) == Variable or type(var)==Friction:
            self.heart.append(var)
        return

    def toString(self):
        text=""
        first = "yes"
        for e in self.heart:
            if first == "yes" and type(e)==Variable:
                text += e.toString(firstInLine="yes")
                first = "no :["
            else:
                if(type(e)==Friction):
                    text+= " + "
                text += e.toString()
                text += " "
        return text


class Friction:

    def __init__(self, numerator=Variable(), denominator=Variable()): ##num= mone, denom= mehane

        self.numerator = numerator

        if denominator.number==0 and denominator.symbols==[]: denominator=1  ##divided by zero
        self.denominator = denominator

        return

    def toString(self):
        text = "<"
        text+= self.numerator.toString(firstInLine="yes")
        text+= " / "
        text+= self.denominator.toString(firstInLine="yes")
        text+= ">"
        return text

class ExpressionProcess:

    def __init__(self, solution=Expression()):
        self.solution = solution
        self.process = [self.solution]

    def complicate(self):
        last = copy.deepcopy(self.process[-1])
        dup = last

        method = 1

        if method==1:
            dup.addVar(Variable(number=11, symbols=["x"]))

        self.process.append(dup)

    def toString(self):
        text=""
        for e in self.process:
            text += e.toString()
            text += "\n"
        return text[:-1]

######################################################################################################
#####                   ###################################     #########            #################
#####                   #########           ############      ###########            #################
#########       ###############    ########    #######        ##############    ######################
#########       ##############                  ##########         #########    ######################
##########       #############      ##################           ###########    ######################
##########       ################          ##########    ###################    ######################
######################################################################################################

eivar1 = Variable(number=3, symbols=["x", "y"])
eivar2 = Variable(number=-5)
eivar3 = Variable(number=-2, symbols=["x"])
eivar4 = Variable(number=3)
e2 = Expression(eivar3)
e2.addVar(eivar4)
'''

e.addVar(eivar2)

print(e.toString())
'''

f1 = Friction(numerator=eivar1, denominator=eivar2)
e = Expression([Variable(number=-12, symbols=["x"])])
e.addVar(f1)
e.addVar(eivar2)
e.addVar(f1)
e.addVar(eivar1)
e.addVar(f1)
e.addVar(eivar1)
ep = ExpressionProcess(solution=e2)

ep.complicate()
ep.complicate()
ep.complicate()

print(ep.toString())