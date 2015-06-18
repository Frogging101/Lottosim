class Match:
    def __init__(self):
        self.matches = 0            #Number of matches
        self.bonusMatched = False   #Whether or not the bonus number was matched

class WinningNumbers:
    def __init__(self):
        self.numbers = set()    #Set of winning numbers
        self.bonus = None       #Bonus number
