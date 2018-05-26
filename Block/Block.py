import pygame

class Block(object):
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        if color[0] >= 25:
            r = color[0] - 25
        else:
            r = color[0]
        if color[1] >= 25:
            g = color[1] - 25
        else:
            g = color[1]
        if color[2] >= 25:
            b = color[2] - 25
        else:
            b = color[2]
        self.color2 = (r,g,b)
            
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
        pygame.draw.rect(gameDisplay, (0,0,0), [self.x, self.y, self.size, self.size])
        pygame.draw.rect(gameDisplay, self.color2, [self.x + self.size/10, self.y + self.size/10, self.size - self.size/5, self.size - self.size/5])
        pygame.draw.rect(gameDisplay, self.color, [self.x + self.size/4, self.y + self.size/4, self.size - self.size/2, self.size - self.size/2])
        pygame.draw.rect(gameDisplay, (255,255,255), [self.x + self.size/10, self.y + self.size/10, self.size /10, self.size /10])

    black = (0, 0, 0)
    red = (255, 0, 0)
