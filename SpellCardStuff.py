import pygame
from pygame import gfxdraw
pygame.init()

class CardInfo:
    def __init__(self,file):
        self.info = {}
        f = open(file,'r')
        for i in range(0,14):
            line = f.readline()
            x = line.find(':')
            self.info[line[:x]] = line[x+1:-1]
        f.close()

class CardLayout:
    def __init__(self):
        self.elements = [[]]
    def add(self,level,thing,x='LEFT',y='TOP'):
        if level >= len(self.elements):
            self.elements.append([(thing,x,y)])
        else:
            self.elements[level].append((thing,x,y))

    def visualize(self,width):
        height = [i[0][0].get_height() for i in self.elements]
        height[0] += 10 #margin under spell level 
        height[4] += 30 #padding of components
        height[6] += 15 #margin above description
        height[7] += 15 #margin above HL header
        height[9] += 30 #margin above PHB page
        
        b = pygame.Surface((width,sum(height)))
        b.fill((255,)*3)

        for i in range(0,len(self.elements)):
            for j in range(0,len(self.elements[i])):
                k = self.elements[i][j]
                x = y = 0
                if k[1] == 'FLUSH': x = self.elements[i][j-1][0].get_width()
                elif k[1] == 'CENTER': x = (width-k[0].get_width())//2
                elif k[1] == 'RIGHT': x = width-k[0].get_width()
                elif k[1] == 'RELATIVE':
                    x = (width+self.elements[i][j-1][0].get_width()-k[0].get_width())//2
                if k[2] == 'CENTER': y = (height[i]-k[0].get_height())//2
                elif k[2] == 'BOTTOM': y = height[i]-k[0].get_height()
                elif k[2] == 'OFFSET': y = height[i]-k[0].get_height()-12
                b.blit(k[0],(x,sum(height[0:i])+y))
        return b

class CardDraw:
    @classmethod
    def __init__(cls,width):
        cls.width = width
        cls.colors = {}
        cls.icons = {}
        cls.components = {}
        schools = []

        #import colors and store school names
        f = open('colors.txt','r')
        for i in range(0,8):
            line = f.readline()
            x = line.find(':')
            schools.append(line[:x])
            c = tuple([int(j) for j in line[x+1:-1].split(' ')])+(0,)
            cls.colors[schools[i]] = c
        f.close()

        #import and colorize school icons
        a = pygame.image.load('schools.png')
        for i in range(0,8):
            b = a.subsurface(pygame.Rect((i%4)*400,(i//4)*400,400,400))
            b.fill(cls.colors[schools[i]], None, pygame.BLEND_ADD)
            #b.set_colorkey((255,)*3)
            cls.icons[schools[i]] = b

        key = ['V','S','M']
        #import component icons
        a = pygame.image.load('components.png')
        for i in range(0,3):
            b = a.subsurface(pygame.Rect(i*100,0,100,100))
            cls.components[key[i]] = b

    @classmethod
    def updateCR(cls,d=55,font=None):
        if font == None:
            font = pygame.font.SysFont('arielblack',32)
        cls.CR = pygame.Surface((d*2+20,d))
        cls.CR.fill((255,)*3)
        #draw concentration icon
        a = pygame.Surface((d,d))
        a.fill((255,)*3)
        pygame.draw.polygon(a,(0,0,0),((0,d/2),(d/2,d),(d,d/2),(d/2,0)))
        x,y = font.size('C')
        a.blit(font.render('C',1,(255,)*3),((d-x)/2,(d-y)/2))
        cls.CR.blit(a,(0,0))
        #draw ritual icon
        a = pygame.Surface((d,d))
        a.fill((255,)*3)
        pygame.draw.circle(a,(0,0,0),(d//2,d//2),d//2,7)
        x,y = font.size('R')
        a.blit(font.render('R',1,(0,0,0)),((d-x)/2,(d-y)/2))
        cls.CR.blit(a,(d+10,0))
        
    @classmethod
    def getLevel(cls,school,level,font,d=80):
        b = pygame.transform.scale(cls.icons[school],(d,d))
        c = font.render(level,1,(0,0,0))
        b.blit(c,((d-c.get_width())//2,(d-c.get_height())//2))
        return b
    
    @classmethod
    def getRC(cls,rit,con,dim=(180,)*3):
        b = cls.CR.copy()
        x,y = b.get_size()
        if rit == 'no':
            b.fill(dim,pygame.Rect(0,0,x//2,y),pygame.BLEND_ADD)
        if con == 'no':
            b.fill(dim,pygame.Rect(x//2,0,x//2,y),pygame.BLEND_ADD)
        return b
    
    @classmethod
    def getComponents(cls,com,d=60):
        x = (cls.width-len(com)*d)//(len(com)+1)
        b = pygame.Surface((cls.width,d))
        b.fill((255,)*3)
        for i in range(0,len(com)):
            a = pygame.transform.scale(cls.components[com[i]],(d,d))
            b.blit(a,(x+i*(x+d),0))
        return b
    
    @classmethod
    def addElements(cls,l,info):
        #parse fonts (temporary)
        font_info = [('Calibri',17),('Calibri',73),('Calibri',26)]
        font_info.append(font_info[0])
        fonts = []
        for i in font_info:
            fonts.append(pygame.font.SysFont(i[0],i[1]))
        fonts[3].set_bold(True)

        l.add(0,cls.getLevel(info['school'],info['level'],fonts[2]))
        l.add(0,cls.getText(info['name'],fonts[0]),'RELATIVE','CENTER')#bigger
        l.add(1,cls.getText('Casting Time: '+info['casting-time'],fonts[0]))
        l.add(2,cls.getText('Range: '+info['range'],fonts[0]))
        l.add(3,cls.getText('Duration: '+info['duration'],fonts[0]))
        l.add(2,cls.getRC(info['ritual'],info['concentration']),'RIGHT','CENTER')
        l.add(4,cls.getComponents(info['components']),'CENTER','CENTER')
        l.add(5,cls.getText(info['damage'],fonts[1]))
        l.add(5,cls.getText(' '+info['type'],fonts[2]),'FLUSH','OFFSET')
        l.add(6,cls.getText(info['description'],fonts[0]),'LEFT','BOTTOM')
        l.add(7,cls.getText('At Higher Levels:',fonts[3]),'CENTER','BOTTOM')
        l.add(8,cls.getText(info['higher'],fonts[0]))
        l.add(9,cls.getText('PHB '+info['page']+' '*5,fonts[0]),'RIGHT','BOTTOM')

    @classmethod
    def getText(cls,text,font,d=0):
        if not d: d = cls.width
        words = [i+' ' for i in text.split(' ')]

        line = words[0]
        lines = []
        for i in words[1:]:
            if font.size(line+i[:-1])[0] > d:
                lines.append(line)
                line = i
            else: line += i
        lines.append(line)
        #return unwrapped text if below width
        if len(lines) == 1:
            return font.render(line,1,(0,0,0))

        height = font.size('Tg')[1]
        text_surface = pygame.Surface((d,len(lines)*height))
        text_surface.fill((255,)*3)
        text_surface.set_colorkey((255,)*3)

        for i in range(0,len(lines)):
            image = font.render(lines[i],1,(0,0,0))
            text_surface.blit(image,(0,i*height))
            
        return text_surface
