import pygame
from blackjackPlayer import *
from blackjackDeck import *

# helper methods
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

pygame.init()

width = 500;
height = 500;

GRAY = (110, 110, 110)
GREEN = (46, 112, 64)
LIGHT_GREEN = (117, 186, 117)

# initialize screen and display
screen = pygame.display.set_mode((width, height));
screen.fill(GREEN);
pygame.display.set_caption("It's time to gamble!")
pygame.display.flip();

# initialize deck and players
deck = Deck();
# deck.printCards();
player = Player('Name')
dealer = Player('Dealer')

dealerTurn()

# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# cardToAdd = deck.drawCard()
# player.addCard(cardToAdd)
# player.printCards()
# total = player.getTotal()
# print('total: ', total)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
            
            
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
    # pygame.display.update()
            



# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((255, 255, 255));

#     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

#     pygame.display.flip()
# pygame.quit()


