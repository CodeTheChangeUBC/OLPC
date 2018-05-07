import pygame
import pygameMenu

from random import *
from pygameMenu.locals import *
from pygameMenu import fonts

fontdir = pygameMenu.fonts.FONT_8BIT

# ABOUT = ['Metris {0}'.format(Metris.__version__),
#          'Author: {0}'.format(Metris.__author__),
#          PYGAMEMENU_TEXT_NEWLINE,
#          'Email: {0}'.format(Metris.__email__)]

COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (640, 480)

# # -----------------------------------------------------------------------------
# # Functions
#
# def random_color():
#     """
#     Return random color.
#
#     :return: Color tuple
#     """
#     return randrange(0, 255), randrange(0, 255), randrange(0, 255)
#
#
# def play_function(font):
#     """
#     Main game function
#
#     :param difficulty: Difficulty of the game
#     :param font: Pygame font
#     :return: None
#     """
#
#
#
#     # Draw random color and text
#     bg_color = random_color()
#     f_width = f.get_size()[0]
#
#     # Reset main menu and disable
#     # You also can set another menu, like a 'pause menu', or just use the same
#     # main_menu as the menu that will check all your input.
#     main_menu.disable()
#     main_menu.reset(1)
#
#     while True:
#
#         # Clock tick
#         clock.tick(60)
#
#         # Application events
#         playevents = pygame.event.get()
#         for e in playevents:
#             if e.type == QUIT:
#                 exit()
#             elif e.type == KEYDOWN:
#                 if e.key == K_ESCAPE:
#                     if main_menu.is_disabled():
#                         main_menu.enable()
#
#                         # Quit this function, then skip to loop of main-menu on line 197
#                         return
#
#         # Pass events to main_menu
#         main_menu.mainloop(playevents)
#
#         # Continue playing
#         surface.fill(bg_color)
#         surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
#         pygame.display.flip()
#
#
#
# # -----------------------------------------------------------------------------
# # PLAY MENU
# play_menu = pygameMenu.Menu(surface,
#                             bgfun=main_background,
#                             color_selected=COLOR_WHITE,
#                             font=pygameMenu.fonts.FONT_BEBAS,
#                             font_color=COLOR_BLACK,
#                             font_size=30,
#                             menu_alpha=100,
#                             menu_color=MENU_BACKGROUND_COLOR,
#                             menu_height=int(WINDOW_SIZE[1] * 0.6),
#                             menu_width=int(WINDOW_SIZE[0] * 0.6),
#                             onclose=PYGAME_MENU_DISABLE_CLOSE,
#                             option_shadow=False,
#                             title='Play menu',
#                             window_height=WINDOW_SIZE[1],
#                             window_width=WINDOW_SIZE[0]
#                             )
# # When pressing return -> play(DIFFICULTY[0], font)
# play_menu.add_option('Start', play_function, DIFFICULTY,
#                      pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30))
# play_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
#                                              ('Medium', 'MEDIUM'),
#                                              ('Hard', 'HARD')],
#                        onreturn=None,
#                        onchange=change_difficulty)
# play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)
#
# # ABOUT MENU
# about_menu = pygameMenu.TextMenu(surface,
#                                  bgfun=main_background,
#                                  color_selected=COLOR_WHITE,
#                                  font=pygameMenu.fonts.FONT_BEBAS,
#                                  font_color=COLOR_BLACK,
#                                  font_size_title=30,
#                                  font_title=pygameMenu.fonts.FONT_8BIT,
#                                  menu_color=MENU_BACKGROUND_COLOR,
#                                  menu_color_title=COLOR_WHITE,
#                                  menu_height=int(WINDOW_SIZE[1] * 0.6),
#                                  menu_width=int(WINDOW_SIZE[0] * 0.6),
#                                  onclose=PYGAME_MENU_DISABLE_CLOSE,
#                                  option_shadow=False,
#                                  text_color=COLOR_BLACK,
#                                  text_fontsize=20,
#                                  title='About',
#                                  window_height=WINDOW_SIZE[1],
#                                  window_width=WINDOW_SIZE[0]
#                                  )
# for m in ABOUT:
#     about_menu.add_line(m)
# about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
# about_menu.add_option('Return to menu', PYGAME_MENU_BACK)
#
# # MAIN MENU
# main_menu = pygameMenu.Menu(surface,
#                             bgfun=main_background,
#                             color_selected=COLOR_WHITE,
#                             font=pygameMenu.fonts.FONT_BEBAS,
#                             font_color=COLOR_BLACK,
#                             font_size=30,
#                             menu_alpha=100,
#                             menu_color=MENU_BACKGROUND_COLOR,
#                             menu_height=int(WINDOW_SIZE[1] * 0.6),
#                             menu_width=int(WINDOW_SIZE[0] * 0.6),
#                             onclose=PYGAME_MENU_DISABLE_CLOSE,
#                             option_shadow=False,
#                             title='Main menu',
#                             window_height=WINDOW_SIZE[1],
#                             window_width=WINDOW_SIZE[0]
#                             )
# main_menu.add_option('Play', play_menu)
# main_menu.add_option('About', about_menu)
# main_menu.add_option('Quit', PYGAME_MENU_EXIT)
