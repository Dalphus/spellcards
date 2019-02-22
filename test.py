import pygame
from Input import InputManager as im
from pygame import gfxdraw
pygame.init()
im.__init__()

window = pygame.display.set_mode((400,400))
window.fill((255,255,255))
pygame.display.flip()

size=50
index = 0
fonts = pygame.font.get_fonts()
fontSize = 35

while True:
    im.manage_input()

    for i in im.keydown():
        if i.key == pygame.K_LEFT and index > 0:
            index -= 1
        if i.key == pygame.K_RIGHT and index < len(fonts)-1:
            index += 1
        if i.key == pygame.K_UP:
            fontSize += 1
        if i.key == pygame.K_DOWN:
            fontSize -= 1
        
        window.fill((255,255,255))
        pygame.draw.polygon(window,(0,0,0),((0,size),(size,2*size),(2*size,size),(size,0)))
        pygame.draw.circle(window,(0,0,0),(150,50),47,8)
        pygame.gfxdraw.aacircle(window,150,50,47,(0,0,0))
        pygame.gfxdraw.aacircle(window,150,50,46,(0,0,0))
        pygame.gfxdraw.aacircle(window,150,50,40,(0,0,0))
        pygame.gfxdraw.aacircle(window,150,50,39,(0,0,0))
        
        font = pygame.font.SysFont(fonts[index],fontSize)
        print(fonts[index],fontSize)
        
        sizeC = tuple([(size*2-i)//2 for i in font.size('C')])
        sizeR = [(size*2-i)//2 for i in font.size('R')]
        sizeR = (sizeR[0]+100,sizeR[1])
        window.blit(font.render('C',1,(255,255,255)),sizeC)
        window.blit(font.render('R',1,(0,0,0)),sizeR)
    pygame.display.flip()

