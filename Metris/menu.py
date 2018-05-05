import pygame
import pygameMenu

from random import *
from pygameMenu.locals import *
from pygameMenu import fonts

fontdir = pygameMenu.fonts.FONT_8BIT

ABOUT = ['Metris {0}'.format(Metris.__version__),
         'Author: {0}'.format(Metris.__author__),
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(Metris.__email__)]

COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (640, 480)