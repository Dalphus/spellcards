import pygame
from SpellCardStuff import *
from Input import InputManager as im
from Customize import StyleManager as sm
pygame.init()
im.__init__()
sm.__init__()

window = pygame.display.set_mode((380,600))

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
        
        window.fill(CardDraw.colors[content.info['school']])
        draw = style.visualize(sm.crunch[0])
        window.blit(draw,(15,15))
        pygame.display.flip()

pygame.image.save(window,'Inflict_Wounds.jpeg')
pygame.display.quit()
pygame.quit()
