# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, math
from pygame.locals import *
from random import randint

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Metris')

    showTextScreen('Metris')


    while True: # game loop
        num = randint(0, 4)
        if num == 0:
            pygame.mixer.music.load('tetrisb.mid')
        elif num == 1:
            pygame.mixer.music.load('ff7.mid')
        elif num == 2:
            pygame.mixer.music.load('eye.mid')
        elif num == 3:
            pygame.mixer.music.load('hip.mid')
        elif num == 4:
            pygame.mixer.music.load('mur.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)
    qSolved = False
    comp_input = 10
    o_upbound = 0
    q1_upbound = 0
    q2_upbound = 0
    o_lbound = 0
    multi_var = randint(0,10)
    two_op = randint(0,1)
    bound_list = calculateUpbound(level)
    o_upbound = bound_list[0]
    q1_upbound = bound_list[1]
    q2_upbound = bound_list[2]
    o_lbound = bound_list[3]
    operator = randint(o_lbound,o_upbound)
    if operator == 3:
        q2 = randint(1,q2_upbound)
        q1 = q2*randint(0, q1_upbound)
    else:
        q2 = randint(0,q2_upbound)
        q1 = randint(0,q1_upbound)
    sol_key = randint(0,3)
    if sol_key == 0:
        char = K_1
    if sol_key == 1:
        char = K_2
    if sol_key == 2:
        char = K_3
    if sol_key == 3:
        char = K_4
    controlsOn = False
    numTries = 0
    
    diff1 = randint(1, 10)
    diff2 = randint(1, 10)
    diff3 = randint(1, 20)
    num_q = 0
    scr_mult = 5

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            numTries = 0
            controlsOn = False
            num_q = 0
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showPauseScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w) and controlsOn == True:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q) and controlsOn == True: # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

                # check for correct answer
                elif event.key == char:
                    if numTries < 1:
                        hard_q = False
                        if (diff1 >= 9):
                            hard_q = True
                        bound_list = calculateUpbound(level)
                        o_upbound = bound_list[0]
                        q1_upbound = bound_list[1]
                        q2_upbound = bound_list[2]
                        o_lbound = bound_list[3]
                        if level <= 4:
                            multi_var = randint(0, 10)
                        else:
                            multi_var = randint(0, 40)
                        two_op = randint(0,1)
                        diff1 = randint(1, 10)
                        diff2 = randint(1, 10)
                        diff3 = randint(1, 20)
                        operator = randint(o_lbound,o_upbound)
                        if operator == 3:
                            q2 = randint(1,q2_upbound)
                            q1 = q2*randint(0, q1_upbound)
                        else:
                            q2 = randint(0,q2_upbound)
                            q1 = randint(0,q1_upbound)
                        sol_key = randint(0,3)
                        if sol_key == 0:
                            char = K_1
                        if sol_key == 1:
                            char = K_2
                        if sol_key == 2:
                            char = K_3
                        if sol_key == 3:
                            char = K_4
                        comp_input = randint(0,3)
                        controlsOn = True
                        score += 10 + scr_mult*num_q
                        if hard_q == True:
                            score += 20
                        hard_q = False
                        level,fallFreq = calculateLevelAndFallFreq(score)
                        num_q += 1
                elif event.key != char and (event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4):
                    numTries += 1
                    comp_input= randint(4,7)
                    controlsOn = False

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
                numTries = 0
                conrolsOn = False
                bound_list = calculateUpbound(level)
                if level <= 4:
                    multi_var = randint(0, 10)
                else:
                    multi_var = randint(0, 40)
                two_op = randint(0,1)
                diff1 = randint(1, 10)
                diff2 = randint(1, 10)
                diff3 = randint(1, 20)
                o_upbound = bound_list[0]
                q1_upbound = bound_list[1]
                q2_upbound = bound_list[2]
                o_lbound = bound_list[3]
                operator = randint(o_lbound,o_upbound)
                if operator == 3:
                    q2 = randint(1,q2_upbound)
                    q1 = q2*randint(0, q1_upbound)
                else:
                    q2 = randint(0,q2_upbound)
                    q1 = randint(0,q1_upbound)
                sol_key = randint(0,3)
                if sol_key == 0:
                    char = K_1
                if sol_key == 1:
                    char = K_2
                if sol_key == 2:
                    char = K_3
                if sol_key == 3:
                    char = K_4
                comp_input = -1
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level, q1, q2, operator, sol_key, diff1, diff2, diff3, multi_var, two_op)
        drawCompliment(comp_input)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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
        q2_upbound= 60
    return [o_upbound, q1_upbound, q2_upbound, o_lbound]

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPressPause():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.

    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                drawInstructions('Instructions')
            elif event.key == K_l:
                drawLeaderboard('Leaderboard')
            elif event.key == K_b:
                showPauseScreen('Pause')
            continue
        return event.key
    return None


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.

    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                drawInstructions('Instructions')
            elif event.key == K_l:
                drawLeaderboard('Leaderboard')
            elif event.key == K_b:
                showTextScreen('Metris')
            continue
        return event.key
    return None


def drawInstructions(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    DISPLAYSURF.fill(BLACK)
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 4) - 40)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 4) - 50)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Choose an answer by pressing keys 1, 2, 3, 4', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)-50)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Rotate block with UP/W key (Only after answering correctly)', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)-25)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Move the block with LEFT/A, RIGHT/D, DOWN/S', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Hard drop by pressing SPACE', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)+25)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Pause the game by pressing P', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)+50)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Exit the game pressing ESCAPE key', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)+75)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 170)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Instructions text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press B to go back', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 195)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() is None:
        pygame.display.update()
        FPSCLOCK.tick()


def drawLeaderboard(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    DISPLAYSURF.fill(BLACK)
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2) - 40)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 50)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 70)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Instructions text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press B to go back', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() is None:
        pygame.display.update()
        FPSCLOCK.tick()




def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    DISPLAYSURF.fill(BLACK)
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2) - 40)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 50)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 70)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Instructions text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press SPACE for instructions', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Leaderboard text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press L for Leaderboard', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 120)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


    while checkForKeyPress() is None:
        pygame.display.update()
        FPSCLOCK.tick()



def showPauseScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    DISPLAYSURF.fill(BLACK)
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2)-3, int(WINDOWHEIGHT / 2) - 40)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 50)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to continue.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 70)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Instructions text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press SPACE for instructions', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # Leaderboard text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press L for Leaderboard', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 120)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


    while checkForKeyPressPause() is None:
        pygame.display.update()
        FPSCLOCK.tick()



def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 80) + 1
    fallFreq = 0.8 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    if numLinesRemoved == 1:
        return 10*numLinesRemoved
    else:
        ret = 0
        multiplier = 1
        pt_score = 5
        for x in range(0, numLinesRemoved):
            ret += multiplier*pt_score
            multiplier += 1
        return ret


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level, q1, q2, operator, sol_key, diff1, diff2, diff3, multi_var, two_op):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

    # draw the question text
    questionSurf = BASICFONT.render('Question :', True, TEXTCOLOR)
    questionRect = questionSurf.get_rect()
    questionRect.topleft = (20, 20)
    DISPLAYSURF.blit(questionSurf, questionRect)
    if operator == 0:
        o = '+'
    elif operator == 1:
        o = '-'
    elif operator == 2:
        o = '*'
    elif operator == 3:
        o = '/'
    elif operator == 4:
        o = '^'
    if (diff1 < 9):
        qSurf = BASICFONT.render('%s %s %s' % (q1, o, q2) , True, TEXTCOLOR)
        qRect = qSurf.get_rect()
        qRect.topleft= (20, 50)
        DISPLAYSURF.blit(qSurf, qRect)
    else:
        if two_op == 0:
            t = '+'
        else:
            t = '-'
        qSurf = BASICFONT.render('%s %s %s %s %s' % (q1, o, q2, t, multi_var) , True, TEXTCOLOR)
        qRect = qSurf.get_rect()
        qRect.topleft= (20, 50)
        DISPLAYSURF.blit(qSurf, qRect)

    # draw answer text
    answerSurf = BASICFONT.render('Answer :', True, TEXTCOLOR)
    answerRect = answerSurf.get_rect()
    answerRect.topleft = (20, 80)
    DISPLAYSURF.blit(answerSurf, answerRect)

    if (diff1 < 9):
        if o == '^':
            actual_ans = math.pow(q1,q2)
        else:
            actual_ans = eval(str(q1) + o + str(q2))
        actual_ans = int(actual_ans)
        fakeans_list = [eval(str(q1) + o + str(q2)) + diff1, eval(str(q1) + o + str(q2)) - diff2, eval(str(q1) + o + str(q2)) + diff3]
        list_count = 0
    else:
        if o == '^':
            inter_ans = math.pow(q1,q2)
            actual_ans = eval(str(inter_ans) + t + str(multi_var))
        else:
            actual_ans = eval(str(q1) + o + str(q2) + t + str(multi_var))
        actual_ans = int(actual_ans)
        fakeans_list = [actual_ans + diff1, actual_ans - diff2, actual_ans + diff3]
        list_count = 0

    for x in range(0,4):
        if x == sol_key:
            sol_print = actual_ans
        else:
            sol_print = fakeans_list[list_count]
            list_count += 1
        if x == 0:
            char = '1)'
        elif x == 1:
            char = '2)'
        elif x == 2:
            char = '3)'
        elif x == 3:
            char = '4)'
        aSurf = BASICFONT.render(char + '   %s' % (sol_print), True, TEXTCOLOR)
        aRect = aSurf.get_rect()
        aRect.topleft = (20, 110+x*30)
        DISPLAYSURF.blit(aSurf, aRect)
        if x == 3:
            list_count = 0

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-150, pixely=100)

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
    complimentRect.midtop = (WINDOWWIDTH/2, 20)
    DISPLAYSURF.blit(complimentSurf, complimentRect)
    if rand == 4 or rand == 5 or rand == 6 or rand == 7:
        controlSurf = BASICFONT.render("Lost controls.", True, TEXTCOLOR)
        controlRect = controlSurf.get_rect()
        controlRect.topleft = (WINDOWWIDTH - 150, 200)
        DISPLAYSURF.blit(controlSurf, controlRect)


if __name__ == '__main__':
    main()
