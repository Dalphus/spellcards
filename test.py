import pygame,re
pygame.init()

f = open('test.txt','r')
text = f.read()
f.close

d = 320
lines = []
for i in text.split('\n'):
    x = re.split('\*[^\*]*\*',i)
    lines.append(x)
    for j in x:
        print(j)
