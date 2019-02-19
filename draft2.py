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
    def add(self,level,thing,x='LEFT',y='TOP'):
        if level >= len(self.elements):
            self.elements.append([(thing,x,y)])
        else:
            self.elements[level].append((thing,x,y))
            
    def draw(self,width=350):
        height = [i[0][0].get_height() for i in self.elements]
        height[4] += 30
        height[7] += 30
        
        card = pygame.Surface((width,sum(height)))
        card.fill((255,255,255))

        for i in range(0,len(self.elements)):
            for j in self.elements[i]:
                x = y = 0
                if j[1] == 'CENTER': x = (width-j[0].get_width())//2
                elif j[1] == 'RIGHT': x = width-j[0].get_width()
                if j[2] == 'CENTER': y = (height[i]-j[0].get_height())//2
                elif j[2] == 'BOTTOM': y = height[i]-j[0].get_height()
                card.blit(j[0],(x,sum(height[0:i])+y))
        return card
    
class Draw:
    @classmethod
    def getLevel(cls,school,level,font,d=80):
        a = pygame.image.load("schools.png").convert_alpha()
        a = pygame.transform.scale(a,(d*4,d*2))
        b = pygame.Surface((d,d))
        b.fill((255,255,255))
        b.blit(a,(0,0),(d*2,d,d,d))
        c = font.render(level,1,(0,0,0))
        b.blit(c,((d-c.get_width())//2,(d-c.get_height())//2))
        return b
    @classmethod
    def getRC(cls,r,c,d=60):#do this without images
        b = pygame.Surface((d*2,d))
        b.fill((255,255,255))
        b.set_colorkey((255,255,255))
        a = pygame.image.load('ritual.png').convert_alpha()
        a = pygame.transform.scale(a,(d,d))
        b.blit(a,(0,0))
        a = pygame.image.load('concentration.png').convert_alpha()
        a = pygame.transform.scale(a,(d,d))
        b.blit(a,(d,0))
        return b
    @classmethod
    def getComponents(cls,c,d=60):
        V = pygame.image.load('visual.png').convert_alpha()
        V = pygame.transform.scale(V,(d,d))
        S = pygame.image.load('sematic.png').convert_alpha()
        S = pygame.transform.scale(S,(d,d))
        M = pygame.image.load('material.png').convert_alpha()
        M = pygame.transform.scale(M,(d,d))
        b = pygame.Surface((3*d,d))
        b.fill((255,255,255))
        b.set_colorkey((255,255,255))
        b.blit(V,(0,0));b.blit(S,(d,0));b.blit(M,(d*2,0))
        return b
    
    @classmethod
    def visualize(cls,info):
        font_info = [('Calibri',17),('Calibri',73),('Calibri',26)]
        fonts = []
        for i in font_info:
            fonts.append(pygame.font.SysFont(i[0],i[1]))
        
        width = 350

        l = Layout()
        l.add(0,cls.getLevel(info['school'],info['level'],fonts[2]))
        l.add(0,cls.getText(info['name'],fonts[0]),'RIGHT')#idk, bigger and local center maybe
        l.add(1,cls.getText('Casting Time: '+info['casting-time'],fonts[0]))
        l.add(2,cls.getText('Range: '+info['range'],fonts[0]))
        l.add(3,cls.getText('Duration: '+info['duration'],fonts[0]))
        l.add(2,cls.getRC(info['ritual'],info['concentration']),'RIGHT','CENTER')
        l.add(4,cls.getComponents(info['components']),'CENTER','CENTER')#divider
        l.add(5,cls.getText(info['damage'],fonts[1]))
        l.add(5,cls.getText(info['type'],fonts[2]),'RIGHT','BOTTOM')#flush
        l.add(6,cls.wrap(info['description'],width,fonts[0]))
        l.add(7,cls.wrap(info['higher'],width,fonts[0]),'LEFT','CENTER')#bold
        l.add(8,cls.getText('PHB '+info['page'],fonts[0]),'RIGHT')
        
        return l.draw()

    @classmethod
    def wrap(cls,text,width,font):
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
    def getText(cls,text,font):
        return font.render(text,1,(0,0,0))
    
class __main__:

    def __init__(self):
        window = pygame.display.set_mode((350,600))
        window.fill((255,255,255))
        
        card = CardInfo('Inflict_Wounds.txt')
        fancy = Draw.visualize(card.info)
        window.blit(fancy,(0,0))
        pygame.display.flip()

__main__()