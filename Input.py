import pygame,sys

class InputManager:
    @classmethod
    def __init__(cls):
        #holds all events to be filtered out
        #pygame.QUIT has to be last
        cls.index = (pygame.KEYDOWN,pygame.KEYUP,\
                      pygame.MOUSEMOTION,\
                      pygame.MOUSEBUTTONDOWN,\
                      pygame.MOUSEBUTTONUP,\
                      pygame.QUIT)
        cls.index_length = len(cls.index)-1

    @classmethod
    def manage_input(cls):
        if pygame.event.peek(pygame.QUIT):
            pygame.display.quit();pygame.quit();sys.exit()
        
        cls.filtered_input = [[],[],[],[],[]]
        for e in pygame.event.get():
            for i in range(0,cls.index_length):
                if e.type == cls.index[i]:
                    cls.filtered_input[i].append(e)
                    break
        
    #easy input retrieval. redundant yes, but convenient
    @classmethod
    def keydown(cls):
        return cls.filtered_input[0]
    @classmethod
    def keyup(cls):
        return cls.filtered_input[1]
    @classmethod
    def mousemotion(cls):
        return cls.filtered_input[2]
    @classmethod
    def mbdown(cls):
        return cls.filtered_input[3]
    @classmethod
    def mbup(cls):
        return cls.filtered_input[4]
