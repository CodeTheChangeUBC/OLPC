import gi

import sugargame
import sugargame.canvas
import pygame
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton
from gettext import gettext as _
import Metris

class MetrisActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.game = Metris.buildMenu() # call menu instead
        self.game.main()

        toolbarbox = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbarbox.toolbar.insert(activity_button, 0)
        self.set_toolbar_box(toolbarbox)

        #activity_button.show()
        #toolbar_box.show()

        stop_button = StopButton(self)
        toolbarbox.toolbar.insert(stop_button, -1)

        # save_bundle_button = ToolButton('save-as-bundle')
        # save_bundle_button.set_tooltip(_('Create bundle (.xo file)'))
        # activity_button.get_page().insert(save_bundle_btn, -1)
        # save_bundle_button.connect('clicked', self.save_bundle)
        # save_bundle_button.show()

        toolbarbox.show_all()