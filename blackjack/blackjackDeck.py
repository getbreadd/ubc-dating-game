import random
from blackjackCard import *

SUITS = ['S', 'H', 'C', 'D']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Deck:
    def __init__(self):
        self.cards = []
        self.makeNewDeck()
        
    def makeNewDeck(self):
        for i in SUITS:
            for j in VALUES:
                card = Card(i, j);
                self.cards.append(card);
        # self.shuffle();
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def printCards(self):
        for card in self.cards:
            card.printCard();