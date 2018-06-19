import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import inputbox
import random, time, sys, math
import json
import datetime
import threading

from Block.BlockT import *
from Block.BlockO import *
from Block.BlockI import *
from Block.BlockL import *
from Block.BlockS import *
from Block.BlockZ import *
from Block.BlockJ import *

from menu import *

class Metris:

    def __init__(self):
        pass

    def makeGameObject(self):
        pygame.init()

        if pygame.display.get_surface() != None:
            self.GAMEDISPLAY = pygame.display.get_surface()
            self.HEIGHT = self.GAMEDISPLAY.get_height()
            self.WIDTH = self.GAMEDISPLAY.get_width()
        else:
            self.HEIGHT = 900
            self.WIDTH = self.HEIGHT * 4 / 3
            self.GAMEDISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption('Metris')
        # dirty = []
        # dirty.append(pygame.draw.rect(self.GAMEDISPLAY, (255, 255, 255),
        #                               pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)))
        # pygame.display.update(dirty)
        pygame.display.update()

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.GRAY = (185, 185, 185)
        self.BORDER_COLOR = (50, 50, 100)
        self.INNER_BG = (25, 25, 40)
        self.INNER_BG2 = (75, 75, 100)
        self.GRID_COLOR = (100, 100, 125)
        self.TEXTCOLOR = self.WHITE
        self.COMBOCOLOR = self.WHITE
        self.TEXTSHADOWCOLOR = self.GRAY
        self.COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
        self.COLORS2 = [(200,0,0), (0,200,0), (0,0,200), (200,200,0), (200,0,200)]
        self.random_color = []
        for i in range(0, 9):
            for j in range(0, 12):
                self.random_color.insert(len(self.random_color), randint(0, len(self.COLORS)-1))

        self.INSTRUCTION = ['Choose an answer by pressing keys 1, 2, 3, 4',
                       'Rotate-clockwise with UP key*',
                       'Rotate-counter-clockwise with Z key*',
                       'Move the block with LEFT, RIGHT, DOWN',
                       'Hard drop by pressing SPACE',
                       'Press Shift to hold the current piece'
                       'Pause the game by pressing P',
                       'Exit the game pressing ESCAPE key',
                       'Press B to go back',
                       'Press M to mute/unmute',
                       ]

        self.BLOCK_SIZE = self.HEIGHT / 28
        self.LEFT_BOUNDARY = self.WIDTH / 2 - 5 * self.BLOCK_SIZE
        self.RIGHT_BOUNDARY = self.WIDTH /2 + 5 * self.BLOCK_SIZE
        self.TOP_BOUNDARY = 4 * self.BLOCK_SIZE
        self.BOTTOM_BOUNDARY = self.TOP_BOUNDARY + 20 * self.BLOCK_SIZE
        self.INIT_X = self.LEFT_BOUNDARY + 5 * self.BLOCK_SIZE
        self.INIT_Y = 3*self.BLOCK_SIZE

        self.SCOREFONT = pygame.font.Font('freesansbold.ttf', self.BLOCK_SIZE * 3 / 4)
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', self.BLOCK_SIZE * 3 / 4)
        self.BASICFONT_OUTLINE = pygame.font.Font('freesansbold.ttf', self.BLOCK_SIZE * 3 / 4 + 2)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 2 * self.BLOCK_SIZE)
        self.TIMEFONT = pygame.font.Font('freesansbold.ttf', self.BLOCK_SIZE * 5 / 4)
        self.TIMEFONT2 = pygame.font.Font('freesansbold.ttf', 53)

        self.MID_FILES = ['mp3s/m0', 'mp3s/m1', 'mp3s/m2', 'mp3s/m3',
                        'mp3s/m4', 'mp3s/m5', 'mp3s/m6', 'mp3s/m7',
                        'mp3s/m8', 'mp3s/m9', 'mp3s/m10', 'mp3s/m11', 'mp3s/m12', 'mp3s/m13']

        self.score = 0

        self.gameExit = False

        self.dx = 0
        self.dy = 0
        self.first_touch = True
        self.hasMove = False
        # self.font = pygame.font.SysFont(None, 25)
        self.gone_down = False
        self.currentBlock = False
        self.block = None
        self.blockSet = []
        self.blockPlaced = False
        self.landed = [[None for i in range(24)] for j in range(10)]
        self.speed = 60
        self.bankedpoints = 0

        self.isSoundOn = True
        self.soundOn = pygame.image.load('images/soundon.png')  # @copyright from Robin Kylander in FLATICON
        self.soundOn.convert()
        self.soundOff = pygame.image.load('images/soundoff.png')  # @copyright from Robin Kylander in FLATICON
        self.soundOff.convert()
        self.soundPosition = (self.LEFT_BOUNDARY / 2, self.HEIGHT * 3 / 4)
        self.isMusicOn = True
        self.musicOn = pygame.image.load('images/musicon.png')  # @copyright from Freepik in FLATICON
        self.musicOn.convert()
        self.musicOff = pygame.image.load('images/musicoff.png')
        self.musicOff.convert()
        self.musicPosition = (self.LEFT_BOUNDARY / 2 + self.soundOn.get_rect().width + 5, self.HEIGHT * 3 / 4)

        self.clock = pygame.time.Clock()

        self.fallFreq = 1
        self.holdBlock = None # holdBlock is a int type specifying block type
        self.mult = 0
        self.level = 0
        self.total_lines = 0
        self.spin = False
        self.d_tspin = False
        self.t_tspin = False
        self.tetris = False
        self.triple = False
        self.double = False
        self.single = False

        self.main_menu = None

        self.MOVE = pygame.USEREVENT + 4
        self.accl = 500
        self.SLACK = pygame.USEREVENT + 5
        self.NOSLACK = pygame.USEREVENT + 6
        self.tolerance = False
        self.tolerable = True

        self.lock = threading.Lock()

    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #=================================================================================================


    def runGame(self):


        self.gameExit = False

        self.blockSet = self.getRandomBlockSet(None)
        nextBlocks = []

        mus_var = randint(0,12)
        pygame.mixer.music.load(self.MID_FILES[mus_var])
        pygame.mixer.music.play(-1, 0.0)
        if self.isMusicOn == False:
            pygame.mixer.music.pause()

        hasSwap = True

        self.calculateLevelAndFallFreq()
        self.level_prev = self.level
        self.qSolved = False
        comp_input = 10
        out_list = self.generateQues()
        controlsOn = False
        numTries = 0
        diff1 = out_list[4]
        num_q = 0
        self.mult = 0
        self.scr_mult = 5
        self.drawCompliment(comp_input)
        fontsize = self.BLOCK_SIZE * 3 / 4
        self.total_lines = 0

        TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(TICK, 1000)
        time = 300000
        # self.timeleft  = self.BASICFONT.render(str(time/1000/60) + " : " + str(time/1000 - (time/1000/60)*60), True, self.TEXTCOLOR)
        TIMEREMAINING = pygame.USEREVENT + 2
        pygame.time.set_timer(TIMEREMAINING, 1000)
    ##    TIMEUP = pygame.USEREVENT + 3
    ##    pygame.time.set_timer(TIMEUP, time)
        # self.MOVE = pygame.USEREVENT + 4
        pygame.time.set_timer(self.MOVE, 0)
        pygame.time.set_timer(self.SLACK, 0)
        pygame.time.set_timer(self.NOSLACK, 0)

        # drawing bg
        # self.GAMEDISPLAY.fill(self.BLACK, [0, 0, self.WIDTH, self.HEIGHT])
        # =========GRADIENT BG===================
        spacing = self.HEIGHT / 100
        for i in range(14, 100):
            self.GAMEDISPLAY.fill((100 + i, 105 + i, 155 + i), [0, spacing * i, self.WIDTH, spacing])

        while not self.gameExit:

            while Gtk.events_pending():
                Gtk.main_iteration()

            if self.bankedpoints > 0:
                self.score += 1
                self.bankedpoints -= 1

            # checkForQuit()
            for event in pygame.event.get():
    ##            if event.type == pygame.QUIT:
    ##                gameExit = True
                #======PARTIAL RESIZABLE WINDOW CODE=============
    ##            if event.type == pygame.VIDEORESIZE:
    ##                self.HEIGHT = event.h
    ##                self.WIDTH = self.HEIGHT * 7 / 6
    ##                self.GAMEDISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
    ##                self.LEFT_BOUNDARY = self.WIDTH / 3
    ##                self.RIGHT_BOUNDARY = self.WIDTH - self.WIDTH / 3
    ##                self.BLOCK_SIZE = (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 10
    ##                self.TOP_BOUNDARY = 4 * self.BLOCK_SIZE
    ##                self.BOTTOM_BOUNDARY = self.TOP_BOUNDARY + 20 * self.BLOCK_SIZE
    ##                self.INIT_X = self.LEFT_BOUNDARY + 5 * self.BLOCK_SIZE
    ##                self.INIT_Y = self.BLOCK_SIZE
                #==================================================
                # if event.type == pygame.VIDEORESIZE:
                #     self.GAMEDISPLAY = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                #     self.GAMEDISPLAY.fill(self.BLACK)
                #==================================================
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = self.soundOn.get_rect()
                    pos.x = self.soundPosition[0]
                    pos.y = self.soundPosition[1]
                    if pos.collidepoint(pygame.mouse.get_pos()):
                        self.flipSoundIcon()
                    pos.x = self.musicPosition[0]
                    pos.y = self.musicPosition[1]
                    if pos.collidepoint(pygame.mouse.get_pos()):
                        self.flipMusicIcon()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.dx = -self.BLOCK_SIZE
                        # self.move()
                        if self.dy is 0:
                            pygame.time.set_timer(self.MOVE, 250)
                        self.block.setX(self.block.getX() + self.dx)
                        if self.checkCollision():
                            self.block.setX(self.block.getX() - self.dx)

                    elif event.key == pygame.K_RIGHT:
                        self.dx = self.BLOCK_SIZE
                        # self.move()
                        if self.dy is 0:
                            pygame.time.set_timer(self.MOVE, 250)
                        self.block.setX(self.block.getX() + self.dx)
                        if self.checkCollision():
                            self.block.setX(self.block.getX() - self.dx)

                    elif event.key == pygame.K_DOWN:
                        self.dy = self.BLOCK_SIZE
                        self.playSound('beep.wav')
                        self.block.setY(self.block.getY() + self.dy)
                        if self.checkCollision():
                            self.block.setY(self.block.getY() - self.dy)
                        pygame.time.set_timer(self.MOVE, 100)

                    elif event.key == pygame.K_UP and controlsOn == True:
                        if self.currentBlock:
                            self.block.rotateR()
                            # self.spin = True
                            self.checkCollisionRotation()
                                # self.block.rotateL()
                            if self.checkCollision():
                                self.block.rotateL()
                                self.block.rotateR2()
                                if self.checkCollision():
                                    self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                    if self.checkCollision():
                                        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                        self.block.rotateL2()
                                        self.block.rotateR3()
                                        if self.checkCollision():
                                            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                            if self.checkCollision():
                                                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                                self.block.rotateL3()
                                                self.block.rotateR4()
                                                if self.checkCollision():
                                                    self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                                    if self.checkCollision():
                                                        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                                        self.block.rotateL4()
                                                        self.spin = False
                                if self.tolerable:
                                    self.tolerance = True
                                    pygame.time.set_timer(self.SLACK, 2500 - self.fallFreq*2)
                            else:
                                self.spin = False
                                if self.tolerable:
                                    self.tolerance = True
                                    pygame.time.set_timer(self.SLACK, 2500 - self.fallFreq*2)
                            # elif self.checkBlockCollision():
                            #     self.block.rotateL4()

                    elif event.key == pygame.K_z and controlsOn == True:
                        if self.currentBlock:
                            self.block.rotateL()
                            # self.spin = True
                            self.checkCollisionRotation()
                            #     self.block.rotateR4()
                            if self.checkCollision():
                                self.block.rotateR()
                                self.block.rotateL2()
                                # self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                # if self.checkCollision():
                                #     self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                #     if self.checkCollision():
                                if self.checkCollision():
                                    self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                    if self.checkCollision():
                                        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                        self.block.rotateR2()
                                        self.block.rotateL3()
                                        if self.checkCollision():
                                            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                            if self.checkCollision():
                                                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                                self.block.rotateR3()
                                                self.block.rotateL4()
                                                if self.checkCollision():
                                                    self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                                    if self.checkCollision():
                                                        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                                        self.block.rotateR4()
                                                        # self.spin = False
                                if self.tolerable:
                                    self.tolerance = True
                                    pygame.time.set_timer(self.SLACK, 2000)
                            else:
                                # self.spin = False
                                if self.tolerable:
                                    self.tolerance = True
                                    pygame.time.set_timer(self.SLACK, 2000)
                            # elif self.checkBlockCollision():
                            #     self.block.rotateR4()

                    elif event.key == pygame.K_SPACE:
                        while not self.checkCollision():
                            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                        self.tolerance = False
                        self.tolerable = False
                        self.tick()

                    elif event.key == pygame.K_p:
                        self.mult = 0
                        self.paused()
                        out_list = self.generateQues()

                    elif event.key == pygame.K_LSHIFT:
                        if hasSwap:
                            self.hold(nextBlocks)
                            out_list = self.generateQues()
                            self.mult = 0
                            hasSwap = False
                    elif event.key == pygame.K_m:
                        self.flipMusicIcon()
                    elif event.key == pygame.K_s:
                        self.flipSoundIcon()
                    # check for correct answer
                    elif event.key == out_list[9]:
                        self.playSound('cor.wav')
                        if numTries < 1:
                            hard_q = False
                            if diff1 > 4:
                                hard_q = True
                            controlsOn = True
                            if num_q <= 5:
                                self.bankedpoints += 10 + 5 * self.mult
                                self.mult += 1
                                if hard_q:
                                    self.bankedpoints += 20
                            self.hard_q = False
                            self.calculateLevelAndFallFreq()
                            num_q += 1
                            out_list = self.generateQues()
                            diff1 = out_list[4]
                            if num_q > 5:
                                comp_input = 8
                            else:
                                comp_input = randint(0,3)
                    elif event.key != out_list[9] and (
                            event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4):
                        numTries += 1
                        self.mult = 0
                        if num_q <= 5 and numTries <= 1:
                            controlsOn = False
                            self.playSound('incor.wav')
                            comp_input = randint(4, 7)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        if self.dx < 0:
                            self.dx = 0
                            if self.dy is 0:
                                pygame.time.set_timer(self.MOVE, 0)
                        # self.accl = 500
                    if event.key == pygame.K_RIGHT:
                        if self.dx > 0:
                            self.dx = 0
                            if self.dy is 0:
                                pygame.time.set_timer(self.MOVE, 0)
                        # self.accl = 500
                    if event.key == pygame.K_DOWN:
                        self.dy = 0
                        pygame.time.set_timer(self.MOVE, 0)
                if event.type == TICK:
                    self.tick()
                if event.type == self.MOVE:
                    self.move()
                #=============TIMED METRIS============
                if event.type == TIMEREMAINING:
                    time -= 1000
                    if time <= 0:
                        self.gameOver()
                #=====================================
                if event.type == self.SLACK:
                    self.tolerance = False
                    pygame.time.set_timer(self.SLACK, 0)
                if event.type == self.NOSLACK:
                    self.tolerance = False
                    self.tolerable = True
                    pygame.time.set_timer(self.NOSLACK, 0)


            # drawing bg
            # =========GRADIENT BG===================
            spacing = self.HEIGHT / 100
            for i in range(85, 100):
                self.GAMEDISPLAY.fill((100 + i, 105 + i, 155 + i), [0, spacing * i, self.WIDTH, spacing])

            #=========RANDOM BLOCK BG===============
            # selector = 0
            # for i in range (0, 10):
            #     for j in range (0, 12):
            #         self.GAMEDISPLAY.fill((0, 150, 200),
            #                               [i*4*self.BLOCK_SIZE, j*4*self.BLOCK_SIZE, 3.5*self.BLOCK_SIZE,
            #                                3.5*self.BLOCK_SIZE])
            #         self.GAMEDISPLAY.fill((0, 100, 150),
            #                               [i*4*self.BLOCK_SIZE + self.BLOCK_SIZE/4, j*4* self.BLOCK_SIZE + self.BLOCK_SIZE/4,
            #                                3.5*self.BLOCK_SIZE - 0.5*self.BLOCK_SIZE, 3.5 * self.BLOCK_SIZE - 0.5*self.BLOCK_SIZE])
            #         selector += 1
            # drawing game bg
            self.GAMEDISPLAY.fill(self.INNER_BG2, [self.LEFT_BOUNDARY, self.TOP_BOUNDARY, 10 * self.BLOCK_SIZE, 20 * self.BLOCK_SIZE])
            self.GAMEDISPLAY.fill(self.INNER_BG, [self.LEFT_BOUNDARY + self.BLOCK_SIZE / 2, self.TOP_BOUNDARY + self.BLOCK_SIZE / 2, 9 * self.BLOCK_SIZE, 19 * self.BLOCK_SIZE])
            # drawing hold bg
            self.GAMEDISPLAY.fill(self.INNER_BG2, [self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 12 * self.BLOCK_SIZE, 8 * self.BLOCK_SIZE, 5 * self.BLOCK_SIZE])
            self.GAMEDISPLAY.fill(self.INNER_BG, [self.RIGHT_BOUNDARY + 1.5 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 12.5 * self.BLOCK_SIZE, 7 * self.BLOCK_SIZE, 4 * self.BLOCK_SIZE])
            # drawing next block bg
            self.GAMEDISPLAY.fill(self.INNER_BG2, [self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 6 * self.BLOCK_SIZE, 8 * self.BLOCK_SIZE, 5 * self.BLOCK_SIZE])
            self.GAMEDISPLAY.fill(self.INNER_BG, [self.RIGHT_BOUNDARY + 1.5 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 6.5 * self.BLOCK_SIZE, 7 * self.BLOCK_SIZE, 4 * self.BLOCK_SIZE])
            # drawing QA bg
            self.GAMEDISPLAY.fill(self.INNER_BG2, [self.BLOCK_SIZE, self.TOP_BOUNDARY, self.LEFT_BOUNDARY - 2 * self.BLOCK_SIZE, 10*self.BLOCK_SIZE])
            self.GAMEDISPLAY.fill(self.INNER_BG, [1.5 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 0.5 * self.BLOCK_SIZE, self.LEFT_BOUNDARY - 3 * self.BLOCK_SIZE, 9 * self.BLOCK_SIZE])
            # drawing stats bg
            self.GAMEDISPLAY.fill(self.INNER_BG2, [self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY, 8 * self.BLOCK_SIZE, 5 * self.BLOCK_SIZE])
            self.GAMEDISPLAY.fill(self.INNER_BG, [self.RIGHT_BOUNDARY + 1.5 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 0.5 * self.BLOCK_SIZE, 7 * self.BLOCK_SIZE, 4 * self.BLOCK_SIZE])

            # draw grid lines
            self.drawGridLines()

            # drawing block objs
            if not self.currentBlock and not self.gameExit:
                # calculating new questions
                self.calculateLevelAndFallFreq()
                numTries = 0
                controlsOn = True
                out_list = self.generateQues()
                diff1 = out_list[4]
                char = out_list[9]
                comp_input = -1
                num_q = 0
                self.mult = 0

                # setting new fall frequency
                pygame.time.set_timer(TICK, self.fallFreq)

                # draw new block
                self.newBlock(nextBlocks)
                self.currentBlock = True
                self.first_touch = True
                self.spin = False
                self.tolerance = False
                self.tolerable = True
                hasSwap = True

            # drawing shadow
            if not self.block is None:
                difference = self.getShadowDifference(self.block.getPerimeter())
                self.drawShadow(self.block.getPerimeter(), difference)

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

            if (diff1 < 5):
                if o == '^':
                    actual_ans = math.pow(out_list[0], out_list[1])
                else:
                    actual_ans = eval(str(out_list[0]) + o + str(out_list[1]))
                actual_ans = int(actual_ans)
                fakeans_list = [actual_ans + diff1, actual_ans - diff2, actual_ans + diff3]
                list_count = 0
            else:
                if out_list[8] == 0:
                    t = '+'
                else:
                    t = '-'
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
                    char = '1)'
                elif x == 1:
                    char = '2)'
                elif x == 2:
                    char = '3)'
                elif x == 3:
                    char = '4)'
                aSurf = self.BASICFONT.render(char + '   %s' % (sol_print), True, self.TEXTCOLOR)
                aRect = aSurf.get_rect()
                aRect.topleft = (self.BLOCK_SIZE * 2, self.TOP_BOUNDARY + (x + 5) * self.BLOCK_SIZE)
                self.GAMEDISPLAY.blit(aSurf, aRect)
                if x == 3:
                    list_count = 0

            # drawing landed blocks
            for i in range(0, len(self.landed)):
                for j in range(0, len(self.landed[i])):
                    if (self.landed[i][j] != None):
                        self.landed[i][j].display(self.GAMEDISPLAY)
                self.block.display(self.GAMEDISPLAY)

            # drawing top cover
            # self.GAMEDISPLAY.fill((0,150,200), [0, 0, self.WIDTH, self.TOP_BOUNDARY])
            for i in range (0, 14):
                self.GAMEDISPLAY.fill((100+i, 105+i, 155+i), [0, spacing*i, self.WIDTH, spacing])

            # drawing timeleft ======================TIMED METRIS=================
            if time / 1000 - (time / 1000 / 60) * 60 < 10:
                timeleft_text_shadow = self.TIMEFONT.render(str(time / 1000 / 60) + " : 0" + str(time / 1000 - (time / 1000 / 60) * 60), True, (50, 50, 100))
                timeleft_text = self.TIMEFONT.render(str(time/1000/60) + " : 0" + str(time/1000 - (time/1000/60)*60), True, (255,255,0))
                time_rect = timeleft_text.get_rect()
                time_rect.center = (self.WIDTH/2, self.TOP_BOUNDARY - 1.5 * self.BLOCK_SIZE)
                time_shadow_rect = timeleft_text.get_rect()
                time_shadow_rect.center = (self.WIDTH / 2 + 5, self.TOP_BOUNDARY - 1.5 * self.BLOCK_SIZE + 5)
            else:
                timeleft_text_shadow = self.TIMEFONT.render(str(time / 1000 / 60) + " : " + str(time / 1000 - (time / 1000 / 60) * 60), True, (50, 50, 100))
                timeleft_text = self.TIMEFONT.render(str(time/1000/60) + " : " + str(time/1000 - (time/1000/60)*60), True, (255,255,0))
                time_rect = timeleft_text.get_rect()
                time_rect.center = (self.WIDTH/2, self.TOP_BOUNDARY - 1.5 * self.BLOCK_SIZE)
                time_shadow_rect = timeleft_text.get_rect()
                time_shadow_rect.center = (self.WIDTH / 2 + 5, self.TOP_BOUNDARY - 1.5 * self.BLOCK_SIZE + 5)
            self.GAMEDISPLAY.blit(timeleft_text_shadow, time_shadow_rect)
            self.GAMEDISPLAY.blit(timeleft_text, time_rect)
            #=====================================================================

            # draw self.score, self.level, multiplier
            self.drawVarsBorder()

            level_text = self.BASICFONT.render("Level: " + str(self.level), True, self.WHITE)
            self.GAMEDISPLAY.blit(level_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 0.5 * self.BLOCK_SIZE))

            #==============POP UP SCORE=====================================
            if self.bankedpoints > 0 and fontsize < self.BLOCK_SIZE * 3 / 4 + 6:
                fontsize += 1
            if self.bankedpoints is 0 and fontsize > self.BLOCK_SIZE * 3 / 4:
                fontsize -= 1
            self.SCOREFONT = pygame.font.Font('freesansbold.ttf', fontsize)
            screen_text = self.BASICFONT.render("Score: ", True, self.WHITE)
            score_text = self.SCOREFONT.render("            " + str(self.score), True, self.WHITE) #=====================
            self.GAMEDISPLAY.blit(score_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 1.5 * self.BLOCK_SIZE)) #=========
            self.GAMEDISPLAY.blit(screen_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 1.5 * self.BLOCK_SIZE))
            #=================================================================

            prt_scr = 10 + self.mult * 5
            if diff1 >= 5:
                prt_scr += 20
            if num_q > 5:
                prt_scr = 0
            val_text = self.BASICFONT.render("Question worth: " + str(prt_scr), True, self.WHITE)
            self.GAMEDISPLAY.blit(val_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 2.5 * self.BLOCK_SIZE))

            #=============LINES CLEARED======================================
            lines_text = self.BASICFONT.render("Lines Cleared: " + str(self.total_lines), True, self.WHITE)
            self.GAMEDISPLAY.blit(lines_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 3.5 * self.BLOCK_SIZE))


            # drawing next blocks
            for i in range(0, len(nextBlocks)):
                nextBlocks[i].display(self.GAMEDISPLAY)

            # draw next blocks border
            self.drawNextBlocksBorder()

            # draw next blocks label
            self.drawNextBlocksLabel()

            # drawing hold
            self.drawHoldBlock(self.holdBlock)

            # draw hold border
            self.drawHoldBorder()

            # draw hold label
            self.drawHoldLabel()

            # draw game area border
            self.drawGameAreaBorder()

            # draw question & answer border
            self.drawQuesAnsBorder()

            questionSurf = self.BASICFONT.render('Question :', True, self.TEXTCOLOR)
            questionRect = questionSurf.get_rect()
            questionRect.topleft = (2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(questionSurf, questionRect)

            answerSurf = self.BASICFONT.render('Answer :', True, self.TEXTCOLOR)
            answerRect = answerSurf.get_rect()
            answerRect.topleft = (2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 4 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(answerSurf, answerRect)

            if (diff1 < 5):
                qSurf = self.BASICFONT.render('%s %s %s' % (out_list[0], o, out_list[1]), True, self.TEXTCOLOR)
                qRect = qSurf.get_rect()
                qRect.topleft = (2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 2 * self.BLOCK_SIZE)
                self.GAMEDISPLAY.blit(qSurf, qRect)
            else:
                if out_list[8] == 0:
                    t = '+'
                else:
                    t = '-'
                qSurf = self.BASICFONT.render('%s %s %s %s %s' % (out_list[0], o, out_list[1], t, out_list[7]), True, self.TEXTCOLOR)
                qRect = qSurf.get_rect()
                qRect.topleft = (2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 2 * self.BLOCK_SIZE)
                self.GAMEDISPLAY.blit(qSurf, qRect)

            # draw compliment
            self.drawCompliment(comp_input)

            self.drawCombo()

            self.drawSoundIcon()
            self.drawMusicIcon()
            #======= NEW SONG EVERY NEW LEVEL ==========
            # if self.level_prev != self.level:
            #     old_var = mus_var
            #     while mus_var == old_var:
            #         mus_var = randint(0,12)
            #     pygame.mixer.music.load(self.MID_FILES[mus_var])
            #     self.level_prev = self.level
            #     pygame.mixer.music.play(-1,0.0)
            #     if self.isMusicOn == False:
            #         pygame.mixer.music.pause()

            pygame.display.update()

            self.clock.tick(self.speed)
            self.hasMove = False

        self.currentBlock = False
        self.block = None
        self.score = 0
        for i in range(0, len(self.landed)):
            for j in range(0, len(self.landed[i])):
                self.landed[i][j] = None
        self.holdBlock = None

    ##    pygame.quit()
    ##    quit()

    #================================END OF RUN GAME==========================


    def tick(self):
        if self.gameExit:
            return
        if self.tolerable and (self.dy is not 0 or self.dx is not 0):
            self.tolerance = True
            pygame.time.set_timer(self.SLACK, 1100 - self.fallFreq)

        #self.lock.acquire()
        if self.block != None:
            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
            if self.checkCollision():
                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                if not self.tolerance:  # self.dy is 0:
                    self.COMBOCOLOR = self.block.getColor()
                    self.spin = self.checkForSpin()
                    self.currentBlock = False
                if self.tolerance:  # self.dy is not 0:
                    self.tolerable = False
                    # self.first_touch = False
                    pygame.time.set_timer(self.NOSLACK, 1500)
            if not self.currentBlock:
                for i in range(0, len(self.block.getPerimeter())):
                    self.landed[self.x2Index(self.block.getPerimeter()[i].getX())][self.y2Index(self.block.getPerimeter()[i].getY())] = \
                        self.block.getPerimeter()[i]
                self.checkLandedAndDelete()
                self.playSound('landSound.wav')
                self.checkGameOver()
        #self.lock.release()

    def checkLandedAndDelete(self):
        y = 0
        rowsToDelete = []
        while (y < len(self.landed[0])):
            if (self.rowFilled(y)):
                rowsToDelete.insert(len(rowsToDelete), y)
            y = y + 1
        self.deleteRows(rowsToDelete)


    def rowFilled(self, y):
        for x in range(0, len(self.landed)):
            if self.landed[x][y] == None:
                return False
        return True

    def checkForSpin(self):
        if self.block == None:
            return False
        self.block.setY(self.block.getY() - self.BLOCK_SIZE)
        if self.checkCollision():
            self.block.setY(self.block.getY() + 2 * self.BLOCK_SIZE)
            if self.checkCollision():
                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                self.block.setX(self.block.getX() - self.BLOCK_SIZE)
                if self.checkCollision():
                    self.block.setX(self.block.getX() + 2 * self.BLOCK_SIZE)
                    if self.checkCollision():
                        self.block.setX(self.block.getX() - self.BLOCK_SIZE)
                        return True
                    else:
                        self.block.setX(self.block.getX() - self.BLOCK_SIZE)
                        return False
                else:
                    self.block.setX(self.block.getX() + self.BLOCK_SIZE)
                    return False
            else:
                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                return False
        else:
            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
            return False

    def deleteRows(self, rows):
        self.total_lines += len(rows)
        # delete rows
        for i in range(0, len(rows)):
            for x in range(0, len(self.landed)):
                self.landed[x][rows[i]] = None
        # move rows above deleted rows down
        for i in range(0, len(rows)):
            for y in range(rows[i], 0, -1):
                for x in range(0, len(self.landed)):
                    if y > 0:
                        if self.landed[x][y - 1] != None:
                            self.landed[x][y - 1].setRelativeY(self.BLOCK_SIZE)
                        self.landed[x][y] = self.landed[x][y - 1]
            self.playSound('clr.wav')

        self.d_tspin = False
        self.t_tspin = False
        self.tetris = False
        self.triple = False
        self.double = False
        self.single = False

        # update self.score
        if len(rows) == 1:
            self.bankedpoints += 10
            self.single = True
        else:
            ret = 0
            multiplier = 1
            pt_score = 5
            if self.spin and len(rows) == 2 and type(self.block) == BlockT:
                self.d_tspin = True
            elif self.spin and len(rows) == 3 and type(self.block) == BlockT:
                self.t_tspin = True
            elif len(rows) == 2:
                self.double = True
            elif len(rows) == 3:
                self.triple = True
            elif len(rows) == 4:
                self.tetris = True
            for x in range(0, len(rows)):
                ret += multiplier * pt_score
                multiplier += 1
            self.bankedpoints += ret


    def checkGameOver(self):
        done = False
        for y in range(0, len(self.landed[0]) - 20):
            if done:
                break
            for x in range(0, len(self.landed)):
                if self.landed[x][y] != None:
                    self.gameOver()
                    done = True
                    break



    def checkCollision(self):
        if not self.currentBlock:
            return False
        blockPerimeter = self.block.getPerimeter()
        for i in range(0, len(blockPerimeter)):
            for j in range(0, len(self.landed)):
                for k in range(0, len(self.landed[j])):
                    if self.landed[j][k] != None:
                        if blockPerimeter[i].getX() == self.landed[j][k].getX() and blockPerimeter[i].getY() == self.landed[j][
                            k].getY():
                            return True
        for i in range(0, len(blockPerimeter)):
            if blockPerimeter[i].getX() < self.LEFT_BOUNDARY or blockPerimeter[i].getX() > self.RIGHT_BOUNDARY - self.BLOCK_SIZE or \
                    blockPerimeter[i].getY() > self.BOTTOM_BOUNDARY - self.BLOCK_SIZE:
                return True

    def checkBlockCollision(self):
        if not self.currentBlock:
            return False
        self.isCollision = False
        blockPerimeter = self.block.getPerimeter()
        for i in range(0, len(blockPerimeter)):
            for j in range(0, len(self.landed)):
                for k in range(0, len(self.landed[j])):
                    if self.landed[j][k] is not None:
                        isCollision = False
                        if blockPerimeter[i].getX() == self.landed[j][k].getX() and blockPerimeter[i].getY() == self.landed[j][k].getY():
                            self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                            if self.checkCollision():
                                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                isCollision = True

                            if self.checkCollision():
                                self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                                if self.checkCollision():
                                    self.block.setY(self.block.getY() + self.BLOCK_SIZE)
                                    return isCollision
        return False


    def checkCollisionRotation(self):
        if not self.currentBlock:
            return False
        blockPerimeter = self.block.getPerimeter()

        for i in range(0, len(blockPerimeter)):
            if blockPerimeter[i].getX() < self.LEFT_BOUNDARY - self.BLOCK_SIZE:
                self.block.setX(self.block.getX() + 2 * self.BLOCK_SIZE)
                # self.checkBlockCollision()
                if self.checkCollision():
                    self.block.setX(self.block.getX() - 2 * self.BLOCK_SIZE)
                    return True
                break
            elif blockPerimeter[i].getX() > self.RIGHT_BOUNDARY:
                self.block.setX(self.block.getX() - 2 * self.BLOCK_SIZE)
                # self.checkBlockCollision()
                if self.checkCollision():
                    self.block.setX(self.block.getX() + 2 * self.BLOCK_SIZE)
                    return True
                break
            # elif blockPerimeter[i].getY() > self.BOTTOM_BOUNDARY:
            #     self.block.setY(self.block.getY() - 2 * self.BLOCK_SIZE)
            #     self.checkBlockCollision()
            #     if self.checkCollision():
            #         self.block.setY(self.block.getX() + 2 * self.BLOCK_SIZE)
            #         return True
            #     break
        for i in range(0, len(blockPerimeter)):
            if blockPerimeter[i].getX() < self.LEFT_BOUNDARY:
                self.block.setX(self.block.getX() + self.BLOCK_SIZE)
                # self.checkBlockCollision()
                if self.checkCollision():
                    self.block.setX(self.block.getX() - self.BLOCK_SIZE)
                    return True
                break
            elif blockPerimeter[i].getX() > self.RIGHT_BOUNDARY - self.BLOCK_SIZE:
                self.block.setX(self.block.getX() - self.BLOCK_SIZE)
                # self.checkBlockCollision()
                if self.checkCollision():
                    self.block.setX(self.block.getX() + self.BLOCK_SIZE)
                    return True
                break
            elif blockPerimeter[i].getY() > self.BOTTOM_BOUNDARY - self.BLOCK_SIZE:
                # self.block.setY(self.block.getY() - self.BLOCK_SIZE)
                # self.checkBlockCollision()
                if self.checkCollision():
                    # self.block.setY(self.block.getX() + self.BLOCK_SIZE)
                    return True
                break
        return False


    def x2Index(self, x):
        return (x - self.LEFT_BOUNDARY) / self.BLOCK_SIZE


    def y2Index(self, y):
        return y / self.BLOCK_SIZE


    ## function to get the minimum vertical difference between current block and
    #  the bottom self.landed Blocks
    def getShadowDifference(self, blockList):
        maxIndex = len(self.landed[0]) - 1
        difference = maxIndex * self.BLOCK_SIZE - blockList[0].getY()
        for i in range(0, len(blockList)):
            if difference > maxIndex * self.BLOCK_SIZE - blockList[i].getY():
                difference = maxIndex * self.BLOCK_SIZE - blockList[i].getY()
        for i in range(0, len(blockList)):
            currX = self.x2Index(blockList[i].getX())
            currY = self.y2Index(blockList[i].getY())
            for y in range(currY, len(self.landed[0])):
                if self.landed[currX][y] != None and difference > y * self.BLOCK_SIZE - blockList[i].getY() - self.BLOCK_SIZE:
                    difference = y * self.BLOCK_SIZE - blockList[i].getY() - self.BLOCK_SIZE
        return difference


    def drawShadow(self, blockList, dist_y):
        for i in range(0, len(blockList)):
            pygame.draw.rect(self.GAMEDISPLAY, blockList[i].getColor(),
                             [blockList[i].getX() + self.BLOCK_SIZE/10, blockList[i].getY() + dist_y + self.BLOCK_SIZE/10,
                              self.BLOCK_SIZE - self.BLOCK_SIZE/5, self.BLOCK_SIZE - self.BLOCK_SIZE/5])
            pygame.draw.rect(self.GAMEDISPLAY, self.INNER_BG,
                             [blockList[i].getX() + self.BLOCK_SIZE/8, blockList[i].getY() + dist_y + self.BLOCK_SIZE/8,
                              self.BLOCK_SIZE - self.BLOCK_SIZE/4, self.BLOCK_SIZE - self.BLOCK_SIZE/4])


    def getRandomBlockSet(self, lastBlock):
        set = [0, 1, 2, 3, 4, 5, 6]
        shuffle(set)
        if set[0] == lastBlock:
            tmp = set[0]
            set[0] = set[1]
            set[1] = tmp
        return set


    def getOffsetX(self, blockType):
        if blockType == 0:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 1:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 2:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 3:
            return 0
        elif blockType == 4:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 5:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 6:
            return 0
        return 0


    def getOffsetY(self, blockType):
        if blockType == 0:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 1:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 2:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 3:
            return 0
        elif blockType == 4:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 5:
            return int(0.5 * self.BLOCK_SIZE)
        elif blockType == 6:
            return int(0.5 * self.BLOCK_SIZE)
        return 0

    def getBlockType(self):
        if type(self.block) == BlockT:
            return 0
        elif type(self.block) == BlockS:
            return 1
        elif type(self.block) == BlockJ:
            return 2
        elif type(self.block) == BlockI:
            return 3
        elif type(self.block) == BlockL:
            return 4
        elif type(self.block) == BlockZ:
            return 5
        elif type(self.block) == BlockO:
            return 6


    def hold(self, nextBlocks):
        tmp = self.holdBlock
        self.holdBlock = self.getBlockType()

        if tmp != None:
            self.blockSet.insert(0, tmp)

        self.newBlock(nextBlocks)
        self.setNextBlocks(nextBlocks)

    def drawHoldBlock(self, blockType):
        if blockType is None:
            return

        block = None;
        # self.holdBlock = None
        offset_x = self.RIGHT_BOUNDARY + self.BLOCK_SIZE * 4
        offset_y = self.TOP_BOUNDARY + self.BLOCK_SIZE * 14
        offset_x += self.getOffsetX(blockType)
        offset_y += self.getOffsetY(blockType)

        if blockType == 0:
            block = BlockT(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 1:
            block = BlockS(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 2:
            block = BlockJ(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 3:
            block = BlockI(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 4:
            block = BlockL(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 5:
            block = BlockZ(offset_x, offset_y, self.BLOCK_SIZE)
        elif blockType == 6:
            block = BlockO(offset_x, offset_y, self.BLOCK_SIZE)

        block.display(self.GAMEDISPLAY)

    def blockListTooShort(self, len):
        return (len <= 1)

    def appendBlockList(self):
        nextBlockSet = self.getRandomBlockSet(self.blockSet[len(self.blockSet) - 1])
        for i in range(0, len(nextBlockSet)):
            self.blockSet.insert(len(self.blockSet), nextBlockSet[i])

    def setNextBlocks(self, nextBlocks):
        while (len(nextBlocks) != 0):
            nextBlocks.pop()

        y_spacing = self.BLOCK_SIZE * 5
        offset_y = self.TOP_BOUNDARY + self.BLOCK_SIZE * 8
        offset_x = self.RIGHT_BOUNDARY + self.BLOCK_SIZE * 4

        for i in range(0, 1):
            if self.blockSet[i] == 0:
                nextBlocks.insert(i, BlockT(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 1:
                nextBlocks.insert(i, BlockS(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 2:
                nextBlocks.insert(i, BlockJ(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 3:
                nextBlocks.insert(i, BlockI(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 4:
                nextBlocks.insert(i, BlockL(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 5:
                nextBlocks.insert(i, BlockZ(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))
            elif self.blockSet[i] == 6:
                nextBlocks.insert(i, BlockO(offset_x + self.getOffsetX(self.blockSet[i]),
                                            i * y_spacing + offset_y + self.getOffsetY(self.blockSet[i]), self.BLOCK_SIZE))

    def drawHoldBorder(self):
        BORDER_WIDTH = 2
        borderList = [(self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 12 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 12 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 17 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 17 * self.BLOCK_SIZE)]
        pygame.draw.lines(self.GAMEDISPLAY, self.BORDER_COLOR, True, borderList, BORDER_WIDTH)


    def drawHoldLabel(self):
        screen_text = self.BASICFONT.render("Hold: ", True, self.WHITE)
        self.GAMEDISPLAY.blit(screen_text, (self.RIGHT_BOUNDARY + 1.2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 12.2 * self.BLOCK_SIZE))


    def drawNextBlocksBorder(self):
        BORDER_WIDTH = 2
        borderList = [(self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 6 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 6 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 11 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 11 * self.BLOCK_SIZE)]
        pygame.draw.lines(self.GAMEDISPLAY, self.BORDER_COLOR, True, borderList, BORDER_WIDTH)


    def drawNextBlocksLabel(self):
        screen_text = self.BASICFONT.render("Next: ", True, self.WHITE)
        self.GAMEDISPLAY.blit(screen_text, (self.RIGHT_BOUNDARY + 1.2 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 6.2 * self.BLOCK_SIZE))


    def drawVarsBorder(self):
        BORDER_WIDTH = 2
        borderList = [(self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY), (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY),
                      (self.RIGHT_BOUNDARY + 9 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 5 * self.BLOCK_SIZE),
                      (self.RIGHT_BOUNDARY + self.BLOCK_SIZE, self.TOP_BOUNDARY + 5 * self.BLOCK_SIZE)]
        pygame.draw.lines(self.GAMEDISPLAY, self.BORDER_COLOR, True, borderList, BORDER_WIDTH)


    def drawQuesAnsBorder(self):
        BORDER_WIDTH = 2
        borderList = [(self.BLOCK_SIZE, self.TOP_BOUNDARY),
                      (self.LEFT_BOUNDARY - self.BLOCK_SIZE, self.TOP_BOUNDARY),
                      (self.LEFT_BOUNDARY - self.BLOCK_SIZE, self.TOP_BOUNDARY + 10 * self.BLOCK_SIZE),
                      (self.BLOCK_SIZE, self.TOP_BOUNDARY + 10 * self.BLOCK_SIZE)]
        pygame.draw.lines(self.GAMEDISPLAY, self.BORDER_COLOR, True, borderList, BORDER_WIDTH)


    def drawGameAreaBorder(self):
        BORDER_WIDTH = 4
        borderList = [(self.LEFT_BOUNDARY - BORDER_WIDTH/2, self.TOP_BOUNDARY - BORDER_WIDTH/2),
                      (self.LEFT_BOUNDARY + 10 * self.BLOCK_SIZE, self.TOP_BOUNDARY - BORDER_WIDTH/2),
                      (self.LEFT_BOUNDARY + 10 * self.BLOCK_SIZE, self.TOP_BOUNDARY + 20 * self.BLOCK_SIZE),
                      (self.LEFT_BOUNDARY - BORDER_WIDTH/2, self.TOP_BOUNDARY + 20 * self.BLOCK_SIZE)]
        pygame.draw.lines(self.GAMEDISPLAY, self.BORDER_COLOR, True, borderList, BORDER_WIDTH)


    def newBlock(self, nextBlocks):

        rand = self.blockSet.pop(0)
        if self.blockListTooShort(len(self.blockSet)):
            self.appendBlockList()

        self.setNextBlocks(nextBlocks)

        if rand == 0:
            self.block = BlockT(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 1:
            self.block = BlockS(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 2:
            self.block = BlockJ(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 3:
            self.block = BlockI(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 4:
            self.block = BlockL(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 5:
            self.block = BlockZ(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)
        elif rand == 6:
            self.block = BlockO(self.INIT_X, self.INIT_Y, self.BLOCK_SIZE)


    def paused(self):
        pause = True
        pygame.mixer.music.pause()
        self.startTime = pygame.mixer.music.get_pos()

        while pause:

            while Gtk.events_pending():
                Gtk.main_iteration()

            self.checkForQuit()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = self.soundOn.get_rect()
                    pos.x = self.soundPosition[0]
                    pos.y = self.soundPosition[1]
                    if pos.collidepoint(pygame.get_pos()):
                        self.flipSoundIcon()
                    pos.x = self.musicPosition[0]
                    pos.y = self.musicPosition[1]
                    if pos.collidepoint(pygame.mouse.get_pos()):
                        self.flipMusicIcon()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.isMusicOn == True:
                            pygame.mixer.music.unpause()
                        pause = False
                    elif event.key == pygame.K_m:
                        self.flipMusicIcon()
                    elif event.key == pygame.K_s:
                        self.flipSoundIcon()

            self.GAMEDISPLAY.fill(self.WHITE, [self.LEFT_BOUNDARY, self.TOP_BOUNDARY, 10 * self.BLOCK_SIZE, 20 * self.BLOCK_SIZE])
            myfont = pygame.font.SysFont('Comic Sans MS', self.BLOCK_SIZE * 3 / 4)
            pausedText = myfont.render("Paused", True, self.BLACK)
            textWidth = pausedText.get_rect().width
            textHeight = pausedText.get_rect().height

            self.GAMEDISPLAY.blit(pausedText, (self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - textWidth / 2,
                                          self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 - textHeight / 2))
            myfont = pygame.font.SysFont('Comic Sans MS', self.BLOCK_SIZE / 2)
            additionalText = myfont.render("Press \"p\" to resume!", True, self.BLACK)
            additionalTextWidth = additionalText.get_rect().width
            additionalTextHeight = additionalText.get_rect().height
            myfont = pygame.font.SysFont('Comic Sans MS', self.BLOCK_SIZE / 2)
            additionalText2 = myfont.render("Press \"Esc\" to quit!", True, self.BLACK)

            self.GAMEDISPLAY.blit(additionalText,
                             (self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
                              self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 + textHeight))
            self.GAMEDISPLAY.blit(additionalText2, (
                self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
                self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 + 2 * textHeight))
            pygame.display.update()
            self.clock.tick(15)


    def gameOver(self):
        pause = True
        self.score += self.bankedpoints
        self.bankedpoints = 0

    #=================================REDRAWS THE NEW SCORE & LAST BLOCK PLACED===============================================

        # drawing self.landed blocks
        for i in range(0, len(self.landed)):
            for j in range(0, len(self.landed[i])):
                if (self.landed[i][j] != None):
                    self.landed[i][j].display(self.GAMEDISPLAY)
            self.block.display(self.GAMEDISPLAY)

        # drawing top cover
        # self.GAMEDISPLAY.fill(self.BLACK, [0, 0, self.WIDTH, self.TOP_BOUNDARY])
        spacing = self.HEIGHT / 100
        for i in range(0, 14):
            self.GAMEDISPLAY.fill((100, 105 + i, 155 + i), [0, spacing * i, self.WIDTH, spacing])

        self.drawGameAreaBorder()
        self.drawQuesAnsBorder()

        # draw self.score, self.level, multiplier
        self.drawVarsBorder()

        # self.GAMEDISPLAY.fill(self.BLACK, [self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 1.5 * self.BLOCK_SIZE, 7.5 * self.BLOCK_SIZE, self.BLOCK_SIZE])
        # screen_text = self.BASICFONT.render("Score: ", True, self.WHITE)
        # score_text = self.SCOREFONT.render("            " + str(self.score), True, self.WHITE)
        # self.GAMEDISPLAY.blit(score_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 1.5 * self.BLOCK_SIZE))
        # self.GAMEDISPLAY.blit(screen_text, (self.RIGHT_BOUNDARY + self.BLOCK_SIZE + 10, self.TOP_BOUNDARY + 1.5 * self.BLOCK_SIZE))


    #==================================================================================

        pygame.mixer.music.stop()
        self.playSound('end.wav')

        initialSize = self.BLOCK_SIZE

        self.updateHiscore(self.checkForNewHiscore())

        while pause:

            while Gtk.events_pending():
                Gtk.main_iteration()

            self.checkForQuit()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = self.soundOn.get_rect()
                    pos.x = self.soundPosition[0]
                    pos.y = self.soundPosition[1]
                    if pos.collidepoint(pygame.mouse.get_pos()):
                        self.flipSoundIcon()
                    pos.x = self.musicPosition[0]
                    pos.y = self.musicPosition[1]
                    if pos.collidepoint(pygame.mouse.get_pos()):
                        self.flipMusicIcon()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:

                        self.dx = 0
                        self.dy = 0

                        self.gameExit = True
                        pause = False

                    elif event.key == pygame.K_m:
                        self.flipMusicIcon()
                    elif event.key == pygame.K_s:
                        self.flipSoundIcon()

            myfont = pygame.font.SysFont('Comic Sans MS', initialSize)
            gameOverText = myfont.render("Game Over", True, self.BLACK)
            textWidth = gameOverText.get_rect().width
            textHeight = gameOverText.get_rect().height
            myfont = pygame.font.SysFont('Comic Sans MS', initialSize - self.BLOCK_SIZE / 2)
            additionalText = myfont.render("Press \"r\" to restart!", True, self.BLACK)
            additionalTextWidth = additionalText.get_rect().width
            additionalTextHeight = additionalText.get_rect().height
            additionalText2 = myfont.render("Press \"Esc\" to quit!", True, self.BLACK)
            myfont = pygame.font.SysFont('Comic Sans MS', initialSize)
            gameOverText2 = myfont.render("Game Over", True, self.RED)
            textWidth2 = gameOverText2.get_rect().width
            textHeight2 = gameOverText2.get_rect().height
            self.GAMEDISPLAY.fill(self.WHITE, [self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - textWidth,
                                     self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 - textHeight, 2 * textWidth,
                                     2 * (textHeight + 2 * additionalTextHeight)])
            self.GAMEDISPLAY.blit(gameOverText, (self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - textWidth / 2,
                                            self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 - textHeight / 2))
            self.GAMEDISPLAY.blit(additionalText, (
                self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
                self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 + textHeight))
            self.GAMEDISPLAY.blit(additionalText2, (
                self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - additionalTextWidth / 2,
                self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 + 2 * textHeight))
            self.GAMEDISPLAY.blit(gameOverText2, (self.LEFT_BOUNDARY + (self.RIGHT_BOUNDARY - self.LEFT_BOUNDARY) / 2 - textWidth / 2 + 2,
                                             self.TOP_BOUNDARY + (self.BOTTOM_BOUNDARY - self.TOP_BOUNDARY) / 2 - textHeight / 2))
            pygame.display.update()
            if initialSize < self.BLOCK_SIZE:
                initialSize += 1
            self.clock.tick(15)


    def drawGridLines(self):
    ##    DOTTTED LINES
    ##    SPACING = self.BLOCK_SIZE / 4
    ##    for i in range (1, 10):
    ##        for j in range (0, 85):
    ##            if j % 2 == 0:
    ##                pygame.draw.line(self.GAMEDISPLAY, (200, 200, 200),
    ##                                (self.LEFT_BOUNDARY + i * self.BLOCK_SIZE, self.TOP_BOUNDARY + j * SPACING),
    ##                                (self.LEFT_BOUNDARY + i * self.BLOCK_SIZE, self.TOP_BOUNDARY + j * SPACING + SPACING),
    ##                                1)
    ##    for i in range (1, 20):
    ##        for j in range (0, 43):
    ##            if j % 2 == 0:
    ##                pygame.draw.line(self.GAMEDISPLAY, (200, 200, 200),
    ##                                (self.LEFT_BOUNDARY + j * SPACING, self.TOP_BOUNDARY + i * self.BLOCK_SIZE),
    ##                                (self.LEFT_BOUNDARY + j * SPACING + SPACING, self.TOP_BOUNDARY + i * self.BLOCK_SIZE),
    ##                                1)
        for i in range (1, 10):
            pygame.draw.line(self.GAMEDISPLAY, self.GRID_COLOR,
                            (self.LEFT_BOUNDARY + i * self.BLOCK_SIZE, self.TOP_BOUNDARY),
                            (self.LEFT_BOUNDARY + i * self.BLOCK_SIZE, self.BOTTOM_BOUNDARY),
                            1)
        for i in range (1, 20):
            pygame.draw.line(self.GAMEDISPLAY, self.GRID_COLOR,
                            (self.LEFT_BOUNDARY, self.TOP_BOUNDARY + i * self.BLOCK_SIZE),
                            (self.LEFT_BOUNDARY + 10 * self.BLOCK_SIZE, self.TOP_BOUNDARY + i * self.BLOCK_SIZE),
                            1)

    def move(self):
        if self.block is None or self.currentBlock is False:
            return
        #self.lock.acquire()
        # self.accl = self.accl * 3 / 5
        pygame.time.set_timer(self.MOVE, 100)
        self.block.setX(self.block.getX() + self.dx)
        if self.checkCollision():
            self.block.setX(self.block.getX() - self.dx)
        self.block.setY(self.block.getY() + self.dy)
        if self.checkCollision():
            self.block.setY(self.block.getY() - self.dy)
        #self.lock.release()

    def generateQues(self):
        if self.level <= 4:
            multi_var = randint(0, 10)
        else:
            multi_var = randint(0, 40)
        two_op = randint(0, 1)
        bound_list = self.calculateUpbound()
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
            char = pygame.K_1
        if sol_key == 1:
            char = pygame.K_2
        if sol_key == 2:
            char = pygame.K_3
        if sol_key == 3:
            char = pygame.K_4
        if self.level < 4:
            diff1 = randint(1,4)
        else:
            diff1 = randint(1,5)
        diff2 = randint(1, 10)
        diff3 = randint(6, 20)
        return [q1, q2, operator, sol_key, diff1, diff2, diff3, multi_var, two_op, char]


    def calculateUpbound(self):
        if self.level == 1:
            o_upbound = 0
            o_lbound = 0
            q1_upbound = 9
            q2_upbound = 9

        elif self.level == 2:
            o_upbound = 1
            o_lbound = 0
            q1_upbound = 9
            q2_upbound = 9
        elif self.level == 3:
            o_upbound = 2
            o_lbound = 2
            q1_upbound = 9
            q2_upbound = 9
        elif self.level == 4:
            o_upbound = 3
            o_lbound = 2
            q1_upbound = 9
            q2_upbound = 9
        elif self.level == 5:
            o_upbound = 1
            o_lbound = 0
            q1_upbound = 9
            q2_upbound = 20
        elif self.level == 6:
            o_upbound = 1
            o_lbound = 0
            q1_upbound = 20
            q2_upbound = 20
        elif self.level == 7:
            o_upbound = 2
            o_lbound = 0
            q1_upbound = 20
            q2_upbound = 20
        elif self.level == 8:
            o_upbound = 3
            o_lbound = 0
            q1_upbound = 20
            q2_upbound = 20
        elif self.level == 9:
            o_upbound = 3
            o_lbound = 0
            q1_upbound = 40
            q2_upbound = 40
        elif self.level == 10:
            o_upbound = 4
            o_lbound = 4
            q1_upbound = 10
            q2_upbound = 5
        elif self.level >= 11:
            o_upbound = 3
            o_lbound = 0
            q1_upbound = 60
            q2_upbound = 60
        return [o_upbound, q1_upbound, q2_upbound, o_lbound]


    def calculateLevelAndFallFreq(self):
        # Based on the self.score, return the self.level the player is on and
        # how many seconds pass until a falling piece falls one space.

        self.level_prev = self.level
        divisor = self.level_prev + 80
        self.level = int(self.score/divisor) + 1
        self.fallFreq = 1010 - (self.total_lines + self.level) * 10 # 500 * (level - 1)
        if self.fallFreq < 50:
            self.fallFreq = 50


    def terminate(self):
        pygame.quit()
        sys.exit()


    def drawCompliment(self, rand):
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
        elif rand == 8:
            compliment = "Good job! Next questions worth points upon block landing."
        complimentSurf = self.BASICFONT.render(compliment, True, self.TEXTCOLOR)
        complimentRect = complimentSurf.get_rect()
        complimentRect.center = (self.WIDTH / 2, self.TOP_BOUNDARY - 2.5 * self.BLOCK_SIZE)
        self.GAMEDISPLAY.blit(complimentSurf, complimentRect)
        if rand == 4 or rand == 5 or rand == 6 or rand == 7:
            controlSurf = self.BASICFONT.render("Lost controls.", True, self.TEXTCOLOR)
            controlRect = controlSurf.get_rect()
            controlRect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 2.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(controlSurf, controlRect)

    def drawCombo(self):
        if self.single:
            combo_outline_surf = self.BASICFONT.render("Single", True, self.BLACK)
            combo_surf = self.BASICFONT.render("Single", True, self.WHITE)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)
        elif self.double:
            combo_outline_surf = self.BASICFONT.render("Double", True, self.BLACK)
            combo_surf = self.BASICFONT.render("Double", True, self.WHITE)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)
        elif self.triple:
            combo_outline_surf = self.BASICFONT.render("Triple", True, self.BLACK)
            combo_surf = self.BASICFONT.render("Triple", True, self.WHITE)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)
        elif self.tetris:
            combo_outline_surf = self.BASICFONT.render("Tetris", True, self.BLACK)
            combo_surf = self.BASICFONT.render("Tetris", True, self.COMBOCOLOR)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)
        elif self.d_tspin:
            combo_outline_surf = self.BASICFONT.render("T-spin Double", True, self.BLACK)
            combo_surf = self.BASICFONT.render("T-spin Double", True, self.COMBOCOLOR)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)
        elif self.t_tspin:
            combo_outline_surf = self.BASICFONT.render("T-spin Triple", True, self.BLACK)
            combo_surf = self.BASICFONT.render("T-spin Triple", True, self.COMBOCOLOR)
            combo_outline_rect = combo_outline_surf.get_rect()
            combo_outline_rect.center = (self.WIDTH / 2 + 1, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE + 1)
            combo_rect = combo_surf.get_rect()
            combo_rect.center = (self.WIDTH / 2, self.BOTTOM_BOUNDARY + 1.5 * self.BLOCK_SIZE)
            self.GAMEDISPLAY.blit(combo_outline_surf, combo_outline_rect)
            self.GAMEDISPLAY.blit(combo_surf, combo_rect)


    def playSound(self, soundSource):
        if self.isSoundOn:
            sound = pygame.mixer.Sound(soundSource)
            sound.play()


    def flipSoundIcon(self):
        if self.isSoundOn:
            self.isSoundOn = False
        else:
            self.isSoundOn = True
        self.drawSoundIcon()
        pygame.display.update()


    def flipMusicIcon(self):
        if self.isMusicOn:
            pygame.mixer.music.pause()
            self.isMusicOn = False
        else:
            pygame.mixer.music.unpause()
            self.isMusicOn = True
        self.drawMusicIcon()
        pygame.display.update()


    def drawSoundIcon(self):
        if self.isSoundOn:
            self.GAMEDISPLAY.blit(self.soundOn, self.soundPosition)
        else:
            self.GAMEDISPLAY.blit(self.soundOff, self.soundPosition)


    def drawMusicIcon(self):
        if self.isMusicOn:
            self.GAMEDISPLAY.blit(self.musicOn, self.musicPosition)
        else:
            self.GAMEDISPLAY.blit(self.musicOff, self.musicPosition)


    def checkForQuit(self):
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            while Gtk.events_pending():
                Gtk.main_iteration()
            self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            while Gtk.events_pending():
                Gtk.main_iteration()
            if event.key == K_ESCAPE:
                self.terminate()  # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event)  # put the other KEYUP event objects back


    # checks if there is a new hiscore. If there is, returns the index of the new hiscore
    #  is to be placed, otherwise returns -1.
    def checkForNewHiscore(self):
        try:
            with open("leaderboard.json") as data_file:
                data = json.load(data_file)
        except IOError:
            self.newLeaderboard()
            with open("leaderboard.json") as data_file:
                data = json.load(data_file)
        # global self.score
        try:
            if self.score * (self.total_lines / 10.0) <= int(data[len(data) - 1]["score"]):
                return -1

            for i in range (len(data)-1, 0, -1):
                while Gtk.events_pending():
                    Gtk.main_iteration()
                if self.score * (self.total_lines / 10.0) > data[i]["score"] and self.score * (self.total_lines / 10.0) <= data[i-1]["score"]:
                    return i
            if self.score * (self.total_lines / 10.0) > int(data[0]["score"]):
                return 0
        except ValueError:
            self.newLeaderboard()
            return -1


    def updateHiscore(self, index):
        if index == -1:
            return
        with open("leaderboard.json") as data_file:
            data = json.load(data_file)
        self.drawHighScore("You made a new High Score!", self.level, self.score, self.total_lines)
        name = inputbox.ask(self.GAMEDISPLAY, "Name")
        for i in range(len(data) - 1, index, -1):
            data[i]["date"] = data[i - 1]["date"]
            data[i]["score"] = data[i - 1]["score"]
            data[i]["name"] = data[i - 1]["name"]
        data[index]["date"] = str(datetime.datetime.now().date())+" "*20
        data[index]["score"] = int(self.score * (self.total_lines / 10.0))
        data[index]["name"] = name
        with open("leaderboard.json", 'w') as data_file:
            json.dump(data, data_file)

    def drawHighScore(self, text, lvl, pts, tL):
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        i = 0
        new_score = pts
        if abs(new_score - int(pts * (tL/10.0))) > 1000:
            self.speed = 900
        elif abs(new_score - int(pts * (tL/10.0))) > 100:
            self.speed = 60
        elif abs(new_score - int(pts * (tL/10.0))) > 10:
            self.speed = 30
        self.GAMEDISPLAY.fill(self.BLACK)
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTSHADOWCOLOR)
        titleRect.center = (int(self.WIDTH / 2)-3, int(self.HEIGHT / 4) - 40)
        self.GAMEDISPLAY.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTCOLOR)
        titleRect.center = (int(self.WIDTH / 2) - 3, int(self.HEIGHT / 4) - 46)
        self.GAMEDISPLAY.blit(titleSurf, titleRect)
        while i < 6:
            if i == 1:
                # Level text.
                pressKeySurf, pressKeyRect = self.makeTextObjs('Level: ' + str(lvl), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 3)
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            if i == 2:
                # Score text.
                pressKeySurf, pressKeyRect = self.makeTextObjs('Score: ' + str(pts), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 4)
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            if i == 3:
                # Lines text.
                pressKeySurf, pressKeyRect = self.makeTextObjs('Lines Cleared: ' + str(tL), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 5)
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            if i == 4:
                # Total text.
                pressKeySurf, pressKeyRect = self.makeTextObjs('Total = ' + str(pts) + " x " + str(tL/10.0), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 6)
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            if i == 5:
                pressKeySurf, pressKeyRect = self.makeTextObjs("press any key to skip", self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 9)
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            while i == 5 and new_score != int(pts * (tL/10.0)):
                while Gtk.events_pending():
                    Gtk.main_iteration()
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_RETURN:
                    new_score = int(pts * (tL/10.0))
                pressKeySurf, pressKeyRect = self.makeTextObjs(str(int(new_score)), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 7)
                pygame.draw.rect(self.GAMEDISPLAY, self.BLACK, [0, int(self.HEIGHT / 2) + self.BLOCK_SIZE * 6.75, self.WIDTH, 2 * self.BLOCK_SIZE])
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
                if new_score > int(pts * (tL/10.0)):
                    new_score -= 1
                else:
                    new_score += 1
                pygame.display.update()
                self.clock.tick(self.speed)
            if i == 5 and new_score == int(pts * (tL/10.0)):
                pressKeySurf, pressKeyRect = self.makeTextObjs(str(int(new_score)), self.BASICFONT, self.TEXTCOLOR)
                pressKeyRect.center = (int(self.WIDTH / 2), int(self.HEIGHT / 2) + self.BLOCK_SIZE * 7)
                pygame.draw.rect(self.GAMEDISPLAY, self.BLACK, [0, int(self.HEIGHT / 2) + self.BLOCK_SIZE * 6.75, self.WIDTH, 2 * self.BLOCK_SIZE])
                self.GAMEDISPLAY.blit(pressKeySurf, pressKeyRect)
            i += 1
            pygame.display.update()
            self.clock.tick(1)

    def checkForKeyPress(self):
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.

        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def drawGameOver(self, text):
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        self.GAMEDISPLAY.fill(self.BLACK)
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTSHADOWCOLOR)
        titleRect.center = (int(self.WIDTH / 2)-3, int(self.HEIGHT / 4) - 40)
        self.GAMEDISPLAY.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = self.makeTextObjs(text, self.BIGFONT, self.TEXTCOLOR)
        titleRect.center = (int(self.WIDTH / 2) - 3, int(self.HEIGHT / 4) - 46)
        self.GAMEDISPLAY.blit(titleSurf, titleRect)

        while self.checkForKeyPress() is None:
            pygame.display.update()
            self.clock.tick()

    def newLeaderboard(self):
        leaderboardFile = open("leaderboard.json", "w")
        leaderboardFile.write("[{\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____SamC______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Gaurav____\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Boyi______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____SamO______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Brandon___\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Tony______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Eric______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____Btai______\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____gauravnv__\"}, \
                                {\"date\": \"2018-05-03          \", \"score\": 0, \"name\": \"_____XDSU______\"}]")
        leaderboardFile.close()


    # =================================================================
    # MENU FUNCTIONS

    def leaderboard_function(self):
        # Draw random color and text
        bg_color = COLOR_BACKGROUND

        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # self.main_menu as the menu that will check all your input.
        self.main_menu.disable()
        self.main_menu.reset(1)

        while True:

            # Clock tick
            self.clock.tick(60)

            # Application events
            playevents = pygame.event.get()
            for e in playevents:
                while Gtk.events_pending():
                    Gtk.main_iteration()

                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        if self.main_menu.is_disabled():
                            self.main_menu.enable()

                            # Quit this function, then skip to loop of main-menu on line 197
                            return

            # Pass events to self.main_menu
            self.main_menu.mainloop(playevents)

            # Continue playing
            self.GAMEDISPLAY.fill(bg_color)
            # self.GAMEDISPLAY.blit(f, (int(WINDOW_SIZE[0] - f_rect.width()) / 2,
            #                      int(WINDOW_SIZE[1] / 2)))

            # ADD FUNCTION HERE
            pygame.display.flip()


    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()


    def play_function(self):
        """
        Main game function

        :param font: Pygame font
        :return: None
        """

        # Draw random color and text
        bg_color = COLOR_BACKGROUND

        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # self.main_menu as the menu that will check all your input.
        self.main_menu.disable()
        self.main_menu.reset(1)

        test = True

        while test:

            # Clock tick
            self.clock.tick(60)

            # Application events
            playevents = pygame.event.get()
            for e in playevents:
                while Gtk.events_pending():
                    Gtk.main_iteration()

                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        if self.main_menu.is_disabled():
                            self.main_menu.enable()

                            return

            # Pass events to self.main_menu
            self.main_menu.mainloop(playevents)

            # Continue playing
            self.GAMEDISPLAY.fill(bg_color)
            # self.GAMEDISPLAY.blit(f, (int(WINDOW_SIZE[0] - f_rect.width()) / 2,
            #                      int(WINDOW_SIZE[1] / 2)))
            self.main_menu.done()
            self.runGame()
            pygame.display.flip()
            test = False


    def main_background(self):
        """
        Function used by menus, draw on background while menu is active.

        :return: None
        """
        self.GAMEDISPLAY.fill(self.RED)

    # global self.main_menu
    def buildMain(self):
        # global self.main_menu
        
        # -----------------------------------------------------------------------------
        # PLAY MENU

        play_menu = pygameMenu.Menu(self.GAMEDISPLAY,
                                    bgfun=None,
                                    color_selected=COLOR_RED,
                                    font=fontdir,
                                    font_color=COLOR_WHITE,
                                    font_title=font_tit,
                                    font_size=self.BLOCK_SIZE,
                                    menu_alpha=100,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=COLOR_RED,
                                    menu_height=int(self.HEIGHT),  #WINDOW_SIZE[1] * 1),
                                    menu_width=int(self.WIDTH),  #WINDOW_SIZE[0] * 1),
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    option_shadow=False,
                                    title='Play menu',
                                    window_height=self.HEIGHT,  #WINDOW_SIZE[1],
                                    window_width=self.WIDTH  #WINDOW_SIZE[0]
                                    )

        play_menu.add_option('Start', self.play_function)

        play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

        # instruction MENU
        instruction_menu = pygameMenu.TextMenu(self.GAMEDISPLAY,
                                               bgfun=None,
                                               color_selected=COLOR_GREEN,
                                               font=fontdir,
                                               font_color=COLOR_WHITE,
                                               font_size_title=self.BLOCK_SIZE,
                                               font_title=font_tit,
                                               menu_color_title=COLOR_GREEN,
                                               menu_height=int(self.HEIGHT),  #WINDOW_SIZE[1] * 1),
                                               menu_width=int(self.WIDTH),  #WINDOW_SIZE[0] * 1),
                                               onclose=PYGAME_MENU_DISABLE_CLOSE,
                                               option_shadow=True,
                                               text_color=COLOR_WHITE,
                                               text_fontsize=self.BLOCK_SIZE * 2 / 3,
                                               title='Instruction',
                                               window_height=self.HEIGHT,  #WINDOW_SIZE[1],
                                               window_width=self.WIDTH,  #WINDOW_SIZE[0],
                                               # menu_color=MENU_BACKGROUND_COLOR,
                                               font_size=self.BLOCK_SIZE,
                                               menu_alpha=100,
                                               menu_color=COLOR_BLACK
                                               )
        for m in self.INSTRUCTION:
            instruction_menu.add_line(m)
        instruction_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
        instruction_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
        instruction_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
        instruction_menu.add_option('Press \'Enter\' to return', PYGAME_MENU_BACK)

        # Leaderboard MENU
        leaderboard_menu = pygameMenu.TextMenu(self.GAMEDISPLAY,
                                               bgfun=None,
                                               color_selected=COLOR_BLUE,
                                               font=fontdir,
                                               font_color=COLOR_WHITE,
                                               font_size_title=self.BLOCK_SIZE,
                                               font_title=font_tit,
                                               # menu_color=MENU_BACKGROUND_COLOR,
                                               menu_color_title=COLOR_BLUE,
                                               menu_height=int(self.HEIGHT),  #WINDOW_SIZE[1] * 1),
                                               menu_width=int(self.WIDTH),  #WINDOW_SIZE[0] * 1),
                                               onclose=PYGAME_MENU_DISABLE_CLOSE,
                                               option_shadow=True,
                                               text_color=COLOR_WHITE,
                                               text_fontsize=self.BLOCK_SIZE * 2 / 3,
                                               title='Leaderboard',
                                               window_height=self.HEIGHT,  #WINDOW_SIZE[1],
                                               window_width=self.WIDTH,  #WINDOW_SIZE[0],
                                               font_size=self.BLOCK_SIZE,
                                               menu_alpha=100,
                                               menu_color=COLOR_BLACK
                                               )
        try:
            with open("leaderboard.json") as data_file:
                data = json.load(data_file)
        except IOError:
            self.newLeaderboard()
            with open("leaderboard.json") as data_file:
                data = json.load(data_file)
        except ValueError:
            self.newLeaderboard()
            with open("leaderboard.json") as data_file:
                data = json.load(data_file)
        LEADERBOARD = []
        try:
            for i in range(0, len(data)):
                LEADERBOARD.insert(len(LEADERBOARD), str(i+1) + "]   " + str(data[i]["date"]) + "          " + str(data[i]["name"]) + "          " + str(data[i]["score"]))
        except ValueError:
            self.newLeaderboard()

        for m in LEADERBOARD:
            leaderboard_menu.add_line(m)

        # leaderboard_menu.add_option('View top 10 self.scores!', leaderboard_function)
        leaderboard_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
        leaderboard_menu.add_option('Press \'Enter\' to return', PYGAME_MENU_BACK)

        # MAIN MENU
        self.main_menu = pygameMenu.Menu(self.GAMEDISPLAY,
                                    bgfun=None,
                                    color_selected=self.RED,
                                    font=fontdir,
                                    font_color=COLOR_WHITE,
                                    font_size=self.BLOCK_SIZE,
                                    menu_alpha=100,
                                    menu_color=COLOR_BLACK,
                                    menu_height=int(self.HEIGHT),  #WINDOW_SIZE[1] * 1),
                                    menu_width=int(self.WIDTH),  #WINDOW_SIZE[0] * 1),
                                    menu_color_title=COLOR_RED,
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
                                    font_title=font_tit,
                                    option_shadow=True,
                                    title='Metris',
                                    window_height=self.HEIGHT,  #WINDOW_SIZE[1],
                                    window_width=self.WIDTH  #WINDOW_SIZE[0]
                                    )
        self.main_menu.add_option('Play', play_menu)
        self.main_menu.add_option('Instruction', instruction_menu)
        self.main_menu.add_option('Leaderboard', leaderboard_menu)
        self.main_menu.add_option('Quit', PYGAME_MENU_EXIT)


    def runMain(self):
        # global self.main_menu
        self.main_menu.mainloop(pygame.event.get())

    def runNewGame(self):
        self.makeGameObject()
        self.running = True
        while self.running:
            self.buildMain()
            self.runMain()
            self.runGame()

# if __name__ == '__main__':
#     while True:
#         game = Metris()
#         game.buildMain()
#         game.runMain()
