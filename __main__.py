import pygame
from SpellCardStuff import *
from Input import InputManager as im

pygame.init()
im.__init__()

width = 450
name = 'Fireball'

CardDraw.__init__(width-60)
content = CardInfo(name+'.txt')

style = CardLayout()
CardDraw.addElements(style,content.info)
draw = style.visualize(width-60)

height = draw.get_height()+30
window = pygame.display.set_mode((width,height))
window.fill(CardDraw.colors[content.info['school']])
window.blit(draw,(15,15))
pygame.display.flip()

while im.manage_input(): pass

pygame.image.save(window,name+'.jpeg')
pygame.display.quit()
pygame.quit

