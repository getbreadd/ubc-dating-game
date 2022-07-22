from logging import setLogRecordFactory
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
USER_WIDTH = WIDTH // 2
USER_HEIGHT = HEIGHT // 4
DEALER_CARD_COORDS = (WIDTH //4, HEIGHT * 0.25)
USER_CARD_COORDS = (WIDTH //4, HEIGHT * 0.60)
CARD_HEIGHT = pygame.image.load("blackjack/Images/cards/2C.jpg").get_height()
CARD_WIDTH = pygame.image.load("blackjack/Images/cards/2C.jpg").get_width()

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)
RED = pygame.Color("red")
BLACK = pygame.Color("black")

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

# ------------------------------- OTHER HELPER METHODS -------------------------------

# Change Announcer mesage
def announceText(msg, msgColour, bckgdColour):
    global announcer
    announcer = font.render(msg, True, msgColour, bckgdColour)
    screen.blit(announcer, announcerArea)
    pygame.display.update()

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

# Area to display dealer's cards
dealerCardArea = pygame.surface.Surface((USER_WIDTH, USER_HEIGHT))
dealerCardArea.fill(BACKGROUND_COLOUR)

running = True
while running:
    # Initial message to user
    announceText(initMessage, RED, None)
    
    # help button
    # TODO !!!

    # Position cards in center no matter amount of cards
    (x, y) = ((1 / 2) * (USER_WIDTH - (user.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (user.getNumCards() - 1))), 0)
    for card in user.cards:
        currCardImg = pygame.image.load(card.getCardImage())
        # currCardImg = pygame.transform.scale(currCardImg, ((HEIGHT // 7), (WIDTH // 7)))  # resize test
        userCardArea.blit(currCardImg, (x, y))
        x += currCardImg.get_width() + CARD_SPACE

    screen.blit(userCardArea, USER_CARD_COORDS)
    
    # Position initial dealer cards
    (w, z) = ((1 / 2) * (USER_WIDTH - (dealer.getNumCards() * CARD_WIDTH) - (CARD_SPACE * (dealer.getNumCards() - 1))), 0)
    for card in dealer.cards:
        currCardImg = pygame.image.load(card.getCardImage())
        dealerCardArea.blit(currCardImg, (w, z))
        w += currCardImg.get_width() + CARD_SPACE
        
    # TO DISPLAY 1 FACEUP 1 FACEDOWN CARD
    # currCardImg = pygame.image.load(dealer.cards[0].getCardImage())
    # dealerCardArea.blit(currCardImg, (w, z))
    # w += currCardImg.get_width() + CARD_SPACE
    # currCardImg = pygame.image.load("blackjack/Images/cards/FACEDOWNCARD.jpg") # FILL IN LATER
    # dealerCardArea.blit(currCardImg, (w, z))
            
    screen.blit(dealerCardArea, DEALER_CARD_COORDS)
    
    # Position the "Dealer's Cards" and "User's Cards" text
    dealerCardText = smallFont.render("Dealer's Cards", True, BLACK, None)
    dealerCardTextArea = dealerCardText.get_rect()
    screen.blit(dealerCardText, ((WIDTH // 2) - (dealerCardTextArea.width // 2), (DEALER_CARD_COORDS[1] - dealerCardTextArea.height - 10)))
    
    userCardText = smallFont.render("Your Cards", True, BLACK, None)
    userCardTextArea = userCardText.get_rect()
    screen.blit(userCardText, ((WIDTH // 2) - (userCardTextArea.width // 2), (USER_CARD_COORDS[1] - userCardTextArea.height - 10)))
    
    # Position the "Dealer Total" and "Your total" text
    dealerTotalText = cardTotalFont.render(("Total: " + str(dealer.getTotal())), True, BLACK, None)
    dealerTotalTextArea = dealerTotalText.get_rect()
    screen.blit(dealerTotalText, ((WIDTH // 2) - (dealerTotalTextArea.width // 2), (DEALER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    
    userTotalText = cardTotalFont.render(("Total: " + str(user.getTotal())), True, BLACK, None)
    userTotalTextArea = userTotalText.get_rect()
    screen.blit(userTotalText, ((WIDTH // 2) - (userTotalTextArea.width // 2), (USER_CARD_COORDS[1] + CARD_HEIGHT + 10)))
    pygame.display.update()
    
    # !!! refactor with helper method for the text stuff later
    
    # user turn
    
    # dealer turn
    
    # ending screen
    


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
        # elif event.type = pygame.MOUSEBUTTONDOWN:
    pygame.display.update()


