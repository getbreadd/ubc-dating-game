import pygame
from PIL import Image
from blackjackPlayer import *
from blackjackDeck import *

pygame.init()

# ------------------------------- CONSTANTS -------------------------------

WIDTH = 1500
HEIGHT = 1000

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)
RED = pygame.Color("red")

# ------------------------------- INITIALIZE GAME STATS -------------------------------

# initialize deck and players
deck = Deck()
# deck.printCards();
user = Player('Name')
dealer = Player('Dealer')

# ------------------------------- GAME VARIABLES -------------------------------

playerTurn = user
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
screen.fill(GREEN)
pygame.display.set_caption("It's time to gamble!")
pygame.display.flip()


# =======================================================================================
# HELPER METHODS
# =======================================================================================

# ------------------------------- OTHER HELPER METHODS -------------------------------

# Change Announcer mesage
def announceText(msg, msgColour, bckgdColour):
    global announcer
    announcer = font.render(msg, True, msgColour, bckgdColour)
    screen.blit(announcer, announcerArea)
    pygame.display.update()

# ------------------------------- USER METHODS -------------------------------

# User takes a turn: hit or stand
# hit -> deal a card to user's hand
#     -> check value for busted -> busted? end turn : continue
# stand -> end turn
def userTurn():
    global playerTurn
    print("It's your turn!!")
    while(playerTurn == user):
        user.printCards()
        print("Total: " + str(user.getTotal()))
        choice = input("Would you like to hit or stand?: ")
        if (choice.casefold() == "hit"):
            newCard = deck.drawCard()
            user.addCard(newCard)
            if (user.getTotal() > 21):
                user.printCards()
                print("Total: " + str(user.getTotal()))
                print("You're busted! RIP")
                playerTurn = dealer
                return
        elif (choice.casefold() == "stand"):
            playerTurn = dealer
            return
        else:
            print("Not a valid response. Try again...if you want to live...")

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
    if (dealer.getTotal() > 21):
        print("Dealer busts!")
    else:
        print("Dealer stands")
    return


# ------------------------------- CONSOLE TESTING -------------------------------

userTurn()
dealerTurn()

#  ------------------------------- PYGAME -------------------------------

# running = True
# while running:
#     # Initial message to user
#     announceText(initMessage, RED, None)

#     # # For inlcuding images
#     # currCardImg = pygame.image.load('blackjack/Images/2C.jpg')
#     # screen.blit(currCardImg, (0, 0))

#     # User's turn
#     # pause = input("Press enter to continue...")
#     # announceText("IT'S YOUR TURN!! GIVE ME THAT MONEY", RED, None)
#     # userTurn()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#         # elif event.type = pygame.MOUSEBUTTONDOWN:
#     pygame.display.update()


