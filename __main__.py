import pygame
from SpellCardStuff import *
from Input import InputManager as im
im.__init__()
pygame.init()

window = pygame.display.set_mode((350,600))
window.fill((255,255,255))

card = CardInfo('Inflict_Wounds.txt')
draw = CardDraw(350)
draw.updateCR()
draw.addElements(card.info)
fancy = draw.visualize()
window.blit(fancy,(0,0))
pygame.display.flip()

while True:
    im.manage_input()
