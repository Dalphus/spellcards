import pygame
from SpellCardStuff import *
from Input import InputManager as im
from Customize import StyleManager as sm
pygame.init()
im.__init__()
sm.__init__()

window = pygame.display.set_mode((350,600))

CardDraw.__init__(350)
CardDraw.updateCR()

content = CardInfo('Inflict_Wounds.txt')

while im.manage_input():
    for i in im.keydown():
        sm.update(i.key)
        
        style = CardLayout()
        CardDraw.width = sm.crunch[0]
        CardDraw.updateCR()
        CardDraw.addElements(style,content.info)
        
        window.fill((255,255,255))
        draw = style.visualize(sm.crunch[0])
        window.blit(draw,(0,0))
        pygame.display.flip()

pygame.display.quit()
pygame.quit()
