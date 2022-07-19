from logging import setLogRecordFactory
from venv import create
import pygame
# from PIL import Image
from blackjackPlayer import *
from blackjackDeck import *

pygame.init()

# ------------------------------- CONSTANTS -------------------------------

WIDTH = 1000
HEIGHT = 700
USER_WIDTH = WIDTH // 2
USER_HEIGHT = HEIGHT // 4

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)
RED = pygame.Color("red")

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
font = pygame.font.Font('freesansbold.ttf', 32)
announcer = font.render(initMessage, True, RED, None)
announcerArea = announcer.get_rect()
announcerArea.center = (WIDTH // 2, HEIGHT // 10)

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
    announcer = font.render(msg, True, msgColour, bckgdColour)
    screen.blit(announcer, announcerArea)
    pygame.display.update()

def createTextButton(msg, msgColour, bckgdColour):
    text = font.render(msg, True, msgColour, None)
    buttonSurface = pygame.surface.Surface((text.get_width(), text.get_height()))
    buttonSurface.fill(bckgdColour)
    buttonSurface.blit(text, (0, 0))
    return buttonSurface

def createImageButton(img, bckgdColour):
    buttonSurface = pygame.surface.Surface((img.get_width(), img.get_height()))
    buttonSurface.fill(bckgdColour)
    buttonSurface.blit(img, (0, 0))
    return buttonSurface


# ------------------------------- OTHER GAME HELPER METHODS -------------------------------

# User to place the bet amount
def placeBet():
    global betAmount
    betAmount = int(input("How many hearts would you like to bet?: "))

def initHands():
    user.addCard(deck.drawCard())
    user.addCard(deck.drawCard())
    dealer.addCard(deck.drawCard())
    print("Starting cards:")
    user.printCards()
    dealer.printCards()
    dealer.addCard(deck.drawCard())

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

# Area to display user's cards
userCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
userCardArea.fill(BACKGROUND_COLOUR)

running = True
while running:
    # Initial message to user
    announceText(initMessage, RED, None)

    # Position cards in center no matter amount of cards
    (x, y) = ((1 / 2) * (USER_WIDTH - (user.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (user.getNumCards() - 1))), 0)
    for card in user.cards:
        currCardImg = pygame.image.load(card.getCardImage())
        userCardArea.blit(currCardImg, (x, y))
        x += currCardImg.get_width() + CARD_SPACE
        button1 = createImageButton(currCardImg, RED)
        screen.blit(button1, (0, 0))

    screen.blit(userCardArea, (WIDTH //4, HEIGHT * 0.75))

    # Add Button
    # button1 = createTextButton("CLICK ME NOWWW!!!", pygame.Color("White"), RED)
    # screen.blit(button1, (0, 0))


    # # For inlcuding images
    # currCardImg = pygame.image.load('blackjack/Images/2C.jpg')
    # screen.blit(currCardImg, (0, 0))

    # User's turn
    # pause = input("Press enter to continue...")
    # announceText("IT'S YOUR TURN!! GIVE ME THAT MONEY", RED, None)
    # userTurn()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            img = pygame.image.load("blackjack/Images/cards/AS.jpg")
            button2 = createImageButton(img, RED)
            screen.blit(button2, (0, 0))
    pygame.display.update()


