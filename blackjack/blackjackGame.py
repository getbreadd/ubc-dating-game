from logging import setLogRecordFactory
from venv import create
import pygame
# from PIL import Image
from blackjackPlayer import *
from blackjackDeck import *

pygame.init()

# ------------------------------- CONSTANTS -------------------------------

# WIDTH = 1000
WIDTH = 850
# HEIGHT = 700
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

# ------------------------------- INITIALIZE GAME STATS -------------------------------

# initialize deck and players
deck = Deck()
# deck.printCards();
user = Player('User')
dealer = Player('Dealer')

# ------------------------------- GAME VARIABLES -------------------------------

playerTurn = user
betAmount = 0
global winner
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


# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# player.printCards()
# total = player.getTotal()
# print('total: ', total)

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
    # screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, 0, WIDTH, (DEALER_CARD_COORDS[1] - dealerCardTextArea.height - 10)))
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, 0, WIDTH, (DEALER_CARD_COORDS[1] - smallFont.get_height() - 10)))
    announcerArea.blit(announcer, (0, 0))
    screen.blit(announcerArea, announcerRect)
    pygame.display.update()

def createTextButton(msg, msgColour, bckgdColour, width):
    text = FONT.render(msg, True, msgColour, None)
    # buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
    buttonSurface = pygame.surface.Surface((width, text.get_height()))
    buttonSurface.fill(bckgdColour)
    buttonSurface.blit(text, ((buttonSurface.get_width() // 2) - (text.get_width() // 2), (buttonSurface.get_height() // 2) - (text.get_height() // 2)))
    return buttonSurface

def createSizedTextButton(msg, msgColour, bckgdColour):
    text = FONT.render(msg, True, msgColour, None)
    buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
    # buttonSurface = pygame.surface.Surface((width, text.get_height()))
    buttonSurface.fill(bckgdColour)
    buttonSurface.blit(text, ((buttonSurface.get_width() // 2) - (text.get_width() // 2), (buttonSurface.get_height() // 2) - (text.get_height() // 2)))
    return buttonSurface
    
# def createImageButton(img, bckgdColour):
#     buttonSurface = pygame.surface.Surface((img.get_width(), img.get_height()))
#     buttonSurface.fill(bckgdColour)
#     buttonSurface.blit(img, (0, 0))
#     return buttonSurface

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

def getStringHeight(str):
    text = FONT.render(str, True, BLACK, None)
    height = text.get_height()
    return height

def displayDealerContinueButton():
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, hitButtonPos[1], WIDTH, hitButton.get_height()))
    screen.blit(seeDealersTurnButton, seeDealersTurnButtonPos)
    
def displayClickToSeeWinnerButton():
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (0, hitButtonPos[1], WIDTH, hitButton.get_height()))
    screen.blit(seeWinnerButton, seeWinnerButtonPos)
    
# def displayEndScreen():
#     screen.fill(pygame.Color(BACKGROUND_COLOUR))
#     announceText("HERE", RED, None)
    
def displayMainGame():
    global playerTurn
    global startDealerTurn
    global dealerCardTextArea
    # Position cards in center no matter amount of cards
    (x, y) = ((1 / 2) * (USER_WIDTH - (user.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (user.getNumCards() - 1))), 0)
    # Display User's cards
    for card in user.cards:
        currCardImg = pygame.image.load(card.getCardImage())
        # currCardImg = pygame.transform.scale(currCardImg, ((HEIGHT // 7), (WIDTH // 7)))  # resize test
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
        currCardImg = pygame.image.load("blackjack/Images/cards/Card_Back.jpg") # FILL IN LATER
        dealerCardArea.blit(currCardImg, (w, z))
    elif (playerTurn == dealer) and startDealerTurn:
        # dealerCardArea.fill(BACKGROUND_COLOUR)
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
    # dealerTotalText = cardTotalFont.render(("Total: " + str(dealer.getTotal())), True, BLACK, None)
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
    # !!! refactor with helper method for the text stuff later
    
    # user turn
    if (user.hasBlackjack() and playerTurn == user):
        announceText("BLACKJACK!! Dealer's turn...", RED, None)
        playerTurn = dealer
        startDealerTurn = True
        displayDealerContinueButton()
    
    # dealer turn
    
    # ending screen
    
    # Add Button
    if (playerTurn == user):
        screen.blit(hitButton, hitButtonPos)
        screen.blit(standButton, standButtonPos)
        
        
    # user turn
    # if (user.hasBlackjack() and playerTurn == user):
    #     announceText("BLACKJACK!! Dealer's turn...", RED, None)
    #     playerTurn = dealer
    #     startDealerTurn = True
    #    # displayDealerContinueButton()
    #     displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
    
    # dealer turn

    # Winner Determined
    # if (gameOver):
    #    determineWinner()
    #    displayContinueButton(seeWinnerButton, seeWinnerButtonPos)
        
def displayLongText(msg):
    words = [word.split(' ') for word in msg.splitlines()]
    space = FONT.size(' ')[0]
    wordsWidth = (WIDTH // 5) * 3 
    wordsHeight = HEIGHT// 3
    pos = (WIDTH // 5, HEIGHT // 5)
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
            
def displayContinueButton(button, buttonPos):
    screen.fill(pygame.Color(BACKGROUND_COLOUR), (hitButtonPos[0], hitButtonPos[1], WIDTH, hitButton.get_height()))
    screen.blit(button, buttonPos)


# ------------------------------- OTHER GAME HELPER METHODS -------------------------------

# User to place the bet amount
def placeBet():
    global betAmount
    betAmount = int(input("How many hearts would you like to bet?: "))

def initHands():
    user.addCard(deck.drawCard())
    user.addCard(deck.drawCard())
    dealer.addCard(deck.drawCard())
    dealer.addCard(deck.drawCard())
    print("Starting cards:")
    user.printCards()
    dealer.printCards()
    # dealer.addCard(deck.drawCard())

# change bet amount to loss if user lost game
def updateBetAmount(winner):
    global betAmount
    if (winner == dealer):
        betAmount *= -1
    elif (winner == None):
        betAmount = 0

# Determine who the winner of the game is
def determineWinner():
    # global winner
    if (winner == None):
        dealerTotal = dealer.getTotal()
        userTotal = user.getTotal()
        dealerBusted = dealer.isBusted()
        userBusted = user.isBusted()
        # dealer wins
        if (userBusted | ((not dealerBusted) & (dealerTotal > userTotal))):
            winner = dealer
        elif (dealerBusted | ((not userBusted) & (userTotal > dealerTotal))):
            winner = user
        else:
            winner = None
            # <CONSOLE>
            # print("PUSH!")
    updateBetAmount(winner)

# <CONSOLE>
# def printWinner():
#     global winner
#     if (winner == None):
#         winner = "No one"
#         print("The winner is...", winner, "!!", sep = "")
#     else:
#         print("The winner is...", winner.getName(), "!!", sep = "")

def setGameOver(isGameOver):
    global gameOver
    gameOver = isGameOver
  

# ------------------------------- USER METHODS -------------------------------

# <CONSOLE>
# User takes a turn: hit or stand
# hit -> deal a card to user's hand
#     -> check value for busted -> busted? end turn : continue
# stand -> end turn
# def userTurn():
#     global playerTurn, winner
#     if user.isBusted():
#         winner = dealer
#         print("You bust!!")
#         return
#     print("It's your turn!!")
#     while(playerTurn == user):
#         user.printCards()
#         print("Total: " + str(user.getTotal()))
#         if (user.hasBlackjack()):
#             user.printCards()
#             print("Congrats! You got BLACKJACK!!")
#             return
#         choice = input("Would you like to hit or stand?: ")
#         if (choice.casefold() == "hit"):
#             newCard = deck.drawCard()
#             user.addCard(newCard)
#             if (user.isBusted()):
#                 winner = dealer
#                 user.printCards()
#                 print("Total: " + str(user.getTotal()))
#                 print("You're busted! RIP")
#                 # playerTurn = dealer
#                 return
#         elif (choice.casefold() == "stand"):
#             playerTurn = dealer
#             return
#         else:
#             print("Not a valid response. Try again...")

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

# <CONSOLE>
# def dealerPrintHand():
#     print("Dealer cards:")
#     dealer.printCards()
#     print("Total:",dealer.getTotal(),end="\n")
#     return

# <CONSOLE>
# def dealerTurn():
#     inp = input('---Enter for dealer turn---')
#     while (inp != ""):
#         inp = input('---Please press enter for dealer turn---')
#     while (dealer.getTotal() < 17):
#         dealerPrintHand()
#         print("Dealer hits")
#         dealer.addCard(deck.drawCard())
#         inp = input('---Please press enter to continue---')
#         while (inp != ""):
#             inp = input('---Please press enter for to continue---')
#     dealerPrintHand()
#     if (dealer.hasBlackjack()):
#         print("Dealer has BLACKJACK!!")
#     elif (dealer.isBusted()):
#         print("Dealer busts!")
#     else:
#         print("Dealer stands")
#     return

def dealerHits():
    dealer.addCard(deck.drawCard())


# ------------------------------- CONSOLE TESTING -------------------------------

# print("Starting amount of hearts: ", user.getBankrollAmount(), sep = "")
# placeBet()
# user.addCard(deck.drawCard())
# user.addCard(deck.drawCard())
# dealer.addCard(deck.drawCard())
# print("Starting cards:")
# user.printCards()
# dealer.printCards()
# dealer.addCard(deck.drawCard())
# print("----------------------------------")
# userTurn()
# print("----------------------------------")
# dealerTurn()
# print("----------------------------------")
# determineWinner()
# printWinner()
# user.updateBankroll(betAmount)
# print("Remaining hearts: ", user.getBankrollAmount(), sep = "")

#  ------------------------------- PYGAME -------------------------------

initHands()
# card = deck.drawCard()
# user.addCard(card)
user.printCards()

# Create buttons
userButtonWidth = WIDTH * 0.14
hitText = "HIT"
standText = "STAND"

hitButton = createTextButton(hitText, BLACK, STEEL_BLUE, userButtonWidth)
standButton = createTextButton(standText, BLACK, STEEL_BLUE, userButtonWidth)

hitButtonPos = ((WIDTH // 2) - hitButton.get_width() - CARD_SPACE, USER_BUTTONS_Y)
standButtonPos = ((WIDTH // 2) + CARD_SPACE, USER_BUTTONS_Y)

# seeDealersTurnButton = createTextButton("Click to see dealer's turn", BLACK, STEEL_BLUE, USER_WIDTH)
# seeDealersTurnButtonPos = ((WIDTH // 2) - (seeDealersTurnButton.get_width() // 2), USER_BUTTONS_Y)

# seeWinnerButton = createTextButton("Click to see the winner", BLACK, STEEL_BLUE, USER_WIDTH)
# seeWinnerButtonPos = ((WIDTH // 2) - (seeWinnerButton.get_width() // 2), USER_BUTTONS_Y)

seeDealersTurnButton = createSizedTextButton("Click to see dealer's turn", BLACK, STEEL_BLUE)
seeDealersTurnButtonPos = ((WIDTH // 2) - (seeDealersTurnButton.get_width() // 2), HEIGHT * 0.85)

seeWinnerButton = createSizedTextButton("Click to see Winner!", BLACK, STEEL_BLUE)
seeWinnerButtonPos = ((WIDTH // 2) - (seeWinnerButton.get_width() // 2), HEIGHT * 0.85)

# buttonPos = ((WIDTH // 2))

running = True
while running:
    
    # Area to display announcer text
    announcerArea = pygame.surface.Surface((WIDTH, FONT.get_height()))
    announcerArea.fill(BACKGROUND_COLOUR)
    
    # Area to display user's cards
    userCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
    userCardArea.fill(BACKGROUND_COLOUR)

    # Area to display dealer's cards
    dealerCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
    dealerCardArea.fill(BACKGROUND_COLOUR)

    # Initial message to user
    # announceText(initMessage, RED, None)ß
    
    # help button
    # TODO !!!
    
    if displayStartScreen:
        screen.fill(BACKGROUND_COLOUR)
        displayLongText("It's time to gamble with a game of BlackJack! Goal of game: get 21 without going over. Click anywhere to start")
    elif displayEndScreen:
        screen.fill(BACKGROUND_COLOUR)
        endCountText = "Your total: " + str(user.getTotal()) + "\nDealer total: " + str(dealer.getTotal())
        toExitText = "\nExit window to return to main game"
        
        if winner == dealer:
            textToDisplay = "Oh no! You've lost!\n" + endCountText + toExitText
            displayLongText(textToDisplay)   
        elif winner == user:
            textToDisplay = "Congratulations, you've won!\n" + endCountText + toExitText
            displayLongText(textToDisplay)
        else:
            textToDisplay = "It's a tie!\n" + endCountText + toExitText
            displayLongText(textToDisplay)   
    elif endBlackJackScreen:
        screen.fill(BLACK)
    elif displayGameScreen:
        displayMainGame()
    # # For inlcuding images
    # currCardImg = pygame.image.load('blackjack/Images/2C.jpg')
    # screen.blit(currCardImg, (0, 0))

    # User's turn
    # pause = input("Press enter to continue...")
    # announceText("IT'S YOUR TURN!! GIVE ME THAT MONEY", RED, None)
    # userTurn()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gameEnd:
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
                displayGameScreen = False
                displayEndScreen = True
            elif displayStartScreen:
                screen.fill(BACKGROUND_COLOUR)
                announceText("It's your turn! Hit or Stand?", RED, None)
                displayGameScreen = True
                displayStartScreen = False
            # elif displayEndScreen:
            #     displayEndScreen = False
            # User chooses to stand
            elif (playerTurn == user) and (standButtonPos[0] <= mouse[0] <= (standButtonPos[0] + standButton.get_width()) and standButtonPos[1] <= mouse[1] <= (standButtonPos[1] + standButton.get_height())):
                if (playerTurn == user):
                    userStands()
                    announceText("You stand. Dealer's turn...", RED, None)
                    startDealerTurn = True
                    displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
                    # button2 = buttonClicked()
                    # screen.blit(button2, (600, 100))
            # User chooses to hit
            elif (playerTurn == user) and (hitButtonPos[0] <= mouse[0] <= (hitButtonPos[0] + hitButton.get_width()) and hitButtonPos[1] <= mouse[1] <= (hitButtonPos[1] + hitButton.get_height())):
                if (playerTurn == user):
                    userHits()
                    if (user.isBusted()):
                        announceText("YOU'RE BUSTED! Dealer's turn...", RED, None)
                        playerTurn = dealer
                        startDealerTurn = True
                        displayContinueButton(seeDealersTurnButton, seeDealersTurnButtonPos)
                    # button3 = buttonClicked()
                    # screen.blit(button3, (100, 100))
            elif startDealerTurn and (playerTurn == dealer) and (not gameEnd):
            # elif startDealerTurn and (playerTurn == dealer) and (seeDealersTurnButtonPos[0] <= mouse[0] <= (seeDealersTurnButtonPos[0] + seeDealersTurnButton.get_width()) and seeDealersTurnButtonPos[1] <= mouse[1] <= (seeDealersTurnButtonPos[1] + seeDealersTurnButton.get_height())):
                # announceText("TEST", RED, None)
                while (dealer.getTotal() < 17):
                    dealerHits()
                if (dealer.getTotal() == 21):
                    announceText("Dealer has BLACKJACK!", RED, None)
                elif (dealer.getTotal() > 21):
                    announceText("Dealer busts!", RED, None)
                elif (dealer.getTotal() >= 17):
                    announceText("Dealer stands", RED, None)
                displayClickToSeeWinnerButton()
                gameEnd = True
            #    setGameOver(True)
            #elif gameOver:
            #    if (winner == None):
            #        announceText("PUSH! It's a draw!", RED, None)
            #    else:
            #        announceText("The winner is... " + winner.name + "!!", RED, None)
    pygame.display.update()


