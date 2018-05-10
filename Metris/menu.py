import pygameMenu
from random import *
from pygameMenu.locals import *
from pygameMenu import fonts
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

fontdir = pygameMenu.fonts.FONT_BEBAS
font_tit = pygameMenu.fonts.FONT_BEBAS

# ABOUT = ['Metris {0}'.format(Metris.__version__),
#          'Author: {0}'.format(Metris.__author__),
#          PYGAMEMENU_TEXT_NEWLINE,
#          'Email: {0}'.format(Metris.__email__)]

COLOR_BACKGROUND = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (0, 0, 0)
WINDOW_SIZE = (800, 680)


def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass


def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None, 28)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")


def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name") + " was entered"

if __name__ == '__main__': main()