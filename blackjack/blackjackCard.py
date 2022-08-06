RANKS = [0, "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def returnCard(self):
        return self;
    
    def deleteCard(self):
        del self;
        
    def getValue(self):
        value = self.rank
        if (value > 10):
            value = 10
        elif (value == 1):
            value = 11
        return value
    
    def getSuit(self):
        return self.suit

    def getCardImage(self):
        return "blackjack/Images/cards/" + str(RANKS[self.rank]) + self.suit + ".jpg"
    
    def printCard(self):
        print(str(RANKS[self.rank]) + self.suit, end = ", ")
