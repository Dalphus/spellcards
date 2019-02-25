import pygame
from pygame import gfxdraw
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
        height[1] += 10 #margin under spell level 
        height[4] += 30 #padding of components
        height[6] += 15 #margin below description
        height[8] += 30 #margin above PHB page
        
        card = pygame.Surface((width,sum(height)))
        card.fill((255,255,255))

        for i in range(0,len(self.elements)):
            for j in range(0,len(self.elements[i])):
                k = self.elements[i][j]
                x = y = 0
                if k[1] == 'FLUSH': x = self.elements[i][j-1][0].get_width()+10
                elif k[1] == 'CENTER': x = (width-k[0].get_width())//2
                elif k[1] == 'RIGHT': x = width-k[0].get_width()
                elif k[1] == 'RELATIVE':
                    x = (width+self.elements[i][j-1][0].get_width()-k[0].get_width())//2
                if k[2] == 'CENTER': y = (height[i]-k[0].get_height())//2
                elif k[2] == 'BOTTOM': y = height[i]-k[0].get_height()
                elif k[2] == 'OFFSET': y = height[i]-k[0].get_height()-12
                card.blit(k[0],(x,sum(height[0:i])+y))
        return card
    
class Draw:
    def __init__(self):
        self.schools = []
        self.colors = {}
        self.icons = {}

        #import colors and store school names
        f = open('colors.txt','r')
        for i in range(0,8):
            line = f.readline()
            x = line.find(':')
            self.schools.append(line[:x])
            c = tuple([int(j) for j in line[x+1:-1].split(' ')])+(0,)
            self.colors[self.schools[i]] = c
        f.close()

        #import and colorize school icons
        a = pygame.image.load("schools.png")
        for i in range(0,8):
            b = a.subsurface(pygame.Rect(400*(i%4),400*(i//4),400,400))
            b.fill(self.colors[self.schools[i]], None, pygame.BLEND_RGBA_ADD)
            b.set_colorkey((255,255,255))
            self.icons[self.schools[i]] = b

        d = 60
        font = pygame.font.SysFont('arielblack',32)
        self.CR = pygame.Surface((d*2+20,d))
        self.CR.fill((255,255,255,0))
        #draw concentration icon
        a = pygame.Surface((d,d))
        a.fill((255,255,255))
        pygame.draw.polygon(a,(0,0,0),((0,d/2),(d/2,d),(d,d/2),(d/2,0)))
        x,y = font.size('C')
        a.blit(font.render('C',1,(255,255,255)),((d-x)/2,(d-y)/2))
        self.CR.blit(a,(0,0))
        #draw ritual icon
        a = pygame.Surface((d,d))
        a.fill((255,255,255))
        pygame.draw.circle(a,(0,0,0),(d//2,d//2),d//2,7)
        x,y = font.size('R')
        a.blit(font.render('R',1,(0,0,0)),((d-x)/2,(d-y)/2))
        self.CR.blit(a,(d+10,0))
        
    def getLevel(self,school,level,font,d=80):
        b = self.icons[school].copy()
        b = pygame.transform.scale(b,(d,d))
        c = font.render(level,1,(0,0,0))
        b.blit(c,((d-c.get_width())//2,(d-c.get_height())//2))
        return b
    
    def getRC(self,rit,con,dim=(180,)*3):
        b = self.CR.copy()
        x,y = b.get_size()
        if rit == 'no':
            b.fill(dim,pygame.Rect(0,0,x//2,y),pygame.BLEND_ADD)
        if con == 'no':
            b.fill(dim,pygame.Rect(x//2,0,x//2,y),pygame.BLEND_ADD)
        return b
    
    def getComponents(self,com,d=60):
        b = pygame.Surface((d,d))
        return b
    
    def visualize(self,info):
        font_info = [('Calibri',17),('Calibri',73),('Calibri',26)]
        font_info.append(font_info[0])
        fonts = []
        for i in font_info:
            fonts.append(pygame.font.SysFont(i[0],i[1]))
        fonts[3].set_bold(True)
        
        width = 350

        l = Layout()
        l.add(0,self.getLevel(info['school'],info['level'],fonts[2]))
        l.add(0,self.getText(info['name'],fonts[0]),'RELATIVE','CENTER')#bigger
        l.add(1,self.getText('Casting Time: '+info['casting-time'],fonts[0]),y='BOTTOM')
        l.add(2,self.getText('Range: '+info['range'],fonts[0]))
        l.add(3,self.getText('Duration: '+info['duration'],fonts[0]))
        l.add(2,self.getRC(info['ritual'],info['concentration']),'RIGHT','CENTER')
        l.add(4,self.getComponents(info['components']),'CENTER','CENTER')#divider
        l.add(5,self.getText(info['damage'],fonts[1]))
        l.add(5,self.getText(info['type'],fonts[2]),'FLUSH','OFFSET')
        l.add(6,self.wrap(info['description'],width,fonts[0]))
        l.add(7,self.wrap(' '*34+info['higher'],width,fonts[0]),y='CENTER')
        l.add(7,self.getText('At Higher Levels:',fonts[3]))
        l.add(8,self.getText('PHB '+info['page']+' '*5,fonts[0]),'RIGHT','BOTTOM')
        
        return l.draw()

    
    def wrap(self,text,width,font):
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

    
    def getText(self,text,font):
        return font.render(text,1,(0,0,0),(255,255,255))
    
class __main__:

    def __init__(self):
        window = pygame.display.set_mode((350,600))
        window.fill((255,255,255))
        
        card = CardInfo('Inflict_Wounds.txt')
        draw = Draw()
        fancy = draw.visualize(card.info)
        window.blit(fancy,(0,0))
        pygame.display.flip()

        while True:
            im.manage_input()

__main__()
