import pygame
from Block import Block

class BlockO(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.orientation = 0
        self.color = (255, 255, 77)

##        |_2_|_3_|
##        |_0_|_1_|   orientation 0
        
        self.blockList = [Block(x, y, size, self.color), Block(x+size, y, size, self.color), Block(x, y-size, size, self.color), Block(x+size, y-size, size, self.color)]

    def display(self, gameDisplay):
        for i in range (0, len(self.blockList)):
            pygame.draw.rect(gameDisplay, Block.black, [self.blockList[i].getX(), self.blockList[i].getY(), self.size, self.size])
            pygame.draw.rect(gameDisplay, self.color, [self.blockList[i].getX(), self.blockList[i].getY(), self.size - 1, self.size - 1])

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        return

    def rotateR(self):
        return

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
