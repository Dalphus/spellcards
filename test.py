import pygame,re
pygame.init()

t = 'A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar \
into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. \
A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It \
ignites flammable objects in the area that aren’t being worn or carried. A bright streak flashes from your pointing finger to a point \
you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered \
on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful \
one. The fire spreads around corners. It ignites flammable objects in the area that aren’t being worn or carried.'
ff = pygame.font.SysFont('Calibri',17)
boldfont = pygame.font.SysFont('Calibri',17,bold=True)

def getText(text,font,d=0,color=(0,0,0)):
    d = 370

    fonts = [font,boldfont]
    i=j=h=w=f = 0
    while j != -1:
        j = text[i:].find(' ')
        #check for bold
        if text[i] == '*': f = 1-f
        w += fonts[f].size(text[i:i+j-1])[0]
        if text[i+j-1] == '*': f = 1-f
        if w > d:
            h += 1
            w = 0
        else: i += j+1
        
    if h == 0: return font.render(text,1,color)
    h = (h+1)*font.size('Tg')[1]

    
    
    text_surface = pygame.Surface((d,h))
    return text_surface

window = pygame.display.set_mode((400,700))
window.fill((255,255,255))
window.blit(getText(t,ff),(15,15))
pygame.display.flip()
