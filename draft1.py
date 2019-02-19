import pygame
from Input import InputManager as im
im.__init__()
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

class __main__:

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

    def __init__(self):
        window = pygame.display.set_mode((350,500))
        window.fill((255,255,255))
        
        card = CardInfo('Inflict_Wounds.txt')

        colors = {'abjuration':(0,0,255),\
                  'conjuration':(255,125,0),\
                  'divination':(200,200,200),\
                  'enchantment':(255,255,0),\
                  'evocation':(255,0,0),\
                  'illusion':(255,0,255),\
                  'necromancy':(0,0,0),\
                  'transmutation':(0,255,0)}

        pygame.draw.rect(window,colors[card.info['school']],pygame.Rect(0,0,350,500),25)

        sfont = pygame.font.SysFont('Calibri',17)
        afont = pygame.font.SysFont('Calibri',73)
        bfont = pygame.font.SysFont('Calibri',26)

        lv = sfont.render(card.info['level']+' level',1,(0,0,0))
        name = sfont.render(card.info['name'],1,(0,0,0))
        page = sfont.render('PHB '+card.info['page'],1,(0,0,0))
        cast = sfont.render('Casting time: '+card.info['casting-time'],1,(0,0,0))
        rang = sfont.render('Range: '+card.info['range'],1,(0,0,0))
        dur = sfont.render('Duration: '+card.info['duration'],1,(0,0,0))
        dmg = afont.render(card.info['damage'],1,(0,0,0))
        typ = bfont.render(card.info['type'],1,(0,0,0))
        dsc = self.wrap(card.info['description'],290,sfont)
        hl = self.wrap(card.info['higher'],290,sfont)

        window.blit(lv,(30,30))
        window.blit(name,(175-name.get_width()/2,30))
        window.blit(page,(320-page.get_width(),30))
        window.blit(cast,(30,55))
        window.blit(rang,(30,75))
        window.blit(dur,(30,95))
        window.blit(dmg,(30,180))
        window.blit(typ,(190,215))
        window.blit(dsc,(30,260))
        window.blit(hl,(30,320))

        pygame.display.flip()

__main__()
