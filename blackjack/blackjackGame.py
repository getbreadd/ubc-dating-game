import pygame
from PIL import Image
from blackjackPlayer import *
from blackjackDeck import *

pygame.init()

WIDTH = 1500
HEIGHT = 1000

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)
RED = pygame.Color("red")

# initialize screen and display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(GREEN)
pygame.display.set_caption("It's time to gamble!")
pygame.display.flip()

# initialize deck and players
deck = Deck()
# deck.printCards();
user = Player('Name')
dealer = Player('Computer')

# Game Variables
playerTurn = user
initMessage = "LET'S GIVE AWAY ALL YOUR MONEYYYYY ^ - ^"
font = pygame.font.Font('freesansbold.ttf', 32)
announcer = font.render(initMessage, True, RED, None)
announcerArea = announcer.get_rect()
announcerArea.center = (WIDTH // 2, HEIGHT // 10)

cardToAdd = deck.drawCard()
user.addCard(cardToAdd)
cardToAdd = deck.drawCard()
user.addCard(cardToAdd)
cardToAdd = deck.drawCard()
user.addCard(cardToAdd)
user.printCards()
total = user.getTotal()
print('total: ', total)
# for x in range(53):
#     card = deck.drawCard()
#     card.printCard()


# =======================================================================================
# HELPER METHODS
# =======================================================================================

# Change Announcer mesage
def announceText(msg, msgColour, bckgdColour):
    global announcer
    announcer = font.render(msg, True, msgColour, bckgdColour)
    screen.blit(announcer, announcerArea)
    pygame.display.update()

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



running = True
while running:
    # Initial message to user
    announceText(initMessage, RED, None)

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
        
    # JUST TRYING STUFF OUT
    
    # font = pygame.font.SysFont('Corbel', 35)
    # text = font.render('?', True, (0, 0, 0))
    # bottom_right = ((width * 0.90), (height * 0.90))
    # radius = 15
    # pygame.draw.circle(screen, LIGHT_GREEN, bottom_right, radius )
    # screen.blit(text, bottom_right)
    # pygame.display.update()

    # mouse = pygame.mouse.get_pos()
    # if bottom_right[0] + 2 * radius > mouse[0] > bottom_right[0] and bottom_right[1] + 2 * radius > mouse[1] > bottom_right[1]:
    #     pygame.draw.circle(screen, (0, 0, 0), bottom_right, radius)
    # else:
    #     pygame.draw.circle(screen, LIGHT_GREEN, bottom_right, radius)
    # pygame.display.update()
    
    # pygame.draw.circle(screen, LIGHT_GREEN, bottom_right, radius)
    pygame.display.update()
            



# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((255, 255, 255));

#     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

#     pygame.display.flip()
# pygame.quit()


