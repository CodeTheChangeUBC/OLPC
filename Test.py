from Block import Block

bList = [Block(1, 2, 3, (0,0,0)), Block(4, 5, 6, (0,0,0,))]

for i in range (0, len(bList)):
    print bList[i].getX()

print (bList[1])
bList.pop(0)
print (bList[0])
