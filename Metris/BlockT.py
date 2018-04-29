import pygame
from Block import Block

black = (0, 0, 0)

class BlockT(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
        self.blockList = [Block(x, y, size), Block(x-size, y, size), Block(x+size, y, size), Block(x, y-size, size)]
##        self.block1 = Block(size, x, y)
##        self.block2 = Block(size, x - size, y)
##        self.block3 = Block(size, x + size, y)
##        self.block4 = Block(size, x, y - size)
        self.color = (175, 0, 125)
        
    def display(self, gameDisplay):
        for i in range (0, len(self.blockList)):
            pygame.draw.rect(gameDisplay, black, [self.blockList[i].getX(), self.blockList[i].getY(), self.size, self.size])
            pygame.draw.rect(gameDisplay, self.color, [self.blockList[i].getX(), self.blockList[i].getY(), self.size - 1, self.size - 1])
        
##        pygame.draw.rect(gameDisplay, black, [self.block1.getX(), self.block1.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, black, [self.block2.getX(), self.block2.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, black, [self.block3.getX(), self.block3.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, black, [self.block4.getX(), self.block4.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, self.color, [self.block1.getX(), self.block1.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block2.getX(), self.block2.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block3.getX(), self.block3.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block4.getX(), self.block4.getY(), self.size - 1, self.size - 1])

    def getLeftBoundary(self):
        left = self.blockList[0].getX()
        for i in range (1, len(blockList)):
            if self.blockList[i].getX() < left:
                left = self.blockList[i].getX()
        return left

    def getPerimeter(self):
        return self.blockList

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        dy = y - self.y
        self.y = y
        for i in range (0, len(self.blockList)):
            self.blockList[i].setY(dy)

    def setX(self, x):
        dx = x - self.x
        self.x = x
        for i in range (0, len(self.blockList)):
            self.blockList[i].setX(dx)

    
