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
        return self.suit

    def getSuit(self):
        return self.suit;
    
    def printCard(self):
        if (self.number == 1):
            print('A' + self.suit)
        elif (self.number == 11):
            print('J' + self.suit)
        elif(self.number == 12):
            print('Q' + self.suit)
        elif(self.number == 13):
            print('K' + self.suit)
        else:
            print(self.number,self.suit);
