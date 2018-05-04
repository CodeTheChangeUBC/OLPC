import pygame
from random import shuffle
from random import randint
from BlockT import BlockT
from BlockO import BlockO
from BlockI import BlockI
from BlockL import BlockL
from BlockS import BlockS
from BlockZ import BlockZ
from BlockJ import BlockJ

pygame.init()

HEIGHT = 600
WIDTH = 800
LEFT_BOUNDARY = WIDTH / 3
RIGHT_BOUNDARY = WIDTH - WIDTH / 3
BLOCK_SIZE = (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 11
INIT_X = WIDTH / 2
INIT_Y = 10

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Metris')

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#pygame.display.flip()
pygame.display.update()

global gameExit
gameExit = False

block1 = [BLOCK_SIZE, BLOCK_SIZE]
global pos_x
pos_x = WIDTH / 2
global pos_y
pos_y = 10
dx = 0
dy = 0
hasMove = False
global score
score = 0
font = pygame.font.SysFont(None, 25)
gone_down = False
global currentBlock
currentBlock = False
block = None
global blockPlaced
blockPlaced = False
global landed
landed = []
speed = 10

landed = [[None for i in range(25)] for j in range(10)]

TICK = pygame.USEREVENT + 1
pygame.time.set_timer(TICK, 1000)
clock = pygame.time.Clock()


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def tick(pos_y):
    if block != None:
        global currentBlock
        block.setY(pos_y + BLOCK_SIZE)
        if checkCollision():
            block.setY(pos_y)
            currentBlock = False

            for i in range (0, len(block.getPerimeter())):
                landed[x2Index(block.getPerimeter()[i].getX())][y2Index(block.getPerimeter()[i].getY())] = block.getPerimeter()[i]
            checkLandedAndDelete()
            checkGameOver()
        else:
            pos_y += BLOCK_SIZE
    return pos_y


def checkLandedAndDelete():
    y = 0
    rowsToDelete = []
    while (y < len(landed[0])):
        if (rowFilled(y)):
            rowsToDelete.insert(len(rowsToDelete), y)
        y = y + 1
    deleteRows(rowsToDelete)


def rowFilled(y):
    for x in range (0, len(landed)):
        if (landed[x][y] == None):
            return False
    return True


def deleteRows(rows):
    global score
    # delete rows
    for i in range (0, len(rows)):
        for x in range (0, len(landed)):
            landed[x][rows[i]] = None
    # move rows above deleted rows down
    for i in range (0, len(rows)):
        for y in range (rows[i], 0, -1):
            for x in range (0, len(landed)):
                if y > 0:
                    if landed[x][y - 1] != None:
                        landed[x][y - 1].setRelativeY(BLOCK_SIZE)
                    landed[x][y] = landed[x][y - 1]
                    
    # update score
    score = score + len(rows)*len(rows)*10
            
##    # move everything down 1
##    for y in range(rows[0], len(landed[0]) - 1):
##        for x in range(0, len(landed) - 1):
##            # if not the top row
##            if (y + len(rows) < len(landed[0])):
##                landed[x][y] = landed[x][y - rows.len()]
##            # else we are at the top row
##            else :
##                landed[x][y] = None
##            landed[x][y].setY(y + BLOCK_SIZE)

def checkGameOver():
    global gameExit
    for y in range (0, len(landed[0]) - 20):
        for x in range (0, len(landed)):
            if landed[x][y] != None:
                gameOver()
            
def checkCollision():
    global currentBlock
    if not currentBlock:
        return False
    global landed
    blockPerimeter = block.getPerimeter()
    for i in range (0, len(blockPerimeter)):
        for j in range (0, len(landed)):
            for k in range (0, len(landed[j])):
                if landed[j][k] != None:
                    if blockPerimeter[i].getX() == landed[j][k].getX() and blockPerimeter[i].getY() == landed[j][k].getY():
                        return True
    for i in range(0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY or blockPerimeter[i].getX() > RIGHT_BOUNDARY - BLOCK_SIZE or blockPerimeter[i].getY() > HEIGHT - BLOCK_SIZE:
            return True


def checkCollisionRotation():
    global pos_x
    global pos_y
    global currentBlock
    if not currentBlock:
        return False
    global landed
    blockPerimeter = block.getPerimeter()
    for i in range (0, len(blockPerimeter)):
        for j in range (0, len(landed)):
            for k in range (0, len(landed[j])):
                if landed[j][k] != None:
                    if blockPerimeter[i].getX() == landed[j][k].getX() and blockPerimeter[i].getY() == landed[j][k].getY():
                        block.setY(block.getY() - BLOCK_SIZE)
                        pos_y -= BLOCK_SIZE
                        if checkCollision():
                            block.setY(block.getY() + BLOCK_SIZE)
                            pos_y += BLOCK_SIZE
                            return True
    for i in range (0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY:
            block.setX(block.getX() + BLOCK_SIZE)
            pos_x += BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() - BLOCK_SIZE)
                pos_x -= BLOCK_SIZE
                return True
            break
        elif blockPerimeter[i].getX() > RIGHT_BOUNDARY - BLOCK_SIZE:
            block.setX(block.getX() - BLOCK_SIZE)
            pos_x -= BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() + BLOCK_SIZE)
                pos_x += BLOCK_SIZE
                return True
            break
        elif blockPerimeter[i].getY() > HEIGHT - BLOCK_SIZE:
            block.setY(block.getY() - BLOCK_SIZE)
            pos_y -= BLOCK_SIZE
            if checkCollision():
                block.setY(block.getX() + BLOCK_SIZE)
                pos_y += BLOCK_SIZE
                return True
            break
    return False


def x2Index(x):
    return (x - LEFT_BOUNDARY) / BLOCK_SIZE


def y2Index(y):
    return y / BLOCK_SIZE

## function to get the minimum vertical difference between current block and
#  the bottom landed Blocks
def getShadowDifference(blockList):
    maxIndex = len(landed[0]) - 1
    difference = maxIndex * BLOCK_SIZE - blockList[0].getY() - 14
    for i in range(0, len(blockList)):
        if difference > maxIndex * BLOCK_SIZE - blockList[i].getY() - 14:
            difference = maxIndex * BLOCK_SIZE - blockList[i].getY() - 14
    for i in range(0, len(blockList)):
        currX = x2Index(blockList[i].getX())
        currY = y2Index(blockList[i].getY())
        for y in range(currY, len(landed[0])):
            if landed[currX][y] != None and difference > y * BLOCK_SIZE - blockList[i].getY() - 14:
                difference = y * BLOCK_SIZE - blockList[i].getY() - 14
    return difference

def drawShadow(blockList, dy):
    for i in range(0, len(blockList)):
        pygame.draw.rect(gameDisplay, blockList[i].getColor(),
             [blockList[i].getX(), blockList[i].getY() + dy, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(gameDisplay, (255, 255, 255),
             [blockList[i].getX() + 1, blockList[i].getY() + dy + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2])

def getRandomBlockSet(lastBlock):
    set = [0, 1, 2, 3, 4, 5, 6]
    shuffle(set)
    if set[0] == lastBlock:
        tmp = set[0]
        set[0] = set[5]
        set[5] = tmp
    return set

def paused():
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        
        gameDisplay.fill(white, [LEFT_BOUNDARY, 0, WIDTH/3 + 10, HEIGHT])
        pausedText = font.render("Paused", True, black)
        gameDisplay.blit(pausedText, (WIDTH/3 + WIDTH/6, HEIGHT/2)) 
        pygame.display.update()
        clock.tick(15)    
    
def gameOver():
    pause = True
    global currentBlock
    global block
    global landed
    global score

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    currentBlock = False
                    block = None
                    score = 0
                    for i in range(0, len(landed)):
                        for j in range(0, len(landed[i])):
                            landed[i][j] = None
                    runGame()
        pausedText = font.render("Game Over", True, black)
        gameDisplay.blit(pausedText, (WIDTH/3 + WIDTH/6, HEIGHT/2)) 
        pygame.display.update()
        clock.tick(15)   

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def runGame():
    global gameExit
    global currentBlock
    global hasMove
    global dx
    global dy
    global block
    global speed
    global pos_y
    global pos_x
    blockSet = getRandomBlockSet(7)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if pos_x:
                        dx = -BLOCK_SIZE
                        # dy = 0
                        if event.key == pygame.K_DOWN:
                            speed = 10
                elif event.key == pygame.K_RIGHT:
                    if pos_x:
                        dx = BLOCK_SIZE
                        # dy = 0
                        if event.key == pygame.K_DOWN:
                            speed = 10
                elif event.key == pygame.K_DOWN:
                    dy = BLOCK_SIZE
                    # dx = 0
                    speed = 20
                    
                elif event.key == pygame.K_UP:
                    if currentBlock:
                        block.rotateR()
                        if checkCollisionRotation():
                            block.rotateL()
                elif event.key == pygame.K_z:
                    if currentBlock:
                        block.rotateL()
                        if checkCollisionRotation():
                            block.rotateR()
                elif event.key == pygame.K_SPACE:
                    while (not checkCollision()):
                        block.setY(block.getY() + BLOCK_SIZE)
                        pos_y += BLOCK_SIZE

                    block.setY(block.getY() - BLOCK_SIZE)
                    pos_y -= BLOCK_SIZE

                    pos_y = tick(pos_y)
                elif event.key == pygame.K_p:
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if dx < 0:
                        dx = 0
                    # dy = 0
                if event.key == pygame.K_RIGHT:
                    if dx > 0:
                        dx = 0
                if event.key == pygame.K_DOWN:
                    dy = 0
                    # dx = 0
                    speed = 10
            if event.type == TICK:
                pos_y = tick(pos_y)
                

        # drawing bg
        gameDisplay.fill(white)
        gameDisplay.fill(black, [0, 0, LEFT_BOUNDARY, HEIGHT])
        gameDisplay.fill(black, [RIGHT_BOUNDARY, 0, WIDTH - RIGHT_BOUNDARY, HEIGHT])
        gameDisplay.fill(black, [0, 0, WIDTH, HEIGHT - 20*BLOCK_SIZE])

        # drawing block objs
        if not currentBlock and not gameExit:
            rand = blockSet.pop()
            if (len(blockSet) == 0):
                blockSet = getRandomBlockSet(rand)
            if rand == 0:
                block = BlockT(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 1:
                block = BlockS(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 2:
                block = BlockJ(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 3:
                block = BlockI(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 4:
                block = BlockL(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 5:
                block = BlockZ(INIT_X, INIT_Y, BLOCK_SIZE)
            elif rand == 6:
                block = BlockO(INIT_X, INIT_Y, BLOCK_SIZE)
            pos_x = INIT_X
            pos_y = INIT_Y
            currentBlock = True
        difference = getShadowDifference(block.getPerimeter())
        drawShadow(block.getPerimeter(), difference)
        for i in range(0, len(landed)):
            for j in range(0, len(landed[i])):
                if (landed[i][j] != None):
                    landed[i][j].display(gameDisplay)
        block.display(gameDisplay)

        # score
        screen_text = font.render("score: " + str(score), True, white)
        gameDisplay.blit(screen_text, (RIGHT_BOUNDARY +
                                    LEFT_BOUNDARY / 10, HEIGHT / 20))

        # collision checking
        if not hasMove:
            #clock.tick(10) - movement speed
            block.setX(pos_x + dx)
            block.setY(pos_y + dy)
            if checkCollision():
                block.setX(pos_x)
                block.setY(pos_y)
            else:
                pos_x += dx
                pos_y += dy

            hasMove = True

        pygame.display.update()

        clock.tick(speed)
        hasMove = False


    pygame.quit()
    quit()

runGame()