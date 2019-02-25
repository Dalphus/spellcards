class Layout:
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

class LayoutManager:
    def __init__():
        f = open('layout_attributes.txt')
        info = f.read().split('\n')
        f.close()

        sfonts = pygame.font.get_fonts()
        fonts = []
        for i in info[1:7]:
            a,b = i.split(' ')
            fonts.append([a,int(b)])
        fontindex = [sfonts.index(i) for i,j in fonts]

        offset = []
        for i in info[8:18]:
            a,b = i.split(' ')
            offset.append([int(a),int(b)])

        crunch = []
        for i in info[19:21]:
            crunch.append(int(i))

        modes = ['font','offset','crunch']
        mode = index = 0
        keys = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,\
                pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]
    def update():
        x = y = 0
        for i in im.keydown():
            for j in range(0,10):
                if i.key == keys[j]:
                    index = j
                    print('changing index:',index)
            if i.key == pygame.K_LEFT:  x = -1
            elif i.key == pygame.K_RIGHT: x = 1
            elif i.key == pygame.K_UP:    y = 1
            elif i.key == pygame.K_DOWN:  y = -1
            elif i.key == pygame.K_SPACE:
                mode = (mode+1)%3
                print('mode:',modes[mode])
            elif i.key == pygame.K_RETURN:
                print(fonts,offset,crunch)

        if x != 0 or y != 0:
            if mode == 0 and index < 6:
                fonts[index][1] = abs(fonts[index][1]+x)
                fontindex[index] = (fontindex[index]+y)%len(sfonts)
                fonts[index][0] = sfonts[fontindex[index]]
                print(fonts[index])
            elif mode == 1:
                offset[index][0] += x
                offset[index][1] += y
                print(offset[index])
            elif mode == 2 and index < 2:
                crunch[index] = abs(crunch[index]+x+y)
                print(crunch)

