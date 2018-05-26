import pygame
from Block import Block

class BlockT(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
        self.orientation = 0
        self.color = (210, 77, 255)

##          |_3_|
##      |_1_|_0_|_2_|   orientation 0

##          |_2_|
##      |_3_|_0_|       orientation 1
##          |_1_|

##      |_2_|_0_|_1_|   orientation 2
##          |_3_|

##          |_1_|
##          |_0_|_3_|   orientation 3
##          |_2_|


        
        self.blockList = [Block(x, y, size, self.color), Block(x-size, y, size, self.color), Block(x+size, y, size, self.color), Block(x, y-size, size, self.color)]
        
    def display(self, gameDisplay):
        for i in range (0, len(self.blockList)):
            self.blockList[i].display(gameDisplay)

    def getLeftBoundary(self):
        left = self.blockList[0].getX()
        for i in range (1, len(self.blockList)):
            if self.blockList[i].getX() < left:
                left = self.blockList[i].getX()
        return left

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

    # rotation about index 1
    def rotateL4(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(-2*self.size)
            self.blockList[2].setRelativeY(-2*self.size)
            self.blockList[3].setRelativeX(-2*self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-2*self.size)
            self.blockList[2].setRelativeY(2*self.size)
            self.blockList[3].setRelativeY(2*self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeX(2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)

        self.orientation = self.orientation + 1

    def rotateL3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeX(2 * self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeX(-2 * self.size)

        self.orientation = self.orientation + 1

    # rotation about index 3
    def rotateL2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeY(-2 * self.size + self.size)
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeY(-2 * self.size + self.size)
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(self.size)  ####
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeY(2 * self.size - self.size)
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeY(2 * self.size - self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-self.size)  ####
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1

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

    # rotation about index 1
    def rotateR4(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeX(2 * self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeX(-2 * self.size)

        self.orientation = self.orientation - 1

    def rotateR3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeX(2 * self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)

        self.orientation = self.orientation - 1

    # rotation about index 3
    def rotateR2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeY(-2 * self.size + self.size)
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(self.size)  ####
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeY(2 * self.size - self.size)
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeY(2 * self.size - self.size)
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-self.size)  ####
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeY(-2 * self.size + self.size)
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1

        self.orientation = self.orientation - 1

         
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
