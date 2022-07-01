import pygame
from blackjackDeck import *

pygame.init()

GRAY = (110, 110, 110)

screen = pygame.display.set_mode([400, 400])
# screen.fill(GRAY)

# pygame.display.set_caption("TESTTT")

deck = Deck();
deck.printCards();

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((255, 255, 255));

#     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

#     pygame.display.flip()
# pygame.quit()

