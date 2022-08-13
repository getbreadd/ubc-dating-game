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

# ------------------------------- INITIALIZE GAME STATS -------------------------------

# initialize deck and players
deck = Deck()
user = Player('User')
dealer = Player('Dealer')

# ------------------------------- GAME VARIABLES -------------------------------

playerTurn = user
betAmount = 0  # FOR BET !!!
winner = None

initMessage = "LET'S GIVE AWAY ALL YOUR MONEYYYYY ^ - ^"
announcer = FONT.render(initMessage, True, RED, None)
announcerRect = announcer.get_rect()
announcerRect.center = (WIDTH // 2, HEIGHT // 10)
smallFont = pygame.font.Font('freesansbold.ttf', 28)
cardTotalFont = pygame.font.Font('freesansbold.ttf', 18)

startDealerTurn = False

gameEnd = False

displayEndScreen = False
displayStartScreen = True
displayGameScreen = False
endBlackJackScreen = False

gameOver = False

dealerContButtonDisplayed = False
winnerContButtonDisplayed = False
pause = False

curMsg = ""
userTurnMsg = "userTurn"
userBJMsg = "userBJ"
userBustedMsg = "userBusted"
userStandMsg = "userStands"
dealerBJMsg = "dealerBJ"
dealerBustedMsg = "dealerBusted"
dealerStandsMsg = "dealerStands"

msgList = {
    userTurnMsg: USER_TURN_MSG,
    userBJMsg: USER_BJ,
    userBustedMsg: USER_BUSTED,
    userStandMsg: USER_STANDS,
    dealerBJMsg: DEALER_BJ,
    dealerBustedMsg: DEALER_BUSTED,
    dealerStandsMsg: DEALER_STANDS,
}


# ------------------------------- INITIALIZE PYGAME SCREEN -------------------------------

# initialize screen and display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND_COLOUR)
pygame.display.set_caption("It's time to gamble!")
pygame.display.flip()


# =======================================================================================
# HELPER METHODS
# =======================================================================================

# ------------------------------- OTHER UI HELPER METHODS -------------------------------

# Change Announcer message
def announceText(msg, msgColour, bckgdColour):
    global announcer
    announcer = FONT.render(msg, True, msgColour, bckgdColour)
    announcerRect = announcer.get_rect()
    announcerRect.center = (WIDTH // 2, HEIGHT // 10)
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, 0, WIDTH, (DEALER_CARD_COORDS[1] - smallFont.get_height() - 10)))
    announcerArea.blit(announcer, (0, 0))
    screen.blit(announcerArea, announcerRect)
    pygame.display.update()

def createTextButton(msg, msgColour, bckgdColour, width):
    text = FONT.render(msg, True, msgColour, None)
    buttonSurface = pygame.surface.Surface((width, text.get_height()))
    buttonSurface.fill(bckgdColour)
    buttonSurface.blit(text, ((buttonSurface.get_width() // 2) - (text.get_width() // 2), (buttonSurface.get_height() // 2) - (text.get_height() // 2)))
    return buttonSurface

def buttonClicked():
    text = FONT.render("CLICKED", True, BLACK, None)
    buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
    buttonSurface.fill(RED)
    buttonSurface.blit(text, (0, 0))
    return buttonSurface

def getStringWidth(str):
    text = FONT.render(str, True, BLACK, None)
    width = text.get_width()
    return width

def displayContinueButton(button, buttonPos):
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, hitButtonPos[1], WIDTH, hitButton.get_height()))
    screen.blit(button, buttonPos)
    
def displayMainGame():
    global playerTurn, startDealerTurn, dealerCardTextArea
    global curMsg, dealerContButtonDisplayed
    # Position cards in center no matter amount of cards
    (x, y) = ((1 / 2) * (USER_WIDTH - (user.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (user.getNumCards() - 1))), 0)
    # Display User's cards
    for card in user.cards:
        currCardImg = pygame.image.load(card.getCardImage())
        userCardArea.blit(currCardImg, (x, y))
        x += currCardImg.get_width() + CARD_SPACE

    screen.blit(userCardArea, USER_CARD_COORDS)
    
    # Position initial dealer cards
    (w, z) = ((1 / 2) * (USER_WIDTH - (dealer.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (dealer.getNumCards() - 1))), 0)
    if (playerTurn == user):
         # TO DISPLAY 1 FACEUP 1 FACEDOWN CARD
        currCardImg = pygame.image.load(dealer.cards[0].getCardImage())
        dealerCardArea.blit(currCardImg, (w, z))
        w += currCardImg.get_width() + CARD_SPACE
        currCardImg = pygame.image.load("blackjack/Images/cards/Card_Back.jpg")
        dealerCardArea.blit(currCardImg, (w, z))
    elif (playerTurn == dealer) and startDealerTurn:
        for card in dealer.cards:
            currCardImg = pygame.image.load(card.getCardImage())
            dealerCardArea.blit(currCardImg, (w, z))
            w += currCardImg.get_width() + CARD_SPACE
    screen.blit(dealerCardArea, DEALER_CARD_COORDS)
    
    # Position the "Dealer's Cards" and "User's Cards" text
    dealerCardText = smallFont.render("Dealer's Cards", True, BLACK, None)
    dealerCardTextArea = dealerCardText.get_rect()
    screen.blit(dealerCardText, ((WIDTH // 2) - (dealerCardTextArea.width // 2), (DEALER_CARD_COORDS[1] - dealerCardTextArea.height - 10)))
    
    userCardText = smallFont.render("Your Cards", True, BLACK, None)
    userCardTextArea = userCardText.get_rect()
    screen.blit(userCardText, ((WIDTH // 2) - (userCardTextArea.width // 2), (USER_CARD_COORDS[1] - userCardTextArea.height - 10)))
    
    # Position the "Dealer Total" and "Your total" text
    if (playerTurn == dealer):
        dealerTotalText = cardTotalFont.render(("Total: " + str(dealer.getTotal())), True, BLACK, None)
    else:
        dealerTotalText = cardTotalFont.render(("Total: ?"), True, BLACK, None)
    dealerTotalTextArea = dealerTotalText.get_rect()
    screen.blit(dealerTotalText, ((WIDTH // 2) - (dealerTotalTextArea.width // 2), (DEALER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    
    userTotalText = cardTotalFont.render(("Total: " + str(user.getTotal())), True, BLACK, None)
    userTotalTextArea = userTotalText.get_rect()
    screen.blit(userTotalText, ((WIDTH // 2) - (userTotalTextArea.width // 2), (USER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    pygame.display.update()
    
    # user turn
    if (user.hasBlackjack() and playerTurn == user):
        announceText(msgList.get(userBJMsg), RED, None)
        curMsg = userBJMsg
        playerTurn = dealer
        startDealerTurn = True
        displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
        dealerContButtonDisplayed = True
    
    # Add Button
    if (playerTurn == user):
        screen.blit(hitButton, hitButtonPos)
        screen.blit(standButton, standButtonPos)
    
    if (dealerContButtonDisplayed and not gameEnd):
        displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
    if (winnerContButtonDisplayed):
        displayContinueButton(seeWinnerButton, seeWinnerButtonPos)
        
    # Add Help Button
    screen.blit(helpButton, helpButtonPos)

    # Set Announcer
    curAnnouncedMsg = determinAnnouncerState()
    displayAnnouncer(curAnnouncedMsg)
        
def displayLongText(msg):
    words = [word.split(' ') for word in msg.splitlines()]
    space = FONT.size(' ')[0]
    wordsWidth = USER_WIDTH + (USER_WIDTH // 4)
    wordsHeight = HEIGHT// 3
    pos = ((WIDTH // 2) - (wordsWidth // 2), announcerRect.centery)
    x, y = pos
    for line in words:
        for word in line:
            word_surface = FONT.render(word, 0, BLACK)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= wordsWidth:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


# ------------------------------- OTHER GAME HELPER METHODS -------------------------------

# FOR BET !!!
# User to place the bet amount
def placeBet():
    global betAmount
    betAmount = int(input("How many hearts would you like to bet?: "))

def initHands():
    user.addCard(deck.drawCard())
    user.addCard(deck.drawCard())
    dealer.addCard(deck.drawCard())
    dealer.addCard(deck.drawCard())

# FOR BET !!!
# change bet amount to loss if user lost game
def updateBetAmount(winner):
    global betAmount
    if (winner == dealer):
        betAmount *= -1
    elif (winner == None):
        betAmount = 0

# Determine who the winner of the game is
def determineWinner():
    global winner
    dealerTotal = dealer.getTotal()
    userTotal = user.getTotal()
    dealerBusted = dealer.isBusted()
    userBusted = user.isBusted()
    if (userBusted | ((not dealerBusted) & (dealerTotal > userTotal))):
        winner = dealer
    elif (dealerBusted | ((not userBusted) & (userTotal > dealerTotal))):
        winner = user
    else:
        winner = None
    # updateBetAmount(winner) # FOR BET !!!

def getWinnerMsg():
    return "The winner is... " + winner.name + "!!"

def displayHelp():
    howToWinBustText = "How to Win:\n" + "\nOnly Dealer Busts = Win \nOnly You Busts = Lose \nBoth You and Dealer Bust = Lose\n"
    howToWinNoBustText = "No One Busts = Player with highest total closes to 21 wins"
    text = "GOAL: GET AS CLOSE TO A TOTAL OF 21 WITHOUT GOING OVER.\n\n" + howToWinBustText + howToWinNoBustText + "\n\nDon't lose..."
    displayLongText(text)

def displayAnnouncer(msgKey):
    announceText(msgKey, RED, None)

def determinAnnouncerState():
    msgKey = msgList.get(curMsg)
    return msgKey
  

# ------------------------------- USER METHODS -------------------------------

def userHits():
    global winner
    newCard = deck.drawCard()
    user.addCard(newCard)
    if (user.isBusted()):
        winner = dealer

def userStands():
    global playerTurn
    playerTurn = dealer


# ------------------------------- DEALER METHODS -------------------------------

def dealerHits():
    dealer.addCard(deck.drawCard())


#  ------------------------------- PYGAME -------------------------------

initHands()

# Create buttons
userButtonWidth = WIDTH * 0.14
hitText = "HIT"
standText = "STAND"

hitButton = createTextButton(hitText, BLACK, STEEL_BLUE, userButtonWidth)
standButton = createTextButton(standText, BLACK, STEEL_BLUE, userButtonWidth)

hitButtonPos = ((WIDTH // 2) - hitButton.get_width() - CARD_SPACE, USER_BUTTONS_Y)
standButtonPos = ((WIDTH // 2) + CARD_SPACE, USER_BUTTONS_Y)

seeDealersTurnText = "Click to see dealer's turn"
seeDealersTurnButton = createTextButton(seeDealersTurnText, BLACK, STEEL_BLUE, getStringWidth(seeDealersTurnText))
seeDealersTurnButtonPos = ((WIDTH // 2) - (seeDealersTurnButton.get_width() // 2), HEIGHT * 0.85)

seeWinnerText = "Click to see Winner!"
seeWinnerButton = createTextButton(seeWinnerText, BLACK, STEEL_BLUE, getStringWidth(seeWinnerText))
seeWinnerButtonPos = ((WIDTH // 2) - (seeWinnerButton.get_width() // 2), HEIGHT * 0.85)

helpButton = createTextButton("?", BLACK, BLUE, WIDTH * 0.05)
helpButtonPos = (WIDTH - helpButton.get_width(), HEIGHT - helpButton.get_height())

running = True
while running:
    if (not pause):
        # Area to display announcer text
        announcerArea = pygame.surface.Surface((WIDTH, FONT.get_height()))
        announcerArea.fill(BACKGROUND_COLOUR)
        
        # Area to display user's cards
        userCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
        userCardArea.fill(BACKGROUND_COLOUR)

        # Area to display dealer's cards
        dealerCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
        dealerCardArea.fill(BACKGROUND_COLOUR)
        
        if displayStartScreen:
            screen.fill(BACKGROUND_COLOUR)
            displayLongText("It's time to gamble with a game of BlackJack! \n\nGoal of game: get 21 without going over. \n\nClick anywhere to start")
        elif displayEndScreen:
            screen.fill(BACKGROUND_COLOUR)
            userEndCountText = "\nYour total: " + str(user.getTotal()) + (" (Busted)" if user.isBusted() else "") + (" (BlackJack)" if user.hasBlackjack() else "")
            dealerEndCountText = "\nDealer total: " + str(dealer.getTotal()) + (" (Busted)" if dealer.isBusted() else "") + (" (BlackJack)" if dealer.hasBlackjack() else "")
            toExitText = "\n\nExit window to return to main game"
            
            if winner == dealer:
                textToDisplay = "Oh no! You've lost!\n" + userEndCountText + dealerEndCountText + toExitText
                displayLongText(textToDisplay)   
            elif winner == user:
                textToDisplay = "Congratulations, you've won!\n" + userEndCountText + dealerEndCountText + toExitText
                displayLongText(textToDisplay)
            else:
                textToDisplay = "PUSH! It's a draw!\n" + userEndCountText + dealerEndCountText + toExitText
                displayLongText(textToDisplay)   
        elif endBlackJackScreen:
            screen.fill(BLACK)
        elif displayGameScreen:
            displayMainGame()

    mouse = pygame.mouse.get_pos()

    # Display help info if mouse hovers over help button
    if (not displayStartScreen and not displayEndScreen and (helpButtonPos[0] <= mouse[0] <= WIDTH) and (helpButtonPos[1] <= mouse[1] <= HEIGHT)):
        screen.fill(BACKGROUND_COLOUR)
        displayHelp()
        pause = True
    else:
        if (pause):
            screen.fill(BACKGROUND_COLOUR)
        pause = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameEnd:
                determineWinner()
                displayGameScreen = False
                displayEndScreen = True
            elif displayStartScreen:
                screen.fill(BACKGROUND_COLOUR)
                announceText(msgList.get(userTurnMsg), RED, None)
                curMsg = userTurnMsg
                displayGameScreen = True
                displayStartScreen = False
            # User chooses to stand
            elif (playerTurn == user) and (standButtonPos[0] <= mouse[0] <= (standButtonPos[0] + standButton.get_width()) and standButtonPos[1] <= mouse[1] <= (standButtonPos[1] + standButton.get_height())):
                if (playerTurn == user):
                    userStands()
                    announceText(msgList.get(userStandMsg), RED, None)
                    curMsg = userStandMsg
                    startDealerTurn = True
                    displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
                    dealerContButtonDisplayed = True
            # User chooses to hit
            elif (playerTurn == user) and (hitButtonPos[0] <= mouse[0] <= (hitButtonPos[0] + hitButton.get_width()) and hitButtonPos[1] <= mouse[1] <= (hitButtonPos[1] + hitButton.get_height())):
                if (playerTurn == user):
                    userHits()
                    if (user.isBusted()):
                        announceText(msgList.get(userBustedMsg), RED, None)
                        curMsg = userBustedMsg
                        playerTurn = dealer
                        startDealerTurn = True
                        displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
                        dealerContButtonDisplayed = True
            # Dealer's Turn
            elif startDealerTurn and (playerTurn == dealer) and (not gameEnd):
                while (dealer.getTotal() < 17):
                    dealerHits()
                if (dealer.getTotal() == 21):
                    announceText(msgList.get(dealerBJMsg), RED, None)
                    curMsg = dealerBJMsg
                elif (dealer.getTotal() > 21):
                    announceText(msgList.get(dealerBustedMsg), RED, None)
                    curMsg = dealerBustedMsg
                elif (dealer.getTotal() >= 17):
                    announceText(msgList.get(dealerStandsMsg), RED, None)
                    curMsg = dealerStandsMsg
                displayContinueButton(seeWinnerButton, seeWinnerButtonPos)
                winnerContButtonDisplayed = True
                gameEnd = True

    pygame.display.update()


