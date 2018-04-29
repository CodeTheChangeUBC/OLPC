class Block(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setY(self, dy):
        self.y += dy

    def setX(self, dx):
        self.x += dx
