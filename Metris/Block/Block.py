import pygame

class Block(object):
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        return self.color

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x
    
    def setRelativeY(self, dy):
        self.y += dy

    def setRelativeX(self, dx):
        self.x += dx

    def display(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0, 0, 0), [self.x, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.size - 1, self.size - 1])
        pygame.draw.rect(gameDisplay, (255,255,255), [self.x, self.y, self.size / 10, self.size / 10])

    black = (0, 0, 0)
    red = (255, 0, 0)
