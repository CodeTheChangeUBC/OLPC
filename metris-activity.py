from gettext import gettext as _

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton


# sys.path.append('..')  # Import sugargame package from top directory.
import sugargame
import sugargame.canvas

import Metris

class MetrisActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)
        self.paused = False

        self.game = Metris.Metris() # call menu instead
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self,
                                                           main=self.game.runNewGame,
                                                           modules=[pygame.display])

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        # self.game.buildMain()
        # self.game.main()

        # toolbarbox = ToolbarBox()
        # activity_button = ActivityToolbarButton(self)
        # toolbarbox.toolbar.insert(activity_button, 0)
        # self.set_toolbar_box(toolbarbox)

        #activity_button.show()
        #toolbar_box.show()
        #
        # stop_button = StopButton(self)
        # toolbarbox.toolbar.insert(stop_button, -1)

        # save_bundle_button = ToolButton('save-as-bundle')
        # save_bundle_button.set_tooltip(_('Create bundle (.xo file)'))
        # activity_button.get_page().insert(save_bundle_btn, -1)
        # save_bundle_button.connect('clicked', self.save_bundle)
        # save_bundle_button.show()

        # self.show_all()


    def _pause_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        self.game.set_paused(self.paused)

        # Update the button to show the next action.
        if self.paused:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon_name('media-playback-pause')
            button.set_tooltip(_("Pause"))

    def _stop_cb(self, button):
        self.game.running = False

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def get_preview(self):
        return self._pygamecanvas.get_preview()