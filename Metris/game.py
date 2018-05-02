import pygame
from BlockT import BlockT

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


gameExit = False

block1 = [BLOCK_SIZE, BLOCK_SIZE]
global pos_x
pos_x = WIDTH / 2
global pos_y
pos_y = 10
dx = 0
dy = 0
hasMove = False
score = 0
font = pygame.font.SysFont(None, 25)
gone_down = False
global currentBlock
currentBlock = False
block = None
global blockPlaced
blockPlaced = False
global blockList
blockList = []
speed = 10


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
        else:
            pos_y += BLOCK_SIZE
    return pos_y

def checkCollision():
    global currentBlock
    if not currentBlock:
        return False
    global blockList
    blockPerimeter = block.getPerimeter()
    for i in range (0, len(blockPerimeter)):
        for j in range (0, len(blockList) - 1):
            placedBlockPerimeter = blockList[j].getPerimeter()
            for k in range (0, len(placedBlockPerimeter)):
                if blockPerimeter[i].getX() == placedBlockPerimeter[k].getX() and blockPerimeter[i].getY() == placedBlockPerimeter[k].getY():
                    return True
    for i in range (0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY or blockPerimeter[i].getX() > RIGHT_BOUNDARY - BLOCK_SIZE or blockPerimeter[i].getY() > HEIGHT - BLOCK_SIZE:
            return True

def checkCollisionRotation():
    global pos_x
    global pos_y
    global currentBlock
    if not currentBlock:
        return False
    global blockList
    blockPerimeter = block.getPerimeter()
    for i in range (0, len(blockPerimeter)):
        for j in range (0, len(blockList) - 1):
            placedBlockPerimeter = blockList[j].getPerimeter()
            for k in range (0, len(placedBlockPerimeter)):
                if blockPerimeter[i].getX() == placedBlockPerimeter[k].getX() and blockPerimeter[i].getY() == placedBlockPerimeter[k].getY():
                    return True
    for i in range (0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY:
            block.setX(block.getX() + BLOCK_SIZE)
            pos_x += BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() - BLOCK_SIZE)
                pos_x -= BLOCK_SIZE
                return True
            break;
        elif blockPerimeter[i].getX() > RIGHT_BOUNDARY - BLOCK_SIZE:
            block.setX(block.getX() - BLOCK_SIZE)
            pos_x -= BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() + BLOCK_SIZE)
                pos_x += BLOCK_SIZE
                return True
            break;
        elif blockPerimeter[i].getY() > HEIGHT - BLOCK_SIZE:
            block.setY(block.getY() - BLOCK_SIZE)
            pos_y -= BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() + BLOCK_SIZE)
                pos_y += BLOCK_SIZE
                return True
            break;
    return False

    
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if pos_x:
                    dx = -BLOCK_SIZE
                    dy = 0
                    speed = 10
            elif event.key == pygame.K_RIGHT:
                if pos_x:
                    dx = BLOCK_SIZE
                    dy = 0
                    speed = 10
            elif event.key == pygame.K_DOWN:
                dy = BLOCK_SIZE
                dx = 0
                speed = 20
            elif event.key == pygame.K_UP:
                if currentBlock:
                    block.rotateL()
                    if checkCollisionRotation():
                        block.rotateR()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                dx = 0
                dy = 0
            if event.key == pygame.K_DOWN:
                dy = 0
                dx = 0
                speed = 10
        if event.type == TICK:
            pos_y = tick(pos_y)


    # drawing bg
    gameDisplay.fill(white)
    gameDisplay.fill(black, [0, 0, LEFT_BOUNDARY, HEIGHT])
    gameDisplay.fill(black, [RIGHT_BOUNDARY, 0, WIDTH - RIGHT_BOUNDARY, HEIGHT])

    # drawing block objs
    if not currentBlock:
        block = BlockT(INIT_X, INIT_Y, BLOCK_SIZE)
        blockList.insert(len(blockList), block)
        pos_x = INIT_X
        pos_y = INIT_Y
        currentBlock = True
    for i in range(0, len(blockList)):
        blockList[i].display(gameDisplay)
    
    # score
    screen_text = font.render("score: " + str(score), True, white)
    gameDisplay.blit(screen_text, (RIGHT_BOUNDARY + LEFT_BOUNDARY / 10, HEIGHT / 20))

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
            
##        if not pos_x + dx <= LEFT_BOUNDARY and not pos_x + 2*dx >= RIGHT_BOUNDARY and block != None:
##            pos_x += dx
##            block.setX(pos_x)
##        if not pos_y + dy >= HEIGHT - BLOCK_SIZE and block != None:
##            pos_y += dy
##            block.setY(pos_y)
##        else:
##            blockPlaced = True

            
        hasMove = True
    
    pygame.display.update()
    
    clock.tick(speed)
    hasMove = False


pygame.quit()
quit()
