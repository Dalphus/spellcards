import pygame
from pygame import gfxdraw
pygame.init()

class CardInfo:
    def __init__(self,file):
        self.info = {}
        f = open(file,'r')
        lines = f.read().split(':')
        f.close()

        x = lines[0].rfind('\n')
        for i in range(1,len(lines)):
            name = lines[i-1][x+1:]
            x = lines[i].rfind('\n')
            self.info[name] = lines[i][:x]

class CardLayout:
    def __init__(self):
        self.elements = [[]]
    def add(self,level,thing,x='LEFT',y='TOP'):
        if level >= len(self.elements):
            self.elements.append([(thing,x,y)])
        else:
            self.elements[level].append((thing,x,y))

    def visualize(self,width,padding=15):
        height = [i[0][0].get_height() for i in self.elements]
        height[0] += 10 #margin under spell level 
        height[4] += 15 #margin above components
        height[5] = 15 #remove height of materials
        height[7] += 10 #margin above description
        height[8] += 15 #margin above HL header
        height[10] += 30 #margin above PHB page
        
        a = pygame.Surface((width,sum(height)))
        a.fill((255,)*3)

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
                elif k[2] == 'OFFSET': y = height[i]-k[0].get_height()-9
                a.blit(k[0],(x,sum(height[0:i])+y))
                
        b = pygame.Surface((width+2*padding,sum(height)+2*padding))
        b.fill((255,)*3)
        b.blit(a,(padding,padding))
        return b

class CardDraw:
    @classmethod
    def __init__(cls,width):
        cls.width = width
        cls.colors = {}
        cls.icons = {}
        cls.components = {}
        cls.fonts = []

        #import fonts
        f = [('Cambriab',34),('Nodesto Caps Condensed Bold',45),\
             ('Corbel',19),('Arial Black',34),('Cambriab',65),\
             ('Corbel',30),('Corbel Bold',22),('Corbel Italic',17),\
             ('Corbel Bold Italic',19)]
        for i in f:
            font = pygame.font.Font('fonts/'+i[0]+'.ttf',i[1])
            cls.fonts.append(font)
        
        #import and colorize school icons
        a = pygame.image.load('schools.png')
        f = open('colors.txt','r')
        for i in range(0,8):
            line = f.readline()
            x = line.split(':')
            c = tuple([int(j) for j in x[1].split(' ')])+(0,)
            cls.colors[x[0]] = c

            b = a.subsurface(pygame.Rect((i%4)*400,(i//4)*400,400,400))
            b.fill(cls.colors[x[0]], None, pygame.BLEND_ADD)
            cls.icons[x[0]] = b
        f.close()

        key = ['V','S','M']
        #import component icons
        a = pygame.image.load('components.png')
        for i in range(0,3):
            b = a.subsurface(pygame.Rect(i*200,0,200,200))
            cls.components[key[i]] = b

        #draw concentration and ritual icons
        d = 58
        cls.CR = pygame.Surface((d*2+20,d))
        cls.CR.fill((255,)*3)
        #concentration
        a = pygame.Surface((d,d))
        a.fill((255,)*3)
        pygame.draw.polygon(a,(0,0,0),((0,d/2),(d/2,d),(d,d/2),(d/2,0)))
        x,y = cls.fonts[3].size('C')
        a.blit(cls.fonts[3].render('C',1,(255,)*3),((d-x)/2,(d-y)/2))
        cls.CR.blit(a,(0,0))
        #ritual
        a = pygame.Surface((d,d))
        a.fill((255,)*3)
        pygame.draw.circle(a,(0,0,0),(d//2,d//2),d//2,7)
        x,y = cls.fonts[3].size('R')
        a.blit(cls.fonts[3].render('R',1,(0,0,0)),((d-x)/2,(d-y)/2))
        cls.CR.blit(a,(d+10,0))
        
    @classmethod
    def getLevel(cls,school,level,font,d=100):
        b = pygame.transform.scale(cls.icons[school],(d,d))
        c = font.render(level,1,(0,0,0))
        b.blit(c,((d-c.get_width())//2,(d-c.get_height())//2))
        return b
    
    @classmethod
    def getCR(cls,rit,con,dim=(220,)*3):
        b = cls.CR.copy()
        x,y = b.get_size()
        if rit == 'no':
            b.fill(dim,pygame.Rect(0,0,x//2,y),pygame.BLEND_ADD)
        if con == 'no':
            b.fill(dim,pygame.Rect(x//2,0,x//2,y),pygame.BLEND_ADD)
        return b
    
    @classmethod
    def getComponents(cls,com,d = 75):
        x = (cls.width-len(com)*d)//(len(com)+1)
        b = pygame.Surface((cls.width,d))
        b.fill((255,)*3)
        for i in range(0,len(com)):
            a = pygame.transform.scale(cls.components[com[i]],(d,d))
            b.blit(a,(x+i*(x+d),0))
        
        return b
    
    @classmethod
    def addElements(cls,l,info):
        l.add(0,cls.getLevel(info['school'],info['level'],cls.fonts[0]))
        l.add(0,cls.getText(info['name'],cls.fonts[1],100),'RELATIVE','CENTER')
        l.add(1,cls.getText('Casting Time: '+info['casting-time'],cls.fonts[2]))
        l.add(2,cls.getText('Range: '+info['range'],cls.fonts[2]))
        l.add(3,cls.getText('Duration: '+info['duration'],cls.fonts[2]))
        l.add(2,cls.getCR(info['ritual'],info['concentration']),'RIGHT','CENTER')
        l.add(4,cls.getComponents(info['components']),'CENTER','BOTTOM')
        l.add(5,cls.getText(info['materials'],cls.fonts[7],0,(180,)*3),'RIGHT','TOP')
        l.add(6,cls.getText(info['damage'],cls.fonts[4]))
        l.add(6,cls.getText(' '+info['type'],cls.fonts[5]),'FLUSH','OFFSET')
        l.add(7,cls.getText(info['description'],cls.fonts[2],15),'CENTER','BOTTOM')
        l.add(8,cls.getText('At Higher Levels:',cls.fonts[6]),'CENTER','BOTTOM')
        l.add(9,cls.getText(info['higher'],cls.fonts[2],15),'CENTER')
        l.add(10,cls.getText('PHB '+info['page'],cls.fonts[7]),'RIGHT','BOTTOM')

    @classmethod
    def getText(cls,text,font,d=0,color=(0,0,0)):
        d = cls.width-d
        lines = []
        i = 0
        while text[i:]:
            if text[i] == '\n':
                lines.append(text[:i])
                text = ' '*5+text[i+1:]
                i = 0
            elif font.size(text[:i].strip('*'))[0] > d:
                x = text[:i].rfind(' ')
                lines.append(text[:x])
                text = text[x+1:]
                i = -1
            i += 1
        lines.append(text)
        #return unwrapped text if below width
        if len(lines) == 1:
            return font.render(text,1,color)
            
        height = font.size('Tg')[1]
        text_surface = pygame.Surface((d,len(lines)*height))
        text_surface.fill((255,)*3)
        text_surface.set_colorkey((255,)*3)

        temp = 0
        f = [font,cls.fonts[8]]
        for i in range(0,len(lines)):
            x = 0
            bold = lines[i].split('*')
            for j in bold:
                image = f[temp].render(j,1,color)
                text_surface.blit(image,(x,i*height))
                x += font.size(j)[0]
                temp = 1-temp
            temp = 0
            
        return text_surface
