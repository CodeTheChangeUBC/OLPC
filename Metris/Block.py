import pygame

class Block(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x
    
    def setRelativeY(self, dy):
        self.y += dy

    def setRelativeX(self, dx):
        self.x += dx

    def display(self, gameDisplay):
        pygame.draw.rect(gameDisplay, Block.black, [self.x, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, Block.red, [self.x + 1, self.y + 1, self.size - 2, self.size - 2])

    black = (0, 0, 0)
    red = (255, 0, 0)
