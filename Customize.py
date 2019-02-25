import pygame
from Input import InputManager as im

class StyleManager:
    @classmethod
    def __init__(cls):
        f = open('layout_attributes.txt')
        info = f.read().split('\n')
        f.close()

        cls.sfonts = pygame.font.get_fonts()
        cls.fonts = []
        for i in info[1:7]:
            a,b = i.split(' ')
            cls.fonts.append([a,int(b)])
        cls.fontindex = [cls.sfonts.index(i) for i,j in cls.fonts]

        cls.offset = []
        for i in info[8:18]:
            a,b = i.split(' ')
            cls.offset.append([int(a),int(b)])

        cls.crunch = []
        for i in info[19:21]:
            cls.crunch.append(int(i))

        cls.modes = ['font','offset','crunch']
        cls.mode = index = 0
        cls.keys = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,\
                pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]
        
    @classmethod
    def update(cls):
        x = y = 0
        for i in im.keydown():
            for j in range(0,10):
                if i.key == cls.keys[j]:
                    cls.index = j
                    print('changing index:',cls.index)
            if i.key == pygame.K_LEFT:  x = -1
            elif i.key == pygame.K_RIGHT: x = 1
            elif i.key == pygame.K_UP:    y = 1
            elif i.key == pygame.K_DOWN:  y = -1
            elif i.key == pygame.K_SPACE:
                cls.mode = (cls.mode+1)%3
                print('mode:',cls.modes[cls.mode])
            elif i.key == pygame.K_RETURN:
                print(cls.fonts,cls.offset,cls.crunch)
                #save settings

        if x != 0 or y != 0:
            if cls.mode == 0 and cls.index < 6:
                cls.fonts[cls.index][1] = abs(cls.fonts[cls.index][1]+x)
                cls.fontindex[cls.index] = (cls.fontindex[cls.index]+y)%len(cls.sfonts)
                cls.fonts[cls.index][0] = cls.sfonts[cls.fontindex[cls.index]]
            elif cls.mode == 1:
                cls.offset[cls.index][0] += x
                cls.offset[cls.index][1] += y
            elif cls.mode == 2 and cls.index < 2:
                cls.crunch[cls.index] = abs(cls.crunch[cls.index]+x+y)

