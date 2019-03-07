import pygame,os
from SpellCardStuff import *
pygame.init()

width = 470
CardDraw.__init__(width-60)

for filename in os.listdir('SpellData'):
    name = filename[:filename.rfind('.')]
    content = CardInfo('SpellData/'+name+'.txt')

    style = CardLayout()
    CardDraw.addElements(style,content.info)
    fancy = style.visualize(width-60)

    card = pygame.Surface((width,fancy.get_height()+30))
    card.fill(CardDraw.colors[content.info['school']])
    card.blit(fancy,(15,15))

    pygame.image.save(card,name+'.jpeg')

pygame.quit()
