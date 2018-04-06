import pygame

black = (0, 0, 0)

class BlockT(object):
    def __init__(self, size, x, y):
        self.x = x
        self.y = y
        self.isCurrent = False
        self.size = size
##        self.block1 = [size, size]
##        self.block2 = [size, size]
##        self.block3 = [size, size]
##        self.block4 = [size, size]
        self.color = (175, 0, 125)
        
    def display(self, gameDisplay):
        pygame.draw.rect(gameDisplay, black, [self.x, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, black, [self.x + self.size, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, black, [self.x - self.size, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, black, [self.x, self.y - self.size, self.size, self.size])
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.size - 1, self.size - 1])
        pygame.draw.rect(gameDisplay, self.color, [self.x + self.size, self.y, self.size - 1, self.size - 1])
        pygame.draw.rect(gameDisplay, self.color, [self.x - self.size, self.y, self.size - 1, self.size - 1])
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y - self.size, self.size - 1, self.size - 1])

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def setX(self, x):
        self.x = x

    
