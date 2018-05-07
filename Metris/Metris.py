from pygame.locals import *
import pygame
import random, time, pygame, sys, math

import os
from Block.BlockT import *
from Block.BlockO import *
from Block.BlockI import *
from Block.BlockL import *
from Block.BlockS import *
from Block.BlockZ import *
from Block.BlockJ import *

from menu import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
TEXTCOLOR = WHITE
HEIGHT = 800
WIDTH = 800
LEFT_BOUNDARY = WIDTH / 3
RIGHT_BOUNDARY = WIDTH - WIDTH / 3
BLOCK_SIZE = (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 11
TOP_BOUNDARY = 4 * BLOCK_SIZE
BOTTOM_BOUNDARY = TOP_BOUNDARY + 20 * BLOCK_SIZE
INIT_X = WIDTH / 2
INIT_Y = BLOCK_SIZE
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
global score
score = 0

GAMEDISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Metris')

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

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
# global score
# score = 0
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

landed = [[None for i in range(24)] for j in range(10)]

TICK = pygame.USEREVENT + 1
pygame.time.set_timer(TICK, 1000)
clock = pygame.time.Clock()

holdBlock = None


## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def tick(pos_y):
    if block != None:
        global currentBlock
        block.setY(pos_y + BLOCK_SIZE)
        if checkCollision():
            block.setY(pos_y)
            currentBlock = False

            for i in range(0, len(block.getPerimeter())):
                landed[x2Index(block.getPerimeter()[i].getX())][y2Index(block.getPerimeter()[i].getY())] = \
                    block.getPerimeter()[i]
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
    for x in range(0, len(landed)):
        if (landed[x][y] == None):
            return False
    return True


def deleteRows(rows):
    global score
    # delete rows
    for i in range(0, len(rows)):
        for x in range(0, len(landed)):
            landed[x][rows[i]] = None
    # move rows above deleted rows down
    for i in range(0, len(rows)):
        for y in range(rows[i], 0, -1):
            for x in range(0, len(landed)):
                if y > 0:
                    if landed[x][y - 1] != None:
                        landed[x][y - 1].setRelativeY(BLOCK_SIZE)
                    landed[x][y] = landed[x][y - 1]

    # update score
    if len(rows) == 1:
        score += 10
    else:
        ret = 0
        multiplier = 1
        pt_score = 5
        for x in range(0, len(rows)):
            ret += multiplier * pt_score
            multiplier += 1
        score += ret


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
    for y in range(0, len(landed[0]) - 20):
        for x in range(0, len(landed)):
            if landed[x][y] != None:
                gameOver()


def checkCollision():
    global currentBlock
    if not currentBlock:
        return False
    global landed
    blockPerimeter = block.getPerimeter()
    for i in range(0, len(blockPerimeter)):
        for j in range(0, len(landed)):
            for k in range(0, len(landed[j])):
                if landed[j][k] != None:
                    if blockPerimeter[i].getX() == landed[j][k].getX() and blockPerimeter[i].getY() == landed[j][
                        k].getY():
                        return True
    for i in range(0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY or blockPerimeter[i].getX() > RIGHT_BOUNDARY - BLOCK_SIZE or \
                blockPerimeter[i].getY() > BOTTOM_BOUNDARY - BLOCK_SIZE:
            return True


def checkCollisionRotation():
    global pos_x
    global pos_y
    global currentBlock
    if not currentBlock:
        return False
    global landed
    blockPerimeter = block.getPerimeter()
    for i in range(0, len(blockPerimeter)):
        for j in range(0, len(landed)):
            for k in range(0, len(landed[j])):
                if landed[j][k] != None:
                    if blockPerimeter[i].getX() == landed[j][k].getX() and blockPerimeter[i].getY() == landed[j][
                        k].getY():
                        block.setY(block.getY() - BLOCK_SIZE)
                        pos_y -= BLOCK_SIZE
                        if checkCollision():
                            block.setY(block.getY() + BLOCK_SIZE)
                            pos_y += BLOCK_SIZE
                            return True

    for i in range(0, len(blockPerimeter)):
        if blockPerimeter[i].getX() < LEFT_BOUNDARY - BLOCK_SIZE:
            block.setX(block.getX() + 2 * BLOCK_SIZE)
            pos_x += 2 * BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() - 2 * BLOCK_SIZE)
                pos_x -= 2 * BLOCK_SIZE
                return True
            break
        elif blockPerimeter[i].getX() > RIGHT_BOUNDARY:
            block.setX(block.getX() - 2 * BLOCK_SIZE)
            pos_x -= 2 * BLOCK_SIZE
            if checkCollision():
                block.setX(block.getX() + 2 * BLOCK_SIZE)
                pos_x += 2 * BLOCK_SIZE
                return True
            break

    for i in range(0, len(blockPerimeter)):
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
        elif blockPerimeter[i].getY() > BOTTOM_BOUNDARY - BLOCK_SIZE:
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
    difference = maxIndex * BLOCK_SIZE - blockList[0].getY()  # - 14
    for i in range(0, len(blockList)):
        if difference > maxIndex * BLOCK_SIZE - blockList[i].getY():  # - 14:
            difference = maxIndex * BLOCK_SIZE - blockList[i].getY()  # - 14
    for i in range(0, len(blockList)):
        currX = x2Index(blockList[i].getX())
        currY = y2Index(blockList[i].getY())
        for y in range(currY, len(landed[0])):
            if landed[currX][y] != None and difference > y * BLOCK_SIZE - blockList[i].getY() - BLOCK_SIZE:  # - 14:
                difference = y * BLOCK_SIZE - blockList[i].getY() - BLOCK_SIZE  # - 14
    return difference


def drawShadow(blockList, dy):
    for i in range(0, len(blockList)):
        pygame.draw.rect(GAMEDISPLAY, blockList[i].getColor(),
                         [blockList[i].getX(), blockList[i].getY() + dy, BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(GAMEDISPLAY, (100, 100, 100),
                         [blockList[i].getX() + 1, blockList[i].getY() + dy + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2])


def getRandomBlockSet(lastBlock):
    set = [0, 1, 2, 3, 4, 5, 6]
    shuffle(set)
    if set[0] == lastBlock:
        tmp = set[0]
        set[0] = set[1]
        set[1] = tmp
    return set


def hold(blockSet, nextBlocks):
    global block
    global pos_x
    global pos_y
    global holdBlock

    tmp = holdBlock

    holdBlock = block
    holdBlock.setX(INIT_X)
    holdBlock.setY(INIT_Y)
    pos_x = INIT_X
    pos_y = INIT_Y

    # first time if hold is empty
    if (tmp == None):
        blockType = blockSet.pop(0)
        if blockListTooShort(len(blockSet)):
            appendBlockList(blockSet)

        # TODO make function            
        if blockType == 0:
            block = BlockT(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 1:
            block = BlockS(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 2:
            block = BlockJ(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 3:
            block = BlockI(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 4:
            block = BlockL(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 5:
            block = BlockZ(INIT_X, INIT_Y, BLOCK_SIZE)
        elif blockType == 6:
            block = BlockO(INIT_X, INIT_Y, BLOCK_SIZE)
    else:
        block = tmp
    setNextBlocks(blockSet, nextBlocks)


def blockListTooShort(len):
    if len <= 5:
        return True
    return False


def appendBlockList(blockSet):
    nextBlockSet = getRandomBlockSet(blockSet[len(blockSet) - 1])
    for i in range(0, len(nextBlockSet)):
        blockSet.insert(len(blockSet), nextBlockSet[i])


def setNextBlocks(blockSet, nextBlocks):
    while (len(nextBlocks) != 0):
        nextBlocks.pop()

    for i in range(0, 4):
        if blockSet[i] == 0:
            nextBlocks.insert(i, BlockT(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 1:
            nextBlocks.insert(i, BlockS(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 2:
            nextBlocks.insert(i, BlockJ(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 3:
            nextBlocks.insert(i, BlockI(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 4:
            nextBlocks.insert(i, BlockL(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 5:
            nextBlocks.insert(i, BlockZ(0, 0, BLOCK_SIZE))
        elif blockSet[i] == 6:
            nextBlocks.insert(i, BlockO(0, 0, BLOCK_SIZE))
        nextBlocks[i].setX(RIGHT_BOUNDARY + LEFT_BOUNDARY / 3)
        nextBlocks[i].setY((i + 1) * BLOCK_SIZE * 5)


def paused():
    pause = True

    pygame.mixer.music.pause()
    startTime = pygame.mixer.music.get_pos()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    pause = False

        GAMEDISPLAY.fill(WHITE, [LEFT_BOUNDARY, TOP_BOUNDARY, 11 * BLOCK_SIZE, 21 * BLOCK_SIZE])
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        pausedText = myfont.render("Paused", True, BLACK)
        textWidth = pausedText.get_rect().width
        textHeight = pausedText.get_rect().height

        GAMEDISPLAY.blit(pausedText, (LEFT_BOUNDARY + (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 2 - textWidth / 2,
                                      TOP_BOUNDARY + (BOTTOM_BOUNDARY - TOP_BOUNDARY) / 2 - textHeight / 2))
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        additionalText = myfont.render("Press \"p\" to resume!", True, BLACK)
        additionalTextWidth = additionalText.get_rect().width
        additionalTextHeight = additionalText.get_rect().height

        GAMEDISPLAY.blit(additionalText,
                         (LEFT_BOUNDARY + (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
                          TOP_BOUNDARY + (BOTTOM_BOUNDARY - TOP_BOUNDARY) / 2 + textHeight))

        pygame.display.update()
        clock.tick(15)


def gameOver():
    pause = True
    global currentBlock
    global block
    global landed
    global score
    global holdBlock

    pygame.mixer.music.stop()
    pygame.mixer.music.load('marioDeath.mid')
    pygame.mixer.music.play(0, 0.0)

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
                    holdBlock = None
                    runGame()

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        gameOverText = myfont.render("Game Over", True, BLACK)
        textWidth = gameOverText.get_rect().width
        textHeight = gameOverText.get_rect().height
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        additionalText = myfont.render("Press \"s\" to restart!", True, BLACK)
        additionalTextWidth = additionalText.get_rect().width
        additionalTextHeight = additionalText.get_rect().height

        GAMEDISPLAY.fill(WHITE, [LEFT_BOUNDARY + (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 2 - textWidth,
                                 TOP_BOUNDARY + (BOTTOM_BOUNDARY - TOP_BOUNDARY) / 2 - textHeight, 2 * textWidth,
                                 2 * (textHeight + additionalTextHeight)])
        GAMEDISPLAY.blit(gameOverText, (LEFT_BOUNDARY + (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 2 - textWidth / 2,
                                        TOP_BOUNDARY + (BOTTOM_BOUNDARY - TOP_BOUNDARY) / 2 - textHeight / 2))
        GAMEDISPLAY.blit(additionalText, (
            LEFT_BOUNDARY + (RIGHT_BOUNDARY - LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
            TOP_BOUNDARY + (BOTTOM_BOUNDARY - TOP_BOUNDARY) / 2 + textHeight))

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
    global score
    blockSet = getRandomBlockSet(None)
    blockT = BlockT(0, 0, BLOCK_SIZE)
    blockS = BlockS(0, 0, BLOCK_SIZE)
    blockJ = BlockJ(0, 0, BLOCK_SIZE)
    blockI = BlockI(0, 0, BLOCK_SIZE)
    blockL = BlockL(0, 0, BLOCK_SIZE)
    blockZ = BlockZ(0, 0, BLOCK_SIZE)
    blockO = BlockO(0, 0, BLOCK_SIZE)
    nextBlocks = []

    MUSICS = ['marioUnderground.mp3', 'one_piece_party.mp3']
    musicIndex = randint(0, len(MUSICS) - 1)
    pygame.mixer.music.load(MUSICS[musicIndex])
    pygame.mixer.music.play(-1, 0.0)

    hasSwap = True

    level, fallFreq = calculateLevelAndFallFreq(score)
    level_prev = level
    qSolved = False
    comp_input = 10
    out_list = generateQues(level)
    controlsOn = False
    numTries = 0
    diff1 = out_list[4]
    num_q = 0
    scr_mult = 5
    drawCompliment(comp_input)

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
                    effect = pygame.mixer.Sound('coin.wav')
                    effect.play()
                    speed = 20


                elif event.key == pygame.K_UP and controlsOn == True:
                    if currentBlock:
                        block.rotateR()
                        if checkCollisionRotation():
                            block.rotateL()

                elif event.key == pygame.K_z and controlsOn == True:
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

                elif event.key == pygame.K_LSHIFT:
                    if (hasSwap == True):
                        hold(blockSet, nextBlocks)
                        hasSwap = False
                # check for correct answer
                elif event.key == out_list[9]:
                    if numTries < 1:
                        hard_q = False
                        if diff1 >= 9:
                            hard_q = True
                        comp_input = randint(0, 3)
                        controlsOn = True
                        score += 10 + 5 * num_q
                        if hard_q == True:
                            score += 20
                        hard_q = False
                        level, fallFreq = calculateLevelAndFallFreq(score)
                        num_q += 1
                        out_list = generateQues(level)
                        diff1 = out_list[4]
                elif event.key != out_list[9] and (
                        event.key == pygame.K_q or event.key == pygame.K_w or event.key == pygame.K_e or event.key == pygame.K_r):
                    numTries += 1
                    comp_input = randint(4, 7)
                    controlsOn = False

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
        ##        gameDisplay.fill((100, 100, 100))
        ##        gameDisplay.fill(BLACK, [0, 0, LEFT_BOUNDARY, HEIGHT])
        ##        gameDisplay.fill(BLACK, [RIGHT_BOUNDARY, 0, WIDTH - RIGHT_BOUNDARY, HEIGHT])
        ##        gameDisplay.fill(BLACK, [0, 0, WIDTH, HEIGHT - 20*BLOCK_SIZE])
        GAMEDISPLAY.fill(BLACK, [0, 0, WIDTH, HEIGHT])
        GAMEDISPLAY.fill((100, 100, 100), [LEFT_BOUNDARY, TOP_BOUNDARY, 11 * BLOCK_SIZE, 21 * BLOCK_SIZE])

        # drawing block objs
        if not currentBlock and not gameExit:
            # while len(nextBlocks) != 0:
            #     nextBlocks.pop()

            # calculating new questions
            level, fallFreq = calculateLevelAndFallFreq(score)
            numTries = 0
            controlsOn = False
            out_list = generateQues(level)
            diff1 = out_list[4]
            char = out_list[9]
            comp_input = -1
            num_q = 0

            rand = blockSet.pop(0)
            if blockListTooShort(len(blockSet)):
                appendBlockList(blockSet)

            setNextBlocks(blockSet, nextBlocks)

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
            hasSwap = True
        difference = getShadowDifference(block.getPerimeter())
        drawShadow(block.getPerimeter(), difference)

        # drawing question/answer text

        # draw answer text
        diff2 = out_list[5]
        diff3 = out_list[6]
        sol_key = out_list[3]
        if out_list[2] == 0:
            o = '+'
        elif out_list[2] == 1:
            o = '-'
        elif out_list[2] == 2:
            o = '*'
        elif out_list[2] == 3:
            o = '/'
        elif out_list[2] == 4:
            o = '^'

        if (diff1 < 9):
            if o == '^':
                actual_ans = math.pow(out_list[0], out_list[1])
            else:
                actual_ans = eval(str(out_list[0]) + o + str(out_list[1]))
            actual_ans = int(actual_ans)
            fakeans_list = [actual_ans + diff1, actual_ans - diff2, actual_ans + diff3]
            list_count = 0
        else:
            if o == '^':
                inter_ans = math.pow(out_list[0], out_list[1])
                actual_ans = eval(str(inter_ans) + t + str(out_list[7]))
            else:
                actual_ans = eval(str(out_list[0]) + o + str(out_list[1]) + t + str(out_list[7]))
            actual_ans = int(actual_ans)
            fakeans_list = [actual_ans + diff1, actual_ans - diff2, actual_ans + diff3]
            list_count = 0

        for x in range(0, 4):
            if x == sol_key:
                sol_print = actual_ans
            else:
                sol_print = fakeans_list[list_count]
                list_count += 1
            if x == 0:
                char = 'Q)'
            elif x == 1:
                char = 'W)'
            elif x == 2:
                char = 'E)'
            elif x == 3:
                char = 'R)'
            aSurf = BASICFONT.render(char + '   %s' % (sol_print), True, TEXTCOLOR)
            aRect = aSurf.get_rect()
            aRect.topleft = (20, 110 + x * 30)
            GAMEDISPLAY.blit(aSurf, aRect)
            if x == 3:
                list_count = 0

        # drawing landed blocks
        for i in range(0, len(landed)):
            for j in range(0, len(landed[i])):
                if (landed[i][j] != None):
                    landed[i][j].display(GAMEDISPLAY)
            block.display(GAMEDISPLAY)

        # drawing top cover
        GAMEDISPLAY.fill(BLACK, [0, 0, WIDTH, TOP_BOUNDARY])

        # draw level
        level_text = BASICFONT.render("level: " + str(level), True, WHITE)
        GAMEDISPLAY.blit(level_text, (RIGHT_BOUNDARY +
                                      LEFT_BOUNDARY / 10, HEIGHT / 20 - 20))

        # score
        screen_text = BASICFONT.render("score: " + str(score), True, WHITE)
        GAMEDISPLAY.blit(screen_text, (RIGHT_BOUNDARY +
                                       LEFT_BOUNDARY / 10, HEIGHT / 20 + 20))

        questionSurf = BASICFONT.render('Question :', True, TEXTCOLOR)
        questionRect = questionSurf.get_rect()
        questionRect.topleft = (20, 20)
        GAMEDISPLAY.blit(questionSurf, questionRect)

        answerSurf = BASICFONT.render('Answer :', True, TEXTCOLOR)
        answerRect = answerSurf.get_rect()
        answerRect.topleft = (20, 80)
        GAMEDISPLAY.blit(answerSurf, answerRect)

        if (diff1 < 9):
            qSurf = BASICFONT.render('%s %s %s' % (out_list[0], o, out_list[1]), True, TEXTCOLOR)
            qRect = qSurf.get_rect()
            qRect.topleft = (20, 50)
            GAMEDISPLAY.blit(qSurf, qRect)
        else:
            if out_list[8] == 0:
                t = '+'
            else:
                t = '-'
            qSurf = BASICFONT.render('%s %s %s %s %s' % (out_list[0], o, out_list[1], t, out_list[7]), True, TEXTCOLOR)
            qRect = qSurf.get_rect()
            qRect.topleft = (20, 50)
            GAMEDISPLAY.blit(qSurf, qRect)

        # draw compliment
        drawCompliment(comp_input)

        # drawing next blocks

        for i in range(0, len(nextBlocks)):
            nextBlocks[i].display(GAMEDISPLAY)

            # drawing hold
            if (holdBlock != None):
                holdBlock.display(GAMEDISPLAY)

        # collision checking
        if not hasMove:
            # clock.tick(10) - movement speed
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


def generateQues(level):
    if level <= 4:
        multi_var = randint(0, 10)
    else:
        multi_var = randint(0, 40)
    two_op = randint(0, 1)
    bound_list = calculateUpbound(level)
    o_upbound = bound_list[0]
    q1_upbound = bound_list[1]
    q2_upbound = bound_list[2]
    o_lbound = bound_list[3]
    operator = randint(o_lbound, o_upbound)
    if operator == 3:
        q2 = randint(1, q2_upbound)
        q1 = q2 * randint(0, q1_upbound)
    else:
        q2 = randint(0, q2_upbound)
        q1 = randint(0, q1_upbound)
    sol_key = randint(0, 3)
    if sol_key == 0:
        char = pygame.K_q
    if sol_key == 1:
        char = pygame.K_w
    if sol_key == 2:
        char = pygame.K_e
    if sol_key == 3:
        char = pygame.K_r
    diff1 = randint(1, 5)
    diff2 = randint(1, 10)
    diff3 = randint(6, 20)
    return [q1, q2, operator, sol_key, diff1, diff2, diff3, multi_var, two_op, char]


def calculateUpbound(level):
    if level == 1:
        o_upbound = 0
        o_lbound = 0
        q1_upbound = 9
        q2_upbound = 9

    elif level == 2:
        o_upbound = 1
        o_lbound = 0
        q1_upbound = 9
        q2_upbound = 9
    elif level == 3:
        o_upbound = 2
        o_lbound = 2
        q1_upbound = 9
        q2_upbound = 9
    elif level == 4:
        o_upbound = 3
        o_lbound = 2
        q1_upbound = 9
        q2_upbound = 9
    elif level == 5:
        o_upbound = 1
        o_lbound = 0
        q1_upbound = 9
        q2_upbound = 20
    elif level == 6:
        o_upbound = 1
        o_lbound = 0
        q1_upbound = 20
        q2_upbound = 20
    elif level == 7:
        o_upbound = 2
        o_lbound = 0
        q1_upbound = 20
        q2_upbound = 20
    elif level == 8:
        o_upbound = 3
        o_lbound = 0
        q1_upbound = 20
        q2_upbound = 20
    elif level == 9:
        o_upbound = 3
        o_lbound = 0
        q1_upbound = 40
        q2_upbound = 40
    elif level == 10:
        o_upbound = 4
        o_lbound = 4
        q1_upbound = 10
        q2_upbound = 5
    elif level >= 11:
        o_upbound = 3
        o_lbound = 0
        q1_upbound = 60
        q2_upbound = 60
    return [o_upbound, q1_upbound, q2_upbound, o_lbound]


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 80) + 1
    fallFreq = 0.8 - (level * 0.02)
    return level, fallFreq


def drawCompliment(rand):
    if rand == 10:
        compliment = "Welcome, player!"
    if rand == 0:
        compliment = "Great!"
    elif rand == 1:
        compliment = "Good job!"
    elif rand == 2:
        compliment = "Nice!"
    elif rand == 3:
        compliment = "Excellent!"
    elif rand == 4:
        compliment = "Incorrect input."
    elif rand == 5:
        compliment = "Nice try!"
    elif rand == 6:
        compliment = "Keep going!"
    elif rand == 7:
        compliment = "Better luck next time!"
    elif rand == -1:
        compliment = " "
    complimentSurf = BASICFONT.render(compliment, True, TEXTCOLOR)
    complimentRect = complimentSurf.get_rect()
    complimentRect.midtop = (WIDTH / 2, 20)
    GAMEDISPLAY.blit(complimentSurf, complimentRect)
    if rand == 4 or rand == 5 or rand == 6 or rand == 7:
        controlSurf = BASICFONT.render("Lost controls.", True, TEXTCOLOR)
        controlRect = controlSurf.get_rect()
        controlRect.topleft = (RIGHT_BOUNDARY + LEFT_BOUNDARY / 3 - 20, HEIGHT - 200)
        GAMEDISPLAY.blit(controlSurf, controlRect)


# =================================================================

def main():
    runGame()


if __name__ == '__main__':
    main()