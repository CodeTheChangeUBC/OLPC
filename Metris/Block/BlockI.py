#

import pygame
from Block import Block

class BlockI(object):
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (135,206,250)
        self.blockList = [Block(x, y, size, self.color), Block(x - size, y, size, self.color), Block(x + size, y, size, self.color), Block(x + 2*size, y, size, self.color)]
        self.orientation = 0

    def display(self, gameDisplay):
        for i in range (0, len(self.blockList)):
            pygame.draw.rect(gameDisplay, Block.black, [self.blockList[i].getX(), self.blockList[i].getY(), self.size, self.size])
            pygame.draw.rect(gameDisplay, self.color, [self.blockList[i].getX(), self.blockList[i].getY(), self.size - 1, self.size - 1])

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        # rotate RED the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[1].setRelativeX(self.size)
            self.blockList[1].setRelativeY(self.size)
            
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)
            
            self.blockList[3].setRelativeX(-2*self.size)
            self.blockList[3].setRelativeY(-2*self.size)

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[1].setRelativeX(self.size + self.size)
            self.blockList[1].setRelativeY(-self.size)

            self.blockList[0].setRelativeX(self.size)
            
            self.blockList[2].setRelativeX(-self.size + self.size)
            self.blockList[2].setRelativeY(self.size)
            
            self.blockList[3].setRelativeX(-2*self.size + self.size)
            self.blockList[3].setRelativeY(2*self.size)
        
        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[1].setRelativeX(-self.size)
            self.blockList[1].setRelativeY(-self.size)
            
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)
            
            self.blockList[3].setRelativeX(2*self.size)
            self.blockList[3].setRelativeY(2*self.size)

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:
            self.blockList[1].setRelativeX(-self.size - self.size);
            self.blockList[1].setRelativeY(self.size);

            self.blockList[0].setRelativeX(-self.size)
            
            self.blockList[2].setRelativeX(self.size - self.size)
            self.blockList[2].setRelativeY(-self.size);
            
            self.blockList[3].setRelativeX(2*self.size - self.size)
            self.blockList[3].setRelativeY(-2*self.size);

        self.orientation += 1;

    def rotateR(self):
        # rotate RED the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[1].setRelativeX(self.size)
            self.blockList[1].setRelativeY(-self.size)
            
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)
            
            self.blockList[3].setRelativeX(-2*self.size)
            self.blockList[3].setRelativeY(2*self.size)

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[1].setRelativeX(-self.size - self.size)
            self.blockList[1].setRelativeY(-self.size)

            self.blockList[0].setRelativeX(-self.size)
            
            self.blockList[2].setRelativeX(self.size - self.size)
            self.blockList[2].setRelativeY(self.size)
            
            self.blockList[3].setRelativeX(2*self.size - self.size)
            self.blockList[3].setRelativeY(2*self.size)
        
        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[1].setRelativeX(-self.size)
            self.blockList[1].setRelativeY(self.size)
            
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)
            
            self.blockList[3].setRelativeX(2*self.size)
            self.blockList[3].setRelativeY(-2*self.size)

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:         
            self.blockList[1].setRelativeX(self.size + self.size)
            self.blockList[1].setRelativeY(self.size)

            self.blockList[0].setRelativeX(self.size)
            
            self.blockList[2].setRelativeX(-self.size + self.size)
            self.blockList[2].setRelativeY(-self.size)
            
            self.blockList[3].setRelativeX(-2*self.size + self.size)
            self.blockList[3].setRelativeY(-2*self.size)
            
        self.orientation -= 1

    def getX(self):
        return self.x

    def getY(self):
        return self.y
        
    def setY(self, y):
        dy = y - self.y
        self.y = y
        for i in range (0, len(self.blockList)):
            self.blockList[i].setRelativeY(dy)

    def setX(self, x):
        dx = x - self.x
        self.x = x
        for i in range (0, len(self.blockList)):
            self.blockList[i].setRelativeX(dx)

    def getColor(self):
        return self.color
