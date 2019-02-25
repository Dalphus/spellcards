import pygame
from SpellCardStuff import *
from Input import InputManager as im
from Customize import StyleManager as sm
pygame.init()
im.__init__()
sm.__init__()

window = pygame.display.set_mode((350,600))
window.fill((255,255,255))

CardDraw.__init__(350)
CardDraw.updateCR()

content = CardInfo('Inflict_Wounds.txt')
style = CardLayout()
CardDraw.addElements(style,content.info)

draw = style.visualize(350)
window.blit(draw,(0,0))
pygame.display.flip()

while im.manage_input():
    sm.update()

pygame.display.quit()
pygame.quit()
