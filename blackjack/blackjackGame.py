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
winner = None

initMessage = "LET'S GIVE AWAY ALL YOUR MONEYYYYY ^ - ^"
announcer = FONT.render(initMessage, True, RED, None)
announcerRect = announcer.get_rect()
announcerRect.center = (WIDTH // 2, HEIGHT // 10)
smallFont = pygame.font.Font('freesansbold.ttf', 28)
cardTotalFont = pygame.font.Font('freesansbold.ttf', 18)

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

# Change Announcer mesage
def announceText(msg, msgColour, bckgdColour):
    global announcer
    announcer = FONT.render(msg, True, msgColour, bckgdColour)
    announcerArea = pygame.surface.Surface((announcer.get_width(), announcer.get_height()))
    announcerArea.fill(BACKGROUND_COLOUR)
    announcerArea.blit(announcer, (0, 0))
    screen.blit(announcerArea, announcerRect)
    # pygame.display.update()

def createTextButton(msg, msgColour, bckgdColour):
    text = FONT.render(msg, True, msgColour, None)
    # buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
    buttonSurface = pygame.surface.Surface((WIDTH * 0.14, text.get_height()))
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
    global winner
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
            print("PUSH!")
    updateBetAmount(winner)

def printWinner():
    global winner
    if (winner == None):
        winner = "No one"
        print("The winner is...", winner, "!!", sep = "")
    else:
        print("The winner is...", winner.getName(), "!!", sep = "")
  

# ------------------------------- USER METHODS -------------------------------

# User takes a turn: hit or stand
# hit -> deal a card to user's hand
#     -> check value for busted -> busted? end turn : continue
# stand -> end turn
def userTurn():
    global playerTurn, winner
    if user.isBusted():
        winner = dealer
        print("You bust!!")
        return
    print("It's your turn!!")
    while(playerTurn == user):
        user.printCards()
        print("Total: " + str(user.getTotal()))
        if (user.hasBlackjack()):
            user.printCards()
            print("Congrats! You got BLACKJACK!!")
            return
        choice = input("Would you like to hit or stand?: ")
        if (choice.casefold() == "hit"):
            newCard = deck.drawCard()
            user.addCard(newCard)
            if (user.isBusted()):
                winner = dealer
                user.printCards()
                print("Total: " + str(user.getTotal()))
                print("You're busted! RIP")
                # playerTurn = dealer
                return
        elif (choice.casefold() == "stand"):
            playerTurn = dealer
            return
        else:
            print("Not a valid response. Try again...")

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

def dealerPrintHand():
    print("Dealer cards:")
    dealer.printCards()
    print("Total:",dealer.getTotal(),end="\n")
    return

def dealerTurn():
    inp = input('---Enter for dealer turn---')
    while (inp != ""):
        inp = input('---Please press enter for dealer turn---')
    while (dealer.getTotal() < 17):
        dealerPrintHand()
        print("Dealer hits")
        dealer.addCard(deck.drawCard())
        inp = input('---Please press enter to continue---')
        while (inp != ""):
            inp = input('---Please press enter for to continue---')
    dealerPrintHand()
    if (dealer.hasBlackjack()):
        print("Dealer has BLACKJACK!!")
    elif (dealer.isBusted()):
        print("Dealer busts!")
    else:
        print("Dealer stands")
    return


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
hitText = "HIT"
standText = "STAND"

hitButton = createTextButton(hitText, BLACK, STEEL_BLUE)
standButton = createTextButton(standText, BLACK, STEEL_BLUE)

hitButtonPos = ((WIDTH // 2) - hitButton.get_width() - CARD_SPACE, HEIGHT * 0.85)
standButtonPos = ((WIDTH // 2) + CARD_SPACE, HEIGHT * 0.85)

running = True
while running:
    # Area to display user's cards
    userCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
    userCardArea.fill(BACKGROUND_COLOUR)

    # Area to display dealer's cards
    dealerCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
    dealerCardArea.fill(BACKGROUND_COLOUR)

    # Initial message to user
    # announceText(initMessage, RED, None)
    
    # help button
    # TODO !!!

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
    # for card in dealer.cards:
    #     currCardImg = pygame.image.load(card.getCardImage())
    #     dealerCardArea.blit(currCardImg, (w, z))
    #     w += currCardImg.get_width() + CARD_SPACE
        
    # TO DISPLAY 1 FACEUP 1 FACEDOWN CARD
    currCardImg = pygame.image.load(dealer.cards[0].getCardImage())
    dealerCardArea.blit(currCardImg, (w, z))
    w += currCardImg.get_width() + CARD_SPACE
    currCardImg = pygame.image.load("blackjack/Images/cards/Card_Back.jpg") # FILL IN LATER
    dealerCardArea.blit(currCardImg, (w, z))
            
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
    dealerTotalText = cardTotalFont.render(("Total: ?"), True, BLACK, None)
    dealerTotalTextArea = dealerTotalText.get_rect()
    screen.blit(dealerTotalText, ((WIDTH // 2) - (dealerTotalTextArea.width // 2), (DEALER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    
    userTotalText = cardTotalFont.render(("Total: " + str(user.getTotal())), True, BLACK, None)
    userTotalTextArea = userTotalText.get_rect()
    screen.blit(userTotalText, ((WIDTH // 2) - (userTotalTextArea.width // 2), (USER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    pygame.display.update()
    
    # !!! refactor with helper method for the text stuff later
    
    # user turn
    if (user.hasBlackjack()):
        announceText("BLACKJACK!! Dealer's turn...", RED, None)
        playerTurn = dealer
    
    # dealer turn
    
    # ending screen
    

    # Add Button
    screen.blit(hitButton, hitButtonPos)
    screen.blit(standButton, standButtonPos)

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
            # User chooses to stand
            if standButtonPos[0] <= mouse[0] <= (standButtonPos[0] + standButton.get_width()) and standButtonPos[1] <= mouse[1] <= (standButtonPos[1] + standButton.get_height()):
                if (playerTurn == user):
                    userStands()
                    announceText("You stand. Dealer's turn...", RED, None)
                    # button2 = buttonClicked()
                    # screen.blit(button2, (600, 100))
            # User chooses to hit
            if hitButtonPos[0] <= mouse[0] <= (hitButtonPos[0] + hitButton.get_width()) and hitButtonPos[1] <= mouse[1] <= (hitButtonPos[1] + hitButton.get_height()):
                if (playerTurn == user):
                    userHits()
                    if (user.isBusted()):
                        announceText("YOU'RE BUSTED! Dealer's turn...", RED, None)
                        playerTurn = dealer
                    # button3 = buttonClicked()
                    # screen.blit(button3, (100, 100))
    pygame.display.update()


