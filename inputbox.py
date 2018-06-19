# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import re


def get_key():
    while 1:
        while Gtk.events_pending():
            Gtk.main_iteration()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 102,
                      (screen.get_height() / 2) - 12,
                      204, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    global current_string
    current_string = []
    display_box(screen, question + ": " + string.join(current_string, ""))
    counter = 15
    while True:
        while Gtk.events_pending():
            Gtk.main_iteration()
        inkey = get_key()
        if inkey == K_BACKSPACE and counter <= 15:
            if not counter == 15:
                current_string = current_string[0:-1]
                counter += 1
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            if counter > 0:
                current_string.append("-")
                counter -= 1
        elif inkey <= 127:
            if counter > 0:
                current_string.append(chr(inkey))
                counter -= 1
        display_box(screen, question + ": " + string.join(current_string, ""))

    return '{:_^15}'.format(string.join(current_string, ""))[:15]


def main():
    screen = pygame.display.set_mode((800, 800))
    print ask(screen, "Name") + " was entered"


if __name__ == '__main__': main()
