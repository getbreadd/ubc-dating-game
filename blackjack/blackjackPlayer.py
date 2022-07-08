class Player:
    def __init__(self, playerName, cards):
        self.playerName = playerName
        self.cards = cards

    def getPlayerHand(self):
        return self.cards