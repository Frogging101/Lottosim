import random
import re

low = 1
high = 49
numChoices = 6
plays = 1000

def genNumbers():
    return [random.randrange(low,high+1) for x in range(numChoices)]

def compareNumbers(choices, winners):
    matches = 0
    for choice in choices:
        for winner in winners:
            if choice == winner:
                matches += 1
    return matches

random.seed()

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

while True:
    strNumChoices = raw_input("How many numbers should be chosen? [6]: ")
    if strNumChoices:
        try:
            numChoices = int(strNumChoices)
        except(ValueError):
            print "Invalid input"
            continue
    break

while True:
    strPlays = raw_input("How many plays should be run? [1000]: ")
    if strPlays:
        try:
            plays = int(strPlays) 
        except(ValueError):
            print "Invalid input"
            continue
    break

testNumbers = genNumbers()
winningNumbers = genNumbers()

allMatches = [0] * (numChoices+1)

for play in range(plays):
    numMatches = compareNumbers(testNumbers, winningNumbers)
    allMatches[numMatches] += 1
    winningNumbers = genNumbers()

for i,matches in enumerate(allMatches):
    print str(i) + " matched: " + str(matches)

