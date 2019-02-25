import pygame
from Input import InputManager as im

pygame.init()
im.__init__()

window = pygame.display.set_mode((500,500))
window.fill((255,255,255))
pygame.display.flip()

size=500

schools = []
colors = {}
f = open('colors.txt','r')
for i in range(0,8):
    line = f.readline()
    x = line.find(':')
    schools.append(line[:x])
    c = tuple([int(j) for j in line[x+1:-1].split(' ')])+(0,)
    colors[schools[i]] = c
f.close()

icons = {}
a = pygame.image.load("schools2.png")
a = pygame.transform.scale(a,(size*4,size*2))
for i in range(0,8):
    b = a.subsurface(pygame.Rect(size*(i%4),size*(i//4),size,size))
    b.fill(colors[schools[i]], None, pygame.BLEND_RGBA_ADD)
    b.set_colorkey((255,255,255))
    icons[schools[i]] = b

index = 0
while True:
    im.manage_input()

    for i in im.keydown():
        if i.key == pygame.K_LEFT and index > 0:
            index -= 1
        if i.key == pygame.K_RIGHT and index < 7:
            index += 1
        window.fill((255,255,255))
        window.blit(icons[schools[index]],(0,0))
            
    pygame.display.flip()

