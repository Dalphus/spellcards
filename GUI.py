import pygame
from Input import InputManager as im

class Button:
    def __init__(self,_rect,_action,_text,font,\
                 _colors = ((0,0,255),(50,50,255),(155,155,255))):
        self.rect = _rect
        self.action = _action
        self.colors = _colors
        self.hover = False
        
        self.text = _text
        self.label = font.render(_text,True,(255,100,0))
        self.text_pos = (self.rect.x+(self.rect.width-self.label.get_width())//2,\
                         self.rect.y+(self.rect.height-self.label.get_height())//2)
    
    def update(self):
        for e in im.mousemotion():
            self.hover = self.rect.collidepoint(e.pos)
        for e in im.mbup():
            if self.hover and e.button == 1:
                self.action()
    
    def draw(self,window=None):
        c = self.hover*(1+pygame.mouse.get_pressed()[0])
        pygame.draw.rect(window,self.colors[c],self.rect)
        window.blit(self.label,self.text_pos)

class Menu:
    def __init__(self,size=(512,512)):
        self.button_list = []
        self.menu_surface = pygame.Surface(size)
        self.menu_surface.set_colorkey((255,255,255))
        
    def add_buttons(self,*buttons):
        for b in buttons:
            self.button_list.append(b)

    def update(self):
        self.menu_surface.fill((255,255,255))
        for b in self.button_list:
            b.update()
            b.draw(self.menu_surface)
