class Card:
    def __init__(self, suit, number):
        self.suit = suit;
        self.number = number;
        
    def returnCard(self):
        return self;
    
    def deleteCard(self):
        del self;
        
    def getValue(self):
        return self.number;

    def getSuit(self):
        return self.suit;
    
    def printCard(self):
        print(self.number + self.suit);
