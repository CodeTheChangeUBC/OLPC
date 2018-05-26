#

import pygame
from Block import Block


class BlockI(object):

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (135, 206, 250)
        self.blockList = [Block(x, y, size, self.color), Block(x - size, y, size, self.color),
                          Block(x + size, y, size, self.color), Block(x + 2 * size, y, size, self.color)]
        self.orientation = 0

    def display(self, gameDisplay):
        for i in range(0, len(self.blockList)):
            self.blockList[i].display(gameDisplay)

    def getPerimeter(self):
        return self.blockList

    def rotateL(self):
        # rotate about the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[0].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() - 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[0].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() - 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[0].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() + 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:
            self.blockList[0].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() + 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation += 1

    def rotateL2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size + 2*self.size)
            self.blockList[1].setRelativeY(2*self.size)  ####
            self.blockList[2].setRelativeX(-2*self.size)
            self.blockList[2].setRelativeY(-2*self.size + 2*self.size)
            self.blockList[3].setRelativeX(-3*self.size)
            self.blockList[3].setRelativeY(-3*self.size + 2*self.size)
            # move everything down 2
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size - self.size)
            self.blockList[3].setRelativeX(-3 * self.size)
            self.blockList[3].setRelativeY(3 * self.size - self.size)
            # move everything up 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size - 2*self.size)
            self.blockList[1].setRelativeY(-2*self.size)  ####
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size - 2*self.size)
            self.blockList[3].setRelativeX(3 * self.size)
            self.blockList[3].setRelativeY(3 * self.size - 2*self.size)
            # move everything up 2
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size + self.size)
            self.blockList[3].setRelativeX(3 * self.size)
            self.blockList[3].setRelativeY(-3 * self.size + self.size)
            # move everything down 1

        self.orientation += 1

    def rotateR2(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(self.size - self.size)
            self.blockList[1].setRelativeY(-self.size)  ####
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size - self.size)
            self.blockList[3].setRelativeX(-3 * self.size)
            self.blockList[3].setRelativeY(3 * self.size - self.size)
            # move everything up 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(self.size - 2*self.size)
            self.blockList[1].setRelativeY(-2*self.size)  ####
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(2 * self.size - 2*self.size)
            self.blockList[3].setRelativeX(3 * self.size)
            self.blockList[3].setRelativeY(3 * self.size - 2*self.size)
            # move everything up 2
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(self.size)
            self.blockList[0].setRelativeY(-self.size + self.size)
            self.blockList[1].setRelativeY(self.size)  ####
            self.blockList[2].setRelativeX(2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size + self.size)
            self.blockList[3].setRelativeX(3 * self.size)
            self.blockList[3].setRelativeY(-3 * self.size + self.size)
            # move everything down 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-self.size)
            self.blockList[0].setRelativeY(-self.size + 2*self.size)
            self.blockList[1].setRelativeY(2*self.size)  ####
            self.blockList[2].setRelativeX(-2 * self.size)
            self.blockList[2].setRelativeY(-2 * self.size + 2*self.size)
            self.blockList[3].setRelativeX(-3 * self.size)
            self.blockList[3].setRelativeY(-3 * self.size + 2*self.size)
            # move everything down 2

        self.orientation -= 1

    def rotateL3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(2*self.size)
            self.blockList[0].setRelativeY(2*self.size - self.size)
            self.blockList[1].setRelativeX(3*self.size)
            self.blockList[1].setRelativeY(3*self.size - self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size - self.size)
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(2 * self.size)
            self.blockList[0].setRelativeY(-2 * self.size + 2*self.size)
            self.blockList[1].setRelativeX(3 * self.size)
            self.blockList[1].setRelativeY(-3 * self.size + 2*self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size + 2*self.size)
            self.blockList[3].setRelativeY(2*self.size)  ####
            # move everything down 2
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-2 * self.size)
            self.blockList[0].setRelativeY(-2 * self.size + self.size)
            self.blockList[1].setRelativeX(-3 * self.size)
            self.blockList[1].setRelativeY(-3 * self.size + self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size + self.size)
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(-2 * self.size)
            self.blockList[0].setRelativeY(2 * self.size - 2*self.size)
            self.blockList[1].setRelativeX(-3 * self.size)
            self.blockList[1].setRelativeY(3 * self.size - 2*self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size - 2*self.size)
            self.blockList[3].setRelativeY(-2*self.size)  ####
            # move everything up 2

        self.orientation += 1

    def rotateR3(self):
        if self.orientation % 4 == 0:
            self.blockList[0].setRelativeX(2 * self.size)
            self.blockList[0].setRelativeY(-2 * self.size + 2*self.size)
            self.blockList[1].setRelativeX(3 * self.size)
            self.blockList[1].setRelativeY(-3 * self.size + 2*self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(-self.size + 2*self.size)
            self.blockList[3].setRelativeY(2*self.size)  ####
            # move everything down 2
        elif self.orientation % 4 == 1:
            self.blockList[0].setRelativeX(-2 * self.size)
            self.blockList[0].setRelativeY(-2 * self.size + self.size)
            self.blockList[1].setRelativeX(-3 * self.size)
            self.blockList[1].setRelativeY(-3 * self.size + self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(-self.size + self.size)
            self.blockList[3].setRelativeY(self.size)  ####
            # move everything down 1
        elif self.orientation % 4 == 2:
            self.blockList[0].setRelativeX(-2 * self.size)
            self.blockList[0].setRelativeY(2 * self.size - 2*self.size)
            self.blockList[1].setRelativeX(-3 * self.size)
            self.blockList[1].setRelativeY(3 * self.size - 2*self.size)
            self.blockList[2].setRelativeX(-self.size)
            self.blockList[2].setRelativeY(self.size - 2*self.size)
            self.blockList[3].setRelativeY(-2*self.size)  ####
            # move everything up 2
        elif self.orientation % 4 == 3:
            self.blockList[0].setRelativeX(2 * self.size)
            self.blockList[0].setRelativeY(2 * self.size - self.size)
            self.blockList[1].setRelativeX(3 * self.size)
            self.blockList[1].setRelativeY(3 * self.size - self.size)
            self.blockList[2].setRelativeX(self.size)
            self.blockList[2].setRelativeY(self.size - self.size)
            self.blockList[3].setRelativeY(-self.size)  ####
            # move everything up 1

        self.orientation -= 1

    def rotateL4(self):
        # rotate about the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[0].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() - 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[0].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() - 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[0].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() + 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:
            self.blockList[0].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() + 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation += 1

    def rotateR4(self):
        # rotate about the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[0].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() + 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[0].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() + 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[0].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() - 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:
            self.blockList[0].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() - 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation -= 1

    def rotateR(self):
        # rotate about the block blockList[0]
        # [1][0][2][3]
        if self.orientation % 4 == 0:
            self.blockList[0].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() + self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() + 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [3]
        # [2]
        # [0]
        # [1]
        elif self.orientation % 4 == 1:
            self.blockList[0].setY(self.blockList[0].getY() - self.size)
            self.blockList[1].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() + self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() + 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        # [3][2][0][1]
        elif self.orientation % 4 == 2:
            self.blockList[0].setX(self.blockList[0].getX() - self.size)
            self.blockList[1].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX())

            self.blockList[2].setY(self.blockList[0].getY() - self.size)
            self.blockList[2].setX(self.blockList[0].getX())

            self.blockList[3].setY(self.blockList[0].getY() - 2 * self.size)
            self.blockList[3].setX(self.blockList[0].getX())

        # [1]
        # [0]
        # [2]
        # [3]
        elif self.orientation % 4 == 3:
            self.blockList[0].setY(self.blockList[0].getY() + self.size)
            self.blockList[1].setX(self.blockList[0].getX() + self.size)
            self.blockList[1].setY(self.blockList[0].getY())

            self.blockList[2].setX(self.blockList[0].getX() - self.size)
            self.blockList[2].setY(self.blockList[0].getY())

            self.blockList[3].setX(self.blockList[0].getX() - 2 * self.size)
            self.blockList[3].setY(self.blockList[0].getY())

        self.orientation -= 1

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

    def getColor(self):
        return self.color
