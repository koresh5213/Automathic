import copy
import random

class Variable:
    def __init__(self, number=1, symbols=[]):
        if (type(number) == type(3)):
            self.number = abs(number)
        else:
            self.number = 1
        self.symbols = symbols

        if(number>=0):
            self.sign = "+"
        else:
            self.sign = "-"

        return

    def toString(self, firstInLine="no"):
        text = ""

        if not(firstInLine=="yes" and self.sign=="+"):
            text += self.sign

        if not ((self.number is 1) and (len(self.symbols) is not 0)):
            text += str(self.number)

        for i in self.symbols:
            text = text + i

        return text

    def isANumber(self):
        return not self.symbols

    def toNumber(self):
        number = self.number
        if(self.sign is "-"):
            number *=-1

        return number


class Expression:

    def __init__(self, heart=Variable(number=0)):
        self.heart = [heart]
        return

    def addVar(self, var, israndom="no"):
        if not( type(var) == Variable or type(var) == Friction ):
            return

        if(self.toString() == "0"):
            self.heart.pop(0)

        if(random=="no"):
            self.heart.append(var)
            return

        if(len(self.heart) == 0):
            position = 0
        else: position = random.randrange(0,len(self.heart))
        self.heart.insert(position, var)
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

    def findMeAFriction(self):
        frictions = [];
        for eivar in self.heart:
            if type(eivar) == Friction :
                frictions.append(eivar)

        if len(frictions) is 0 :
            return -1;

        return random.choice(frictions)

    def findMeANumber(self):
        numbers = [];
        for eivar in self.heart:
            if type(eivar) == Variable:
                if(eivar.isANumber()):
                    numbers.append(eivar.toNumber())

        if len(numbers) is 0:
            return -1;

        return random.choice(numbers)

    def removeVar(self, var):
        if not (type(var) is Variable or Friction):
            return

        for eivar in self.heart:
            if eivar.toString() == var.toString():
                self.heart.remove(eivar)
                break
        return

    def findMeaVarof(self, symbols):
        listofvars=[]
        for eivar in self.heart:
            if (symbols == eivar.symbols):
                listofvars.append(eivar)

        return random.choice(listofvars)

    def findMeaSymbol(self):
        varlist = []
        for eivar in self.heart:
            if not (eivar.isANumber()):
                varlist.append(eivar)

        if(len(varlist) == 0):
            return -1

        randvar = random.choice(varlist)
        return randvar.symbols

    def findMeARandomVar(self): return self.findMeaVarof(self.findMeaSymbol())


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

    def complicate(self, method=0):
        last = copy.deepcopy(self.process[-1])
        dup = last

        if method not in (1,2):
            method = random.randint(1,2)

        if method == 1:
            randnumberfromexpression = Variable(number=last.findMeANumber())
            randnumbertosubtract = random.randrange(1, 15, 2)
            numbertoadd = randnumberfromexpression.toNumber() - randnumbertosubtract

            dup.removeVar(randnumberfromexpression)
            dup.addVar(Variable(number=randnumbertosubtract), israndom="yes!")
            dup.addVar(Variable(number=numbertoadd), israndom="yes!")

        if method == 2:
            randvarfromexpression = last.findMeARandomVar()

            randnumbertosubtract = random.randrange(1, 15, 2)
            randvartosubtract = Variable(number=randnumbertosubtract, symbols=randvarfromexpression.symbols)

            numbertoadd = randvarfromexpression.toNumber() - randnumbertosubtract
            vartoadd = Variable(number=numbertoadd, symbols=randvarfromexpression.symbols)

            dup.removeVar(randvarfromexpression)
            dup.addVar(randvartosubtract, israndom="yes!")
            dup.addVar(vartoadd, israndom="yes!")

        self.process.append(dup)

    def toString(self):
        text=""
        rev = self.process[::-1]
        for e in rev:
            text += e.toString()
            text += "\n"
        return text[:-1]

    def getlatest(self):
        return self.process[-1]

class Exersice:
    def __init__(self, complications=2):
        randstartingvar = random.randint(0,10)
        randnumbertingvar = random.randint(0, 10)
        var1 = Variable(number= randstartingvar, symbols=["x"])
        var2 = Variable(number=randnumbertingvar)

        exp = Expression(var1)
        exp.addVar(var2)

        self.pro = ExpressionProcess(solution=exp)
        for i in range(complications):
            self.pro.complicate()

    def exstr(self):
        return self.pro.getlatest().toString()

    def soltionstr(self):
        return self.pro.toString()



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
bituy1.addVar(eivar2)

ep = ExpressionProcess(solution=bituy1)
print(ep.toString())
ep.complicate()
ep.complicate(method=1)
ep.complicate(method=3)
print(ep.toString())
'''

