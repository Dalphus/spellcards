import pygame
from Input import InputManager as im

pygame.init()
im.__init__()

x = {'a':1,'b':2,'c':3}
print(x)
for i,j in x.items():
    j += 1
print(x)
