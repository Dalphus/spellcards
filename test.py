

info = {}
f = open('Inflict_Wounds.txt','r')
lines = f.read().split(':')
f.close()

x = lines[0].rfind('\n')
for i in range(1,len(lines)):
    name = lines[i-1][x+1:]
    x = lines[i].rfind('\n')
    info[name] = lines[i][:x]

print(info)

