import pygame
from blackjackPlayer import *
from blackjackDeck import *

pygame.init()

# ------------------------------- CONSTANTS -------------------------------

WIDTH = 850
HEIGHT = 650
USER_WIDTH = WIDTH * (2/3)
USER_HEIGHT = HEIGHT // 4
DEALER_CARD_COORDS = ((WIDTH // 2) - (USER_WIDTH // 2), HEIGHT * 0.25)
USER_CARD_COORDS = ((WIDTH // 2) - (USER_WIDTH // 2), HEIGHT * 0.60)
USER_BUTTONS_Y = USER_CARD_COORDS[1] + USER_HEIGHT
CARD_HEIGHT = pygame.image.load("blackjack/Images/cards/2C.jpg").get_height()
CARD_WIDTH = pygame.image.load("blackjack/Images/cards/2C.jpg").get_width()

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)
RED = pygame.Color("red")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")
STEEL_BLUE = (35, 90, 225)

FONT = pygame.font.Font('freesansbold.ttf', 32)
BACKGROUND_COLOUR = GREEN
CARD_SPACE = 3
CARD_WIDTH = 75

USER_TURN_MSG = "It's your turn! Hit or Stand?"
USER_BJ = "BLACKJACK!! Dealer's turn..."
USER_STANDS = "You stand. Dealer's turn..."
USER_BUSTED = "YOU'RE BUSTED! Dealer's turn..."
DEALER_BUSTED = "Dealer busts!"
DEALER_BJ = "Dealer has BLACKJACK!"
DEALER_STANDS = "Dealer stands"

# ======================================================================================
# ------------------------------- CREATE BLACKJACK CLASS -------------------------------
# ======================================================================================

class BlackJackGame:
    def __init__(self, running):
        self.running = running

        # init ui and stats
        self.initGameStats()
        self.initPygameScreen()
        self.createButtons()
        self.initAreas()

        self.initHands()

        # Run BlackJack
        self.runGame()
    
    # ------------------------------- INITIALIZE GAME STATS -------------------------------

    def initGameStats(self):
        self.deck = Deck()
        self.user = Player('User')
        self.dealer = Player('Dealer')

        self.playerTurn = self.user
        self.betAmount = 0  # FOR BET !!!
        self.winner = None

        self.initMessage = "LET'S GIVE AWAY ALL YOUR MONEYYYYY ^ - ^"
        self.announcer = FONT.render(self.initMessage, True, RED, None)
        self.announcerRect = self.announcer.get_rect()
        self.announcerRect.center = (WIDTH // 2, HEIGHT // 10)
        self.smallFont = pygame.font.Font('freesansbold.ttf', 28)
        self.cardTotalFont = pygame.font.Font('freesansbold.ttf', 18)

        self.startDealerTurn = False

        self.gameEnd = False

        self.displayEndScreen = False
        self.displayStartScreen = True
        self.displayGameScreen = False
        self.endBlackJackScreen = False

        self.dealerContButtonDisplayed = False
        self.winnerContButtonDisplayed = False
        self.pause = False

        self.curMsg = ""
        self.userTurnMsg = "userTurn"
        self.userBJMsg = "userBJ"
        self.userBustedMsg = "userBusted"
        self.userStandMsg = "userStands"
        self.dealerBJMsg = "dealerBJ"
        self.dealerBustedMsg = "dealerBusted"
        self.dealerStandsMsg = "dealerStands"

        self.msgList = {
            self.userTurnMsg: USER_TURN_MSG,
            self.userBJMsg: USER_BJ,
            self.userBustedMsg: USER_BUSTED,
            self.userStandMsg: USER_STANDS,
            self.dealerBJMsg: DEALER_BJ,
            self.dealerBustedMsg: DEALER_BUSTED,
            self.dealerStandsMsg: DEALER_STANDS,
        }
    
    # ------------------------------- INITIALIZE PYGAME SCREEN -------------------------------
    
    def initPygameScreen(self):
        # initialize screen and display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND_COLOUR)
        pygame.display.set_caption("It's time to gamble!")
        pygame.display.flip()
    
    # ------------------------------- CREATE BUTTONS -------------------------------
    
    def createButtons(self):
        self.userButtonWidth = WIDTH * 0.14
        self.hitText = "HIT"
        self.standText = "STAND"

        self.hitButton = self.createTextButton(self.hitText, BLACK, STEEL_BLUE, self.userButtonWidth)
        self.standButton = self.createTextButton(self.standText, BLACK, STEEL_BLUE, self.userButtonWidth)

        self.hitButtonPos = ((WIDTH // 2) - self.hitButton.get_width() - CARD_SPACE, USER_BUTTONS_Y)
        self.standButtonPos = ((WIDTH // 2) + CARD_SPACE, USER_BUTTONS_Y)

        self.seeDealersTurnText = "Click to see dealer's turn"
        self.seeDealersTurnButton = self.createTextButton(self.seeDealersTurnText, BLACK, STEEL_BLUE, self.getStringWidth(self.seeDealersTurnText))
        self.seeDealersTurnButtonPos = ((WIDTH // 2) - (self.seeDealersTurnButton.get_width() // 2), HEIGHT * 0.85)

        self.seeWinnerText = "Click to see Winner!"
        self.seeWinnerButton = self.createTextButton(self.seeWinnerText, BLACK, STEEL_BLUE, self.getStringWidth(self.seeWinnerText))
        self.seeWinnerButtonPos = ((WIDTH // 2) - (self.seeWinnerButton.get_width() // 2), HEIGHT * 0.85)

        self.helpButton = self.createTextButton("?", BLACK, BLUE, WIDTH * 0.05)
        self.helpButtonPos = (WIDTH - self.helpButton.get_width(), HEIGHT - self.helpButton.get_height())
    
    # ------------------------------- INITIALIZE AREAS -------------------------------

    def initAreas(self):
        self.announcerArea = None
        self.userCardArea = None
        self.dealerCarArea = None

    # =======================================================================================
    # HELPER METHODS
    # =======================================================================================

    # ------------------------------- OTHER UI HELPER METHODS -------------------------------

    # Change Announcer message
    def announceText(self, msg, msgColour, bckgdColour):
        self.announcer = FONT.render(msg, True, msgColour, bckgdColour)
        self.announcerRect = self.announcer.get_rect()
        self.announcerRect.center = (WIDTH // 2, HEIGHT // 10)
        self.screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, 0, WIDTH, (DEALER_CARD_COORDS[1] - self.smallFont.get_height() - 10)))
        self.announcerArea.blit(self.announcer, (0, 0))
        self.screen.blit(self.announcerArea, self.announcerRect)
        pygame.display.update()

    def createTextButton(self, msg, msgColour, bckgdColour, width):
        text = FONT.render(msg, True, msgColour, None)
        buttonSurface = pygame.surface.Surface((width, text.get_height()))
        buttonSurface.fill(bckgdColour)
        buttonSurface.blit(text, ((buttonSurface.get_width() // 2) - (text.get_width() // 2), (buttonSurface.get_height() // 2) - (text.get_height() // 2)))
        return buttonSurface

    def buttonClicked(self):
        text = FONT.render("CLICKED", True, BLACK, None)
        buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
        buttonSurface.fill(RED)
        buttonSurface.blit(text, (0, 0))
        return buttonSurface

    def getStringWidth(self, str):
        text = FONT.render(str, True, BLACK, None)
        width = text.get_width()
        return width

    def displayContinueButton(self, button, buttonPos):
        self.screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, self.hitButtonPos[1], WIDTH, self.hitButton.get_height()))
        self.screen.blit(button, buttonPos)

    def displayPlayerLabel(self, label, initY):
        cardText = self.smallFont.render(label, True, BLACK, None)
        cardTextArea = cardText.get_rect()
        self.screen.blit(cardText, ((WIDTH // 2) - (cardTextArea.width // 2), (initY[1] - cardTextArea.height - 10)))

    def displayTotalLabel(self, label, initY):
        totalText = self.smallFont.render(label, True, BLACK, None)
        totalTextArea = totalText.get_rect()
        self.screen.blit(totalText, ((WIDTH // 2) - (totalTextArea.width // 2), (initY[1] + CARD_HEIGHT + 10)))

    def addButtons(self):
        if (self.playerTurn == self.user):
            self.screen.blit(self.hitButton, self.hitButtonPos)
            self.screen.blit(self.standButton, self.standButtonPos)
        
        if (self.dealerContButtonDisplayed and not self.gameEnd):
            self.displayContinueButton(self.seeDealersTurnButton, self.seeDealersTurnButtonPos)
        if (self.winnerContButtonDisplayed):
            self.displayContinueButton(self.seeWinnerButton, self.seeWinnerButtonPos)
            
        # Add Help Button
        self.screen.blit(self.helpButton, self.helpButtonPos)

    def displayMainGame(self):
        self.displayUserCards() 
        self.displayDealerCards()

        self.displayPlayerLabel("Dealer's Cards", DEALER_CARD_COORDS)
        self.displayPlayerLabel("Your Cards", USER_CARD_COORDS)
                
        # Position the "Dealer Total" and "Your total" text
        if (self.playerTurn == self.dealer):
            dealerTotalText = "Total: " + str(self.dealer.getTotal())
        else:
            dealerTotalText = "Total: ?"
        self.displayTotalLabel(dealerTotalText, DEALER_CARD_COORDS)
        self.displayTotalLabel("Total: " + str(self.user.getTotal()), USER_CARD_COORDS)
        pygame.display.update()
        
        # user turn
        if (self.user.hasBlackjack() and self.playerTurn == self.user):
            self.announceText(self.msgList.get(self.userBJMsg), RED, None)
            self.curMsg = self.userBJMsg
            self.playerTurn = self.dealer
            self.startDealerTurn = True
            self.displayContinueButton(self.seeDealersTurnButton, self.seeDealersTurnButtonPos)
            self.dealerContButtonDisplayed = True
        
        # Add Button
        self.addButtons()

        # Set Announcer
        curAnnouncedMsg = self.determinAnnouncerState()
        self.displayAnnouncer(curAnnouncedMsg)
            
    def displayLongText(self, msg):
        words = [word.split(' ') for word in msg.splitlines()]
        space = FONT.size(' ')[0]
        wordsWidth = USER_WIDTH + (USER_WIDTH // 4)
        wordsHeight = HEIGHT// 3
        pos = ((WIDTH // 2) - (wordsWidth // 2), self.announcerRect.centery)
        x, y = pos
        for line in words:
            for word in line:
                word_surface = FONT.render(word, 0, BLACK)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= wordsWidth:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


    # ------------------------------- OTHER GAME HELPER METHODS -------------------------------

    # FOR BET !!!
    # User to place the bet amount
    def placeBet(self):
        self.betAmount = int(input("How many hearts would you like to bet?: "))

    def initHands(self):
        self.user.addCard(self.deck.drawCard())
        self.user.addCard(self.deck.drawCard())
        self.dealer.addCard(self.deck.drawCard())
        self.dealer.addCard(self.deck.drawCard())

    # FOR BET !!!
    # change bet amount to loss if user lost game
    def updateBetAmount(self, winner):
        if (winner == self.dealer):
            self.betAmount *= -1
        elif (winner == None):
            self.betAmount = 0

    # Determine who the winner of the game is
    def determineWinner(self):
        dealerTotal = self.dealer.getTotal()
        userTotal = self.user.getTotal()
        dealerBusted = self.dealer.isBusted()
        userBusted = self.user.isBusted()
        if (userBusted | ((not dealerBusted) & (dealerTotal > userTotal))):
            self.winner = self.dealer
        elif (dealerBusted | ((not userBusted) & (userTotal > dealerTotal))):
            self.winner = self.user
        else:
            self.winner = None
        # self.updateBetAmount(winner) # FOR BET !!!

    def getWinnerMsg(self):
        return "The winner is... " + self.winner.name + "!!"

    def displayHelp(self):
        howToWinBustText = "How to Win:\n" + "\nOnly Dealer Busts = Win \nOnly You Busts = Lose \nBoth You and Dealer Bust = Lose\n"
        howToWinNoBustText = "No One Busts = Player with highest total closes to 21 wins"
        text = "GOAL: GET AS CLOSE TO A TOTAL OF 21 WITHOUT GOING OVER.\n\n" + howToWinBustText + howToWinNoBustText + "\n\nDon't lose..."
        self.displayLongText(text)

    def displayAnnouncer(self, msgKey):
        self.announceText(msgKey, RED, None)

    def determinAnnouncerState(self):
        msgKey = self.msgList.get(self.curMsg)
        return msgKey
    

    # ------------------------------- USER METHODS -------------------------------

    def displayUserCards(self):
        # Position cards in center no matter amount of cards
        (x, y) = ((1 / 2) * (USER_WIDTH - (self.user.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (self.user.getNumCards() - 1))), 0)
        # Display User's cards
        for card in self.user.cards:
            currCardImg = pygame.image.load(card.getCardImage())
            self.userCardArea.blit(currCardImg, (x, y))
            x += currCardImg.get_width() + CARD_SPACE

        self.screen.blit(self.userCardArea, USER_CARD_COORDS)

    def userHits(self):
        newCard = self.deck.drawCard()
        self.user.addCard(newCard)
        if (self.user.isBusted()):
            self.winner = self.dealer
            self.announceText(self.msgList.get(self.userBustedMsg), RED, None)
            self.curMsg = self.userBustedMsg
            self.playerTurn = self.dealer
            self.startDealerTurn = True
            self.displayContinueButton(self.seeDealersTurnButton, self.seeDealersTurnButtonPos)
            self.dealerContButtonDisplayed = True

    def userStands(self):
        self.playerTurn = self.dealer
        self.announceText(self.msgList.get(self.userStandMsg), RED, None)
        self.curMsg = self.userStandMsg
        self.startDealerTurn = True
        self.displayContinueButton(self.seeDealersTurnButton, self.seeDealersTurnButtonPos)
        self.dealerContButtonDisplayed = True


    # ------------------------------- DEALER METHODS -------------------------------

    def displayDealerCards(self):
        # Position initial dealer cards
        (w, z) = ((1 / 2) * (USER_WIDTH - (self.dealer.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (self.dealer.getNumCards() - 1))), 0)
        if (self.playerTurn == self.user):
            # TO DISPLAY 1 FACEUP 1 FACEDOWN CARD
            currCardImg = pygame.image.load(self.dealer.cards[0].getCardImage())
            self.dealerCardArea.blit(currCardImg, (w, z))
            w += currCardImg.get_width() + CARD_SPACE
            currCardImg = pygame.image.load("blackjack/Images/cards/Card_Back.jpg")
            self.dealerCardArea.blit(currCardImg, (w, z))
        elif (self.playerTurn == self.dealer) and self.startDealerTurn:
            for card in self.dealer.cards:
                currCardImg = pygame.image.load(card.getCardImage())
                self.dealerCardArea.blit(currCardImg, (w, z))
                w += currCardImg.get_width() + CARD_SPACE
        self.screen.blit(self.dealerCardArea, DEALER_CARD_COORDS)

    def dealerTurn(self):
        while (self.dealer.getTotal() < 17):
            self.dealerHits()
        if (self.dealer.getTotal() == 21):
            self.announceText(self.msgList.get(self.dealerBJMsg), RED, None)
            self.curMsg = self.dealerBJMsg
        elif (self.dealer.getTotal() > 21):
            self.announceText(self.msgList.get(self.dealerBustedMsg), RED, None)
            self.curMsg = self.dealerBustedMsg
        elif (self.dealer.getTotal() >= 17):
            self.announceText(self.msgList.get(self.dealerStandsMsg), RED, None)
            self.curMsg = self.dealerStandsMsg
        self.displayContinueButton(self.seeWinnerButton, self.seeWinnerButtonPos)
        self.winnerContButtonDisplayed = True
        self.gameEnd = True

    def dealerHits(self):
        self.dealer.addCard(self.deck.drawCard())

    # ------------------------------- REFACTORED GAME METHODS -------------------------------

    def runGame(self):
        # running = True
        while self.running:
            if (not self.pause):
                self.createAreas()
                self.displayScreen()

            mouse = pygame.mouse.get_pos()
            self.handleEvent(mouse)

            pygame.display.update()

    def createAreas(self):
        # Area to display announcer text
        self.announcerArea = pygame.surface.Surface((WIDTH, FONT.get_height()))
        self.announcerArea.fill(BACKGROUND_COLOUR)
        
        # Area to display user's cards
        self.userCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
        self.userCardArea.fill(BACKGROUND_COLOUR)

        # Area to display dealer's cards
        self.dealerCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
        self.dealerCardArea.fill(BACKGROUND_COLOUR)
    
    def displayScreen(self):
        if self.displayStartScreen:
            self.screen.fill(BACKGROUND_COLOUR)
            self.displayLongText("It's time to gamble with a game of BlackJack! \n\nGoal of game: get 21 without going over. \n\nClick anywhere to start")
        elif self.displayEndScreen:
            self.screen.fill(BACKGROUND_COLOUR)
            userEndCountText = "\nYour total: " + str(self.user.getTotal()) + (" (Busted)" if self.user.isBusted() else "") + (" (BlackJack)" if self.user.hasBlackjack() else "")
            dealerEndCountText = "\nDealer total: " + str(self.dealer.getTotal()) + (" (Busted)" if self.dealer.isBusted() else "") + (" (BlackJack)" if self.dealer.hasBlackjack() else "")
            toExitText = "\n\nExit window to return to main game"
            
            if self.winner == self.dealer:
                textToDisplay = "Oh no! You've lost!\n" + userEndCountText + dealerEndCountText + toExitText
                self.displayLongText(textToDisplay)   
            elif self.winner ==self.user:
                textToDisplay = "Congratulations, you've won!\n" + userEndCountText + dealerEndCountText + toExitText
                self.displayLongText(textToDisplay)
            else:
                textToDisplay = "PUSH! It's a draw!\n" + userEndCountText + dealerEndCountText + toExitText
                self.displayLongText(textToDisplay)   
        elif self.endBlackJackScreen:
            self.screen.fill(BLACK)
        elif self.displayGameScreen:
            self.displayMainGame()
    
    def checkHelpEvent(self, mouse):
        # Display help info if mouse hovers over help button
        if (not self.displayStartScreen and not self.displayEndScreen and (self.helpButtonPos[0] <= mouse[0] <= WIDTH) and (self.helpButtonPos[1] <= mouse[1] <= HEIGHT)):
            self.screen.fill(BACKGROUND_COLOUR)
            self.displayHelp()
            self.pause = True
        else:
            if (self.pause):
                self.screen.fill(BACKGROUND_COLOUR)
            self.pause = False
    
    def handleEvent(self, mouse):
        self.checkHelpEvent(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.gameEnd:
                    self.determineWinner()
                    self.displayGameScreen = False
                    self.displayEndScreen = True
                elif self.displayStartScreen:
                    self.screen.fill(BACKGROUND_COLOUR)
                    self.announceText(self.msgList.get(self.userTurnMsg), RED, None)
                    self.curMsg = self.userTurnMsg
                    self.displayGameScreen = True
                    self.displayStartScreen = False
                # User chooses to stand
                elif (self.playerTurn == self.user) and (self.standButtonPos[0] <= mouse[0] <= (self.standButtonPos[0] + self.standButton.get_width()) and self.standButtonPos[1] <= mouse[1] <= (self.standButtonPos[1] + self.standButton.get_height())):
                    if (self.playerTurn == self.user):
                        self.userStands()
                # User chooses to hit
                elif (self.playerTurn == self.user) and (self.hitButtonPos[0] <= mouse[0] <= (self.hitButtonPos[0] + self.hitButton.get_width()) and self.hitButtonPos[1] <= mouse[1] <= (self.hitButtonPos[1] + self.hitButton.get_height())):
                    if (self.playerTurn == self.user):
                        self.userHits()
                # Dealer's Turn
                elif self.startDealerTurn and (self.playerTurn == self.dealer) and (not self.gameEnd):
                    self.dealerTurn()


# ------------------------------- TESTING -------------------------------

game1 = BlackJackGame(True)