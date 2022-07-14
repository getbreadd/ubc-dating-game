from blackjackCard import *
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.bankroll = 0

    def getName(self):
        return self.name

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
    
    def getBankrollAmount(self):
        return self.bankroll
    
    def updateBankroll(self, amount):
        self.bankroll += amount
    
    def hasBlackjack(self):
        return ((len(self.cards) == 2) & (self.getTotal() == 21))

    def isBusted(self):
        return self.getTotal() > 21
    
    def printCards(self):
        print(self.name + ": ", end = '')
        print("[", end = '')
        for card in self.cards:
            card.printCard()
        print("]")