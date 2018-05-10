import pygame
from Block import Block

class BlockJ(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
        self.orientation = 0
        self.color = (0,0,139)

##   |1|
##   |2||0||3|

        self.blockList = [Block(x,y,size, self.color), Block(x-size,y-size,size, self.color), Block(x-size,y,size, self.color), Block(x+size,y,size, self.color)]

    def display(self, gameDisplay):
        for i in range(0, len(self.blockList)):
            self.blockList[i].display(gameDisplay)

    def getLeftBoundary(self):
        left = self.blockList[0].getX()
        for i in range(1, len(blockList)):
            if self.blockList[i].getX() < left:
                left = self.blockList[i].getX()
        return left

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        if self.orientation % 4 == 0:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() - self.size)
        elif self.orientation % 4 == 1:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX() - self.size)
            self.blockList[3].setY(self.blockList[0].getY())
        elif self.orientation % 4 == 2:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() + self.size)
        elif self.orientation % 4 == 3:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX() + self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation = self.orientation + 1

    def rotateR(self):
        ##   |1|
        ##   |2||0||3|
        if self.orientation % 4 == 0:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() + self.size)
        elif self.orientation % 4 == 1:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX() + self.size)
            self.blockList[3].setY(self.blockList[0].getY())
        elif self.orientation % 4 == 2:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() - self.size)
        elif self.orientation % 4 == 3:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX() - self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation = self.orientation - 1
            

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        dy = y -self.y
        self.y = y
        for i in range(0, len(self.blockList)):
            self.blockList[i].setRelativeY(dy)

    def setX(self, x):
        dx = x - self.x
        self.x = x
        for i in range(0, len(self.blockList)):
            self.blockList[i].setRelativeX(dx)
                
