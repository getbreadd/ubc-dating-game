import pygame
from blackjackPlayer import *
from blackjackDeck import *

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
comp = Player('Computer')

cardToAdd = deck.drawCard()
player.addCard(cardToAdd)
cardToAdd = deck.drawCard()
player.addCard(cardToAdd)
cardToAdd = deck.drawCard()
player.addCard(cardToAdd)
player.printCards()
total = player.getTotal()
print('total: ', total)
# for x in range(53):
#     card = deck.drawCard()
#     card.printCard()

running = True
while running:
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


