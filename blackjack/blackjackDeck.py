import random
from blackjackCard import *

SUITS = ['S', 'H', 'C', 'D']
RANKS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

class Deck:
    def __init__(self):
        self.cards = []
        self.makeNewDeck()
        
    def makeNewDeck(self):
        for i in SUITS:
            for j in RANKS:
                card = Card(i, j);
                self.cards.append(card);
        self.shuffle();
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def printCards(self):
        for card in self.cards:
            card.printCard();
            
    def drawCard(self):
        currLength = len(self.cards)
        if (currLength == 0):
            self.makeNewDeck()
            print("Out of cards! Shuffling...")
        toDraw = random.randint(0, currLength - 1)
        cardDrawn = self.cards[toDraw]
        self.cards.pop(toDraw)
        return cardDrawn
        