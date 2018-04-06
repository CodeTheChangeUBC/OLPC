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
pos_x = WIDTH / 2
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
blockList = []


TICK = pygame.USEREVENT + 1
pygame.time.set_timer(TICK, 1000)
clock = pygame.time.Clock()

def tick(pos_y):
    if block != None:
        # block.setY(block.getY() + BLOCK_SIZE)
        pos_y += BLOCK_SIZE
        global blockPlaced
        global currentBlock
        if (blockPlaced == True):
            currentBlock = False
            blockPlaced = False
        return pos_y

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if pos_x:
                    dx = -BLOCK_SIZE
                    dy = 0
            elif event.key == pygame.K_RIGHT:
                if pos_x:
                    dx = BLOCK_SIZE
                    dy = 0
            elif event.key == pygame.K_DOWN:
                dy = 2*BLOCK_SIZE
                dx = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                dx = 0
                dy = 0
            if event.key == pygame.K_DOWN:
                dy = 0
                dx = 0
        if event.type == TICK:
            #if pos_y < HEIGHT - 2*BLOCK_SIZE:
            pos_y = tick(pos_y)

        #change to touch another block
        #if pos_y >= (HEIGHT - BLOCK_SIZE):
        #    dy = 0

    # drawing bg & block
    gameDisplay.fill(white)
    gameDisplay.fill(black, [0, 0, LEFT_BOUNDARY, HEIGHT])
    gameDisplay.fill(black, [RIGHT_BOUNDARY, 0, WIDTH - RIGHT_BOUNDARY, HEIGHT])
    pygame.draw.rect(gameDisplay, black, [pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE])
    pygame.draw.rect(gameDisplay, red, [pos_x, pos_y, BLOCK_SIZE - 1, BLOCK_SIZE - 1])

    #test draw block obj
    if not currentBlock:
        block = BlockT(BLOCK_SIZE, INIT_X, INIT_Y)
        blockList.insert(len(blockList), block)
        pos_x = INIT_X
        pos_y = INIT_Y
        currentBlock = True
    block.display(gameDisplay)
    
    # score
    screen_text = font.render("score: " + str(score), True, white)
    gameDisplay.blit(screen_text, (RIGHT_BOUNDARY + LEFT_BOUNDARY / 10, HEIGHT / 20))

    # boundary checking (maybe put block collison here too)
    if not hasMove:
        clock.tick(10)
        if not pos_x + dx <= LEFT_BOUNDARY and not pos_x + 2*dx >= RIGHT_BOUNDARY and block != None:
            pos_x += dx
            block.setX(pos_x)
        if not pos_y + dy >= HEIGHT - BLOCK_SIZE and block != None:
            pos_y += dy
            block.setY(pos_y)
        else:
            blockPlaced = True
        hasMove = True
    
    pygame.display.update()
    
    clock.tick(40)
    hasMove = False


pygame.quit()
quit()
