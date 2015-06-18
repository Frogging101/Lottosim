import random
import re
from LottoObjects import *

low = 1
high = 49
numChoices = 6
plays = 1000
useBonusNumber = True

def genNumbers(exclude=set()):
    numbers = set()
    wn = WinningNumbers()

    while True:
        while len(numbers) < numChoices:
            randNum = random.randrange(low,high+1)
            numbers.add(randNum)
        if hash(frozenset(numbers)) not in exclude:
            break
        else:
            #print str(numbers)+" excluded!"
            numbers = set()
    if useBonusNumber:
        while True:
            randNum = random.randrange(low,high+1)
            if randNum not in numbers:
                wn.bonus = randNum
                break

    wn.numbers = numbers
    return wn

def genChoices(exclude=set()):
    choices = genNumbers(exclude).numbers
    return choices

def compareNumbers(choices, winners):
    matches = 0
    match = Match()
    for choice in choices:
        if choice in winners.numbers:
            matches += 1

    match.matches = matches

    if useBonusNumber and winners.bonus:
        if winners.bonus in choices:
            match.bonusMatched = True
        else:
            match.bonusMatched = False
    return match

def getUserInt(question, default):
    while True:
        strInt = raw_input(question)
        if strInt:
            try:
                myInt = int(strInt)
            except ValueError:
                print "Invalid input. Please enter a number"
                continue
        else:
            myInt = default
        break
    return myInt

def getUserYN(question, default):
    while True:
        strYN = raw_input(question)
        if strYN:
            if strYN.startswith('y'):
                return True
            elif strYN.startswith('n'):
                return False
            else:
                print "Enter yes or no"
                continue
        else:
            return default

def setOptions():
    global numChoices, useBonusNumber, high, low
    reNumRange = re.compile(r"(?P<low>[0-9]+)-(?P<high>[0-9]+)")
    while True:
        strNumRange = raw_input("What is the range of numbers to choose from? [1-49]: ")
        if strNumRange:
            match = reNumRange.match(strNumRange)
            if match:
                high = int(match.group('high'))
                low = int(match.group('low'))
            else:
                print "Invalid input. Format is '[low]-[high]'"
                continue
        break

    numChoices = getUserInt("How many numbers should be chosen? [6]: ", 6)
    useBonusNumber = getUserYN("Generate a bonus number? [True]: ", True)

class Menu:
    #TODO: Fix this numbering thing
    SIMPLAYS = ("Simulate plays", 0)
    PUNTILWIN = ("Play until win", 1)
    MULTIDRAW = ("Draw until win", 2)
    OPTIONS = ("Modify options", 3)
    NEWSEED = ("New random seed", 4)
    QUIT = ("Quit", 5)

    options = [SIMPLAYS,\
                PUNTILWIN,\
                MULTIDRAW,\
                OPTIONS,\
                NEWSEED,\
                QUIT]

    @staticmethod
    def numToOption(num):
        for option in Menu.options:
            if option[1] == num:
                return option

    @staticmethod
    def menu():
        print '\n',
        for option in Menu.options:
            print str(option[1]) + ": " + option[0]
        print '\n',
        while True:
            optionNum = getUserInt("Choose an option: ", None)
            if Menu.numToOption(optionNum):
                return Menu.numToOption(optionNum)
            else:
                continue


random.seed()

done = False

setOptions()
while not done:
    alreadyPlayed = None
    selection = Menu.menu()
    if selection == Menu.SIMPLAYS:
        plays = 1000
        again = True
        winningNumbers = genNumbers()
        while again:
            alreadyPlayed = set()
            print "\nWinning numbers: "+str(winningNumbers.numbers)
            if useBonusNumber:
                print "Bonus: "+str(winningNumbers.bonus)
            plays = getUserInt("How many plays should be run? ["+str(plays)+"]: ", plays)

            print '\n',

            allMatches = [[0,0] for x in range(numChoices+2)]

            for play in range(plays):
                testNumbers = genChoices(alreadyPlayed)
                match = compareNumbers(testNumbers, winningNumbers)
                alreadyPlayed.add(hash(frozenset(testNumbers)))
                allMatches[match.matches][0] += 1
                allMatches[match.matches][1] += int(match.bonusMatched)

            for i,matches in enumerate(allMatches):
                print str(i) + " matched: " + str(allMatches[i][0]),
                if useBonusNumber:
                    print ', '+str(allMatches[i][1])+" with bonus"
            print '\n',
            again = getUserYN("Run again? (y/n): ", True)

    elif selection == Menu.PUNTILWIN:
        numToWin = 6
        bonusRequired = False
        again = True
        while again:
            alreadyPlayed = set()
            winningNumbers = genNumbers()
            plays = 0
            print "\nWinning numbers: "+str(winningNumbers.numbers)
            if useBonusNumber:
                print "Bonus number: "+str(winningNumbers.bonus)
            numToWin = getUserInt("How many numbers are required to win? ["+str(numToWin)+"]: ", numToWin)
            if useBonusNumber:
                bonusRequired = getUserYN("Bonus required to win? ["+str(bonusRequired)+"]: ", bonusRequired)
            valid = True
            if numToWin == 0:
                print "\nYou win by default"
                valid = False
            elif numToWin+int(bonusRequired) > numChoices:
                print "\nYou're never going to win this"
                valid = False

            if valid:
                win = False
                while not win:
                    testNumbers = genChoices(alreadyPlayed)
                    match = compareNumbers(testNumbers, winningNumbers)
                    alreadyPlayed.add(hash(frozenset(testNumbers)))
                    plays += 1
                    if plays % 1000000 == 0:
                        print str(plays) + " plays performed"
                    if match.matches >= numToWin:
                        win = True
                    if bonusRequired and not match.bonusMatched and match.matches < numToWin+1:
                        win = False
                    if win:
                        print "\nYou won by matching "+str(match.matches)+" numbers after "+str(plays)+" plays"
                        print "Your numbers were "+str(testNumbers)
            again = getUserYN("Run again? (y/n): ", True)

    elif selection == Menu.MULTIDRAW:
        numToWin = 6
        again = True
        plays = 10
        bonusRequired = False
        while again:
            draws = 0
            numToWin = getUserInt("\nHow many numbers are required to win? ["+str(numToWin)+"]: ", numToWin)
            if useBonusNumber:
                bonusRequired = getUserYN("Bonus required to win? (y/n) ["+str(bonusRequired)+"]: ", bonusRequired)
            plays = getUserInt("How many plays will you do per draw? ["+str(plays)+"]: ", plays)
            valid = True
            if numToWin == 0:
                print "\nYou win by default"
                valid = False
            elif numToWin+int(bonusRequired) > numChoices:
                print "\nYou're never going to win this"
                valid = False

            if valid:
                win = False
                while not win:
                    winningNumbers = genNumbers()
                    alreadyPlayed = set()
                    draws += 1

                    if draws % 1000000 == 0:
                        print str(draws) + " draws performed"

                    for x in range(plays):
                        testNumbers = genChoices(alreadyPlayed)
                        match = compareNumbers(testNumbers, winningNumbers)
                        alreadyPlayed.add(frozenset(testNumbers))
                        if match.matches >= numToWin:
                            win = True
                        if bonusRequired and not match.bonusMatched and match.matches < numToWin+1:
                            win = False
                        if win:
                            print "\nYou won by matching "+str(match.matches)+" numbers after "+str(draws)+" draws"
                            print "Your numbers were "+str(testNumbers)+" and the winning numbers were "+str(winningNumbers.numbers)
                            if useBonusNumber:
                                print "The bonuns number was "+str(winningNumbers.bonus)
                            break

            again = getUserYN("Run again? (y/n): ", True)


    elif selection == Menu.OPTIONS:
        setOptions()

    elif selection == Menu.NEWSEED:
        random.seed()
 
    elif selection == Menu.QUIT:
        break
