import pygame
pygame.init()

def getText(text,font,width=350,color=(0,0,0)):
    lines = []
    i = 0
    while text[i:]:
        if text[i] == '\n':
            lines.append(text[:i])
            text = ' '*5+text[i+1:]
            i = 0
        elif font.size(text[:i].strip('*'))[0] > width:
            x = text[:i].rfind(' ')
            lines.append(text[:x])
            text = text[x+1:]
            i = -1
        i += 1
    lines.append(text)
    #return unwrapped text if below width
    if len(lines) == 1:
        return font.render(line,1,color)
        
    height = font.size('Tg')[1]
    text_surface = pygame.Surface((width,len(lines)*height))
    text_surface.fill((255,)*3)
    text_surface.set_colorkey((255,)*3)

    for i in range(0,len(lines)):
        bold = lines[i].split('*')
        x = 0
        for j in bold:
            image = font.render(j,1,color)
            text_surface.blit(image,(x,i*height))
            x += font.size(j)[0]
            font.set_bold(not font.get_bold())
            font.set_italic(not font.get_italic())
        font.set_bold(False)
        font.set_italic(False)
        
    return text_surface

f = open('test.txt','r')
x = f.read()
f.close()
image = getText(x,pygame.font.SysFont('corbel',17))

window = pygame.display.set_mode((380,500))
window.fill((255,)*3)
window.blit(image,(15,15))
pygame.display.flip()

pygame.image.save(window,'test.')
