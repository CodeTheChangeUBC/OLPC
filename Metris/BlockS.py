import pygame
from Block import Block

class BlockS(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
        self.orientation = 0


##   |0|
##   |1||2|
##      |3|         Orientation 0

        self.blockList = [Block(x, y-size, size),
                          Block(x, y, size),
                          Block(x+size, y, size),
                          Block(x+size, y+size, size)]
        self.color = (0, 255, 0)

    def display(self, gameDisplay):
        for i in range(0, len(self.blockList)):
            pygame.draw.rect(gameDisplay, Block.black, [self.blockList[i].getX(), self.blockList[i].getY(), self.size, self.size])
            pygame.draw.rect(gameDisplay, self.color, [self.blockList[i].getX(), self.blockList[i].getY(), self.size, self.size])

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        self.blockList[2].setX(self.blockList[3].getX())
        self.blockList[2].setY(self.blockList[3].getY())

        self.blockList[3].setX(self.blockList[1].getX())
        self.blockList[3].setY(self.blockList[1].getY())

        if self.orientation % 4 == 0:
            self.blockList[1].setRelativeX(self.size)
            self.blockList[1].setRelativeY(self.size)
        elif self.orientation % 4 == 1:
            self.blockList[1].setRelativeX(self.size)
            self.blockList[1].setRelativeY(-self.size)
        elif self.orientation % 4 == 2:
            self.blockList[1].setRelativeX(-self.size)
            self.blockList[1].setRelativeY(-self.size)
        elif self.orientation % 4 == 3:
            self.blockList[1].setRelativeX(-self.size)
            self.blockList[1].setRelativeY(self.size)

        self.orientation = self.orientation + 1

    def rotateR(self):
        self.blockList[1].setX(self.blockList[3].getX())
        self.blockList[1].setY(self.blockList[3].getY())

        self.blockList[3].setX(self.blockList[2].getX())
        self.blockList[3].setY(self.blockList[2].getY())

        if self.orientation % 4 == 0:
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)
        elif self.orientation % 4 == 1:
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)
        elif self.orientation % 4 == 2:
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)
        elif self.orientation % 4 == 3:
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)

        self.orientation = self.orientation - 1

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        dy = y - self.y
        self.y = y
        for i in range(0, len(self.blockList)):
            self.blockList[i].setRelativeY(dy)

    def setX(self, x):
        dx = x - self.x
        self.x = x
        for i in range(0, len(self.blockList)):
            self.blockList[i].setRelativeX(dx)
