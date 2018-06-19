import pygame
from Block import Block

class BlockL(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
        self.orientation = 0
        self.color = (255, 128, 0)

##              | 2 |
##      | 3 |_0_| 1 |
##                    orientation 0
        
        self.blockList = [Block(x, y, size, self.color), Block(x+size, y, size, self.color), Block(x+size, y-size, size, self.color), Block(x-size, y, size, self.color)]
##        self.block1 = Block(size, x, y)
##        self.block2 = Block(size, x, y+size)
##        self.block3 = Block(size, x + size, y+size)
##        self.block4 = Block(size, x, y - size)
        
    def display(self, gameDisplay):
        for i in range (0, len(self.blockList)):
            self.blockList[i].display(gameDisplay)
        
##        pygame.draw.rect(gameDisplay, Block.black, [self.block1.getX(), self.block1.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, Block.black, [self.block2.getX(), self.block2.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, Block.black, [self.block3.getX(), self.block3.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, Block.black, [self.block4.getX(), self.block4.getY(), self.size, self.size])
##        pygame.draw.rect(gameDisplay, self.color, [self.block1.getX(), self.block1.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block2.getX(), self.block2.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block3.getX(), self.block3.getY(), self.size - 1, self.size - 1])
##        pygame.draw.rect(gameDisplay, self.color, [self.block4.getX(), self.block4.getY(), self.size - 1, self.size - 1])

    def getLeftBoundary(self):
        left = self.blockList[0].getX()
        for i in range (1, len(self.blockList)):
            if self.blockList[i].getX() < left:
                left = self.blockList[i].getX()
        return left

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        if self.orientation % 4 == 0:
            self.blockList[1].setX(self.blockList[0].getX())
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() + self.size)
        elif self.orientation % 4 == 1:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX() + self.size)
            self.blockList[3].setY(self.blockList[0].getY())
        elif self.orientation % 4 == 2:
            self.blockList[1].setX(self.blockList[0].getX())
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() - self.size)
        elif self.orientation % 4 == 3:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX() - self.size)
            self.blockList[3].setY(self.blockList[0].getY())
            
        self.orientation = self.orientation + 1

    # rotation about index 1
    def rotateL3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)
            self.blockList[3].setRelativeX(2*self.size)
            self.blockList[3].setRelativeY(2*self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)
            self.blockList[3].setRelativeX(2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)

        self.orientation = self.orientation + 1

    # rotation about index 1
    def rotateR3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)
            self.blockList[3].setRelativeX(2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            self.blockList[3].setRelativeY(-2 * self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)
            self.blockList[3].setRelativeX(2 * self.size)
            self.blockList[3].setRelativeY(2 * self.size)

        self.orientation = self.orientation - 1

    # center rotation
    def rotateL2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)  # + self.size)
            self.blockList[1].setRelativeY(-2*self.size)  # + self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)  # + self.size)
            self.blockList[3].setRelativeX(2*self.size)
            # self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)  # + self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            # self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)  # + self.size)
            self.blockList[3].setRelativeY(-2 * self.size)  # + self.size)
            # move everything down 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)  # - self.size)
            self.blockList[1].setRelativeY(2 * self.size)  # - self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)  # - self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            # self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)  # - self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            # self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)  # - self.size)
            self.blockList[3].setRelativeY(2 * self.size)  # - self.size)
            # move everything up 1

        # if self.orientation % 4 == 0:
        #     self.blockList[0].setRelativeX(2*self.size)
        #     self.blockList[1].setRelativeX(self.size)
        #     self.blockList[1].setRelativeY(-self.size)
        #     self.blockList[3].setRelativeX(3*self.size)
        #     self.blockList[3].setRelativeY(self.size)
        # elif self.orientation % 4 == 1:
        #     self.blockList[0].setRelativeY(-2 * self.size)
        #     self.blockList[1].setRelativeX(-self.size)
        #     self.blockList[1].setRelativeY(-self.size)
        #     self.blockList[3].setRelativeX(self.size)
        #     self.blockList[3].setRelativeY(-3*self.size)
        # elif self.orientation % 4 == 2:
        #     self.blockList[0].setRelativeX(-2 * self.size)
        #     self.blockList[1].setRelativeX(-self.size)
        #     self.blockList[1].setRelativeY(self.size)
        #     self.blockList[3].setRelativeX(-3 * self.size)
        #     self.blockList[3].setRelativeY(-self.size)
        # elif self.orientation % 4 == 3:
        #     self.blockList[0].setRelativeY(2 * self.size)
        #     self.blockList[1].setRelativeX(self.size)
        #     self.blockList[1].setRelativeY(self.size)
        #     self.blockList[3].setRelativeX(-self.size)
        #     self.blockList[3].setRelativeY(3*self.size)

        self.orientation = self.orientation + 1

    # center rotation
    def rotateR2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)  # + self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            # self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size)  # + self.size)
            self.blockList[3].setRelativeY(-2 * self.size)  # + self.size)
            # move everything down 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)  # - self.size)
            self.blockList[1].setRelativeY(2 * self.size)  # - self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size)  # - self.size)
            self.blockList[3].setRelativeX(-2 * self.size)
            # self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)  # - self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            # self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size)  # - self.size)
            self.blockList[3].setRelativeY(2 * self.size)  # - self.size)
            # move everything up 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)  # + self.size)
            self.blockList[1].setRelativeY(-2 * self.size)  # + self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size)  # + self.size)
            self.blockList[3].setRelativeX(2 * self.size)
            # self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1

        # if self.orientation % 4 == 0:
        #     self.blockList[0].setRelativeY(-2 * self.size)
        #     self.blockList[1].setRelativeX(-self.size)
        #     self.blockList[1].setRelativeY(-self.size)
        #     self.blockList[3].setRelativeX(self.size)
        #     self.blockList[3].setRelativeY(-3 * self.size)
        # elif self.orientation % 4 == 1:
        #     self.blockList[0].setRelativeX(-2 * self.size)
        #     self.blockList[1].setRelativeX(-self.size)
        #     self.blockList[1].setRelativeY(self.size)
        #     self.blockList[3].setRelativeX(-3 * self.size)
        #     self.blockList[3].setRelativeY(-self.size)
        # elif self.orientation % 4 == 2:
        #     self.blockList[0].setRelativeY(2 * self.size)
        #     self.blockList[1].setRelativeX(self.size)
        #     self.blockList[1].setRelativeY(self.size)
        #     self.blockList[3].setRelativeX(-self.size)
        #     self.blockList[3].setRelativeY(3 * self.size)
        # elif self.orientation % 4 == 3:
        #     self.blockList[0].setRelativeX(2 * self.size)
        #     self.blockList[1].setRelativeX(self.size)
        #     self.blockList[1].setRelativeY(-self.size)
        #     self.blockList[3].setRelativeX(3 * self.size)
        #     self.blockList[3].setRelativeY(self.size)

        self.orientation = self.orientation - 1

    def rotateL4(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(-2*self.size)
            self.blockList[1].setRelativeY(-2*self.size)
            self.blockList[2].setRelativeX(-3*self.size)
            self.blockList[2].setRelativeY(-self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(3*self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[2].setRelativeX(3 * self.size)
            self.blockList[2].setRelativeY(self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-3*self.size)

        self.orientation = self.orientation + 1

    def rotateR4(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(3 * self.size)
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(2 * self.size)
            self.blockList[2].setRelativeX(3 * self.size)
            self.blockList[2].setRelativeY(self.size)
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-3 * self.size)
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size)
            self.blockList[1].setRelativeX(-2 * self.size)
            self.blockList[1].setRelativeY(-2 * self.size)
            self.blockList[2].setRelativeX(-3 * self.size)
            self.blockList[2].setRelativeY(-self.size)

        self.orientation = self.orientation - 1

    def rotateR(self):
        if self.orientation % 4 == 0:
            self.blockList[1].setX(self.blockList[0].getX())
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() - self.size)
        elif self.orientation % 4 == 1:
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX() - self.size)
            self.blockList[3].setY(self.blockList[0].getY())
        elif self.orientation % 4 == 2:
            self.blockList[1].setX(self.blockList[0].getX())
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[3].setX(self.blockList[0].getX())
            self.blockList[3].setY(self.blockList[0].getY() + self.size)
        elif self.orientation % 4 == 3:
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())
            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[3].setX(self.blockList[0].getX() + self.size)
            self.blockList[3].setY(self.blockList[0].getY())
            
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

    def getColor(self):
        return self.color
