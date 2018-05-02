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

    black = (0, 0, 0)
