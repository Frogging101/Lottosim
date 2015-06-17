import random
import re

low = 1
high = 49
numChoices = 6
plays = 1000

def genNumbers():
    numbers = []
    while len(numbers) < numChoices:
        randNum = random.randrange(low,high+1)
        if randNum not in numbers:
            numbers.append(randNum)
    return numbers

def compareNumbers(choices, winners):
    matches = 0
    for choice in choices:
        for winner in winners:
            if choice == winner:
                matches += 1
    return matches

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
    selection = Menu.menu()
    if selection == Menu.SIMPLAYS:
        plays = 1000
        again = True
        winningNumbers = genNumbers()
        while again:
            print "\nWinning numbers: "+str(winningNumbers)
            plays = getUserInt("How many plays should be run? ["+str(plays)+"]: ", plays)

            print '\n',
            testNumbers = genNumbers()

            allMatches = [0] * (numChoices+1)

            for play in range(plays):
                numMatches = compareNumbers(testNumbers, winningNumbers)
                allMatches[numMatches] += 1
                testNumbers = genNumbers()

            for i,matches in enumerate(allMatches):
                print str(i) + " matched: " + str(matches)

            again = getUserYN("Run again? (y/n): ", True)

    elif selection == Menu.PUNTILWIN:
        numToWin = 6
        again = True
        while again:
            winningNumbers = genNumbers()
            plays = 0
            print "\nWinning numbers: "+str(winningNumbers)
            numToWin = getUserInt("How many numbers are required to win? ["+str(numToWin)+"]: ", numToWin)
            valid = True
            if numToWin == 0:
                print "\nYou win by default"
                valid = False
            elif numToWin > numChoices:
                print "\nYou're never going to win this"
                valid = False

            if valid:
                win = False
                while not win:
                    testNumbers = genNumbers()
                    numMatches = compareNumbers(testNumbers, winningNumbers)
                    plays += 1
                    if plays % 1000000 == 0:
                        print str(plays) + " plays performed"
                    if numMatches >= numToWin:
                        print "\nYou won by matching "+str(numMatches)+" numbers after "+str(plays)+" plays"
                        print "Your numbers were "+str(testNumbers)
                        win = True
            again = getUserYN("Run again? (y/n): ", True)

    elif selection == Menu.MULTIDRAW:
        numToWin = 6
        again = True
        plays = 10
        while again:
            draws = 0
            numToWin = getUserInt("\nHow many numbers are required to win? ["+str(numToWin)+"]: ", numToWin)
            plays = getUserInt("How many plays will you do per draw? ["+str(plays)+"]: ", plays)
            valid = True
            if numToWin == 0:
                print "\nYou win by default"
                valid = False
            elif numToWin > numChoices:
                print "\nYou're never going to win this"
                valid = False

            if valid:
                win = False
                while not win:
                    winningNumbers = genNumbers()
                    draws += 1

                    if draws % 1000000 == 0:
                        print str(draws) + " draws performed"

                    for x in range(plays):
                        testNumbers = genNumbers()
                        numMatches = compareNumbers(testNumbers, winningNumbers)
                        if numMatches >= numToWin:
                            print "\nYou won by matching "+str(numMatches)+" numbers after "+str(draws)+" draws"
                            print "Your numbers were "+str(testNumbers)+" and the winning numbers were "+str(winningNumbers)
                            win = True

            again = getUserYN("Run again? (y/n): ", True)


    elif selection == Menu.OPTIONS:
        setOptions()

    elif selection == Menu.NEWSEED:
        random.seed()
 
    elif selection == Menu.QUIT:
        break
