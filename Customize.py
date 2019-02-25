import pygame
from Input import InputManager as im

class StyleManager:
    @classmethod
    def __init__(cls):
        f = open('layout_attributes.txt')
        info = f.read().split('\n')
        f.close()
        heads = [info.index(':element offset:'),info.index(':crunch:')]

        cls.sfonts = pygame.font.get_fonts()
        cls.fonts = []
        for i in info[1:heads[0]]:
            a,b = i.split(' ')
            cls.fonts.append([a,int(b)])
        cls.fontindex = [cls.sfonts.index(i) for i,j in cls.fonts]

        cls.offset = []
        for i in info[heads[0]+1:heads[1]]:
            a,b = i.split(' ')
            cls.offset.append([int(a),int(b)])

        cls.crunch = []
        for i in info[heads[1]+1:]:
            cls.crunch.append(int(i))

        cls.modes = ['font','offset','crunch']
        cls.mode = 0
        cls.index = 0
        cls.keys = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,\
                pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]
        
    @classmethod
    def update(cls,key):
        x = y = 0
        for j in range(0,10):
            if key == cls.keys[j]:
                cls.index = j
                print('changing index:',cls.index)
        if key == pygame.K_LEFT:  x = -1
        elif key == pygame.K_RIGHT: x = 1
        elif key == pygame.K_UP:    y = 1
        elif key == pygame.K_DOWN:  y = -1
        elif key == pygame.K_SPACE:
            cls.mode = (cls.mode+1)%3
            print('mode:',cls.modes[cls.mode])
        elif key == pygame.K_RETURN:
            print('saving...')
            cls.save()

        if cls.mode == 0 and cls.index < len(cls.fonts):
            cls.fonts[cls.index][1] = abs(cls.fonts[cls.index][1]+x)
            cls.fontindex[cls.index] = (cls.fontindex[cls.index]+y)%len(cls.sfonts)
            cls.fonts[cls.index][0] = cls.sfonts[cls.fontindex[cls.index]]
            print(cls.fonts[cls.index])
        elif cls.mode == 1:
            cls.offset[cls.index][0] += x
            cls.offset[cls.index][1] += y
            print(cls.offset[cls.index])
        elif cls.mode == 2 and cls.index < len(cls.crunch):
            cls.crunch[cls.index] = abs(cls.crunch[cls.index]+x+y)
            print(cls.crunch)

    @classmethod
    def save(cls):
        print(cls.fonts,cls.offset,cls.crunch)
        f = open('layout_attributes.txt',w)
        f.write(':fonts:')
        for i in self.fonts:
            f.write(i[0]+' '+str(i[1]))
        f.write(':element offset:')
        for i in self.offset:
            f.write(str(i[0])+' '+str(i[1]))
        f.write(':crunch:')
        for i in self.crunch:
            f.write(str(i))
        f.close()
