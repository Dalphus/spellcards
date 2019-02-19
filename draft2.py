import pygame
from Input import InputManager as im
im.__init__()
pygame.init()

width = 350

class CardInfo:
    def __init__(self,file):
        self.info = {}
        f = open(file,'r')
        for i in range(0,14):
            line = f.readline()
            x = line.find(':')
            self.info[line[:x]] = line[x+1:-1]
        f.close()
        
class Layout:
    def __init__(self):
        self.elements = [[]]
        maxLevel = 0
    def add(self,level,thing,mode,space=(1,1)):
        if level > maxLevel:
            maxLevel += 1
            self.elements.append([(thing,mode,space)])
        else:
            self.elements[level].append((thing,mode,space))
    def draw(self):
        padding = 30
        size = (350,500)
        color = (0,0,0)
        x = pygame.Surface(size)
        x.fill((255,255,255))

        for i in self.elements:
            for j in i:
                j.drawOn(x)

        return x
class Draw:
    @classmethod
    def visualize(cls,info):
        
        font_info = [('Calibri',17),('Calibri',73),('Calibri',26)]
        fonts = []
        for i in font_info:
            fonts.append(pygame.font.SysFont(i[0],i[1]))
        
        color = (0,0,0)
        size = (350,500)
        
        a = cls.wrap(info['description'],size[0]-60,fonts[0])
        b = cls.wrap(info['higher'],size[0]-60,fonts[0])

        #surface
        card_surface = pygame.Surface(size)
        card_surface.fill((255,255,255))
        #border
        pygame.draw.rect(card_surface,color,pygame.Rect(0,0,size[0],size[1]),25)
        #level
        pygame.draw.circle(card_surface,(255,255,255),(35,35),40)
        pygame.draw.circle(card_surface,color,(35,35),45,12)
        c = fonts[2].render(info['level'],1,(0,0,0))
        card_surface.blit(c,(35-c.get_width()/2,35-c.get_height()/2))
        #name
        c = fonts[0].render(info['name'],1,(0,0,0))
        card_surface.blit(c,(size[0]/2-c.get_width()/2,30))
        #PHB
        c = fonts[0].render('PHB '+info['page'],1,(0,0,0))
        card_surface.blit(c,(size[0]-30-c.get_width(),30))
        #casting times
        c = fonts[0].render('Casting time: '+info['casting-time'],1,(0,0,0))
        card_surface.blit(c,(30,55))
        #range
        c = fonts[0].render('Range: '+info['range'],1,(0,0,0))
        card_surface.blit(c,(30,75))
        #duration
        c = fonts[0].render('Duration: '+info['duration'],1,(0,0,0))
        card_surface.blit(c,(30,95))
        #damage
        c = fonts[1].render(info['damage'],1,(0,0,0))
        card_surface.blit(c,(30,180))
        #type
        c = fonts[2].render(info['type'],1,(0,0,0))
        card_surface.blit(c,(190,215))

        card_surface.blit(a,(30,260))
        card_surface.blit(b,(30,320))
        
        return card_surface

    @classmethod
    def wrap(csl,text,width,font):
        words = [i+' ' for i in text.split(' ')]

        line = words[0]
        lines = []
        for i in words[1:]:
            if font.size(line+i[:-1])[0] > width:
                lines.append(line)
                line = i
            else: line += i
        lines.append(line)

        height = font.size('Tg')[1]
        text_surface = pygame.Surface((width,len(lines)*height))
        text_surface.fill((255,255,255))

        for i in range(0,len(lines)):
            image = font.render(lines[i],1,(0,0,0))
            text_surface.blit(image,(0,i*height))
            
        return text_surface

    @classmethod
    def outline(rect):
        pass
    
class __main__:

    def __init__(self):
        window = pygame.display.set_mode((350,600))
        window.fill((255,255,255))
        
        card = CardInfo('Inflict_Wounds.txt')
        fancy = Draw.visualize(card.info)
        window.blit(fancy,(0,0))
        pygame.display.flip()

__main__()
