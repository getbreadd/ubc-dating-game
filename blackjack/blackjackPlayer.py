from blackjackCard import *
class Player:
    def __init__(self, playerName):
        self.playerName = playerName
        self.cards = []

    def getPlayerHand(self):
        return self.cards
    
    def addCard(self, card):
        self.cards.append(card)
        
    def getNumCards(self):
        return len(self.cards)
    
    def getTotal(self):
        sum = 0
        for card in self.cards:
            sum += card.getValue()
        numAce = self.getNumAce()
        while (sum > 21 and numAce > 0):
            sum -= 10
            numAce -= 1
        return sum 
        
    def getNumAce(self):
        numAce = 0
        for x in self.cards:
            if x.getValue == 1:
                numAce += 1
        return numAce
    
    def printCards(self):
        print("Your cards: ", end = '')
        print("[", end = '')
        for card in self.cards:
            card.printCard()
        print("]")