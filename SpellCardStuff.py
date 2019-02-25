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
            
    def draw(self,width):
        height = [i[0][0].get_height() for i in self.elements]
        height[0] += 10 #margin under spell level 
        height[4] += 30 #padding of components
        height[6] += 15 #margin above description
        height[7] += 15 #margin above HL header
        height[9] += 30 #margin above PHB page
        
        card = pygame.Surface((width,sum(height)))
        card.fill((255,255,255))

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
                card.blit(k[0],(x,sum(height[0:i])+y))
        return card
    
class CardDraw:
    def __init__(self,width):
        self.width = width
        self.colors = {}
        self.icons = {}
        self.components = {}
        schools = []

        #import colors and store school names
        f = open('colors.txt','r')
        for i in range(0,8):
            line = f.readline()
            x = line.find(':')
            schools.append(line[:x])
            c = tuple([int(j) for j in line[x+1:-1].split(' ')])+(0,)
            self.colors[schools[i]] = c
        f.close()

        #import and colorize school icons
        a = pygame.image.load('schools.png')
        for i in range(0,8):
            b = a.subsurface(pygame.Rect((i%4)*400,(i//4)*400,400,400))
            b.fill(self.colors[schools[i]], None, pygame.BLEND_ADD)
            #b.set_colorkey((255,255,255))
            self.icons[schools[i]] = b

        key = ['V','S','M']
        #import component icons
        a = pygame.image.load('components.png')
        for i in range(0,3):
            b = a.subsurface(pygame.Rect(i*100,0,100,100))
            self.components[key[i]] = b

    def updateCR(self,d=50,font=None):
        if font == None:
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
        b = pygame.transform.scale(self.icons[school],(d,d))
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
        x = (self.width-len(com)*d)//(len(com)+1)
        b = pygame.Surface((self.width,d))
        b.fill((255,255,255))
        for i in range(0,len(com)):
            a = pygame.transform.scale(self.components[com[i]],(d,d))
            b.blit(a,(x+i*(x+d),0))
        return b
    
    def addElements(self,info):
        #parse fonts (temporary)
        font_info = [('Calibri',17),('Calibri',73),('Calibri',26)]
        font_info.append(font_info[0])
        fonts = []
        for i in font_info:
            fonts.append(pygame.font.SysFont(i[0],i[1]))
        fonts[3].set_bold(True)

        self.l = CardLayout()
        self.l.add(0,self.getLevel(info['school'],info['level'],fonts[2]))
        self.l.add(0,self.getText(info['name'],fonts[0]),'RELATIVE','CENTER')#bigger
        self.l.add(1,self.getText('Casting Time: '+info['casting-time'],fonts[0]))
        self.l.add(2,self.getText('Range: '+info['range'],fonts[0]))
        self.l.add(3,self.getText('Duration: '+info['duration'],fonts[0]))
        self.l.add(2,self.getRC(info['ritual'],info['concentration']),'RIGHT','CENTER')
        self.l.add(4,self.getComponents(info['components']),'CENTER','CENTER')#divider
        self.l.add(5,self.getText(info['damage'],fonts[1]))
        self.l.add(5,self.getText(' '+info['type'],fonts[2]),'FLUSH','OFFSET')
        self.l.add(6,self.getText(info['description'],fonts[0]),'LEFT','BOTTOM')
        self.l.add(7,self.getText('At Higher Levels:',fonts[3]),'CENTER','BOTTOM')
        self.l.add(8,self.getText(info['higher'],fonts[0]))
        self.l.add(9,self.getText('PHB '+info['page']+' '*5,fonts[0]),'RIGHT','BOTTOM')

    def visualize(self):
        return self.l.draw(self.width)

    def getText(self,text,font,d=0):
        if not d: d = self.width
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
        text_surface.fill((255,255,255))
        text_surface.set_colorkey((255,255,255))

        for i in range(0,len(lines)):
            image = font.render(lines[i],1,(0,0,0))
            text_surface.blit(image,(0,i*height))
            
        return text_surface
