import pygame
from SpellCardStuff import *
from Input import InputManager as im
#from GUI import *
pygame.init()
im.__init__()

width = 450

CardDraw.__init__(width-60)
content = CardInfo('Fireball.txt')

style = CardLayout()
CardDraw.addElements(style,content.info)
draw = style.visualize(width-60)

height = draw.get_height()+30
window = pygame.display.set_mode((width,height))
window.fill(CardDraw.colors[content.info['school']])
window.blit(draw,(15,15))
pygame.display.flip()

while im.manage_input(): pass

pygame.image.save(window,'Fireball.jpeg')
pygame.display.quit()
pygame.quit



