import sys
import pygame
import gui_objects
from time import strftime, localtime
# from time import time, gmtime, strftime, mktime, localtime
from pprint import pprint
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS, TITLE_RECT, ROWS
from displayscreen import PiInfoScreen
from database import RACK_DB
sys.dont_write_bytecode = True


# For more information on the variables and functions in this file view
# displayscreen.py in the root folder of this project


class myScreen(PiInfoScreen):
    # PiInfoScreen.__init__()
    refreshtime = 1
    displaytime = 5
    pluginname = "File Accn"
    plugininfo = "place to file things. "
    accn = ''

    def __init__(self, *args, **kwargs):
        PiInfoScreen.__init__(self, args[0], kwargs)

        self.surface.fill(COLORS['CLOUD'])
        self.hint_text.string = "settings will\n be here soon!"
        self.title.update()
        RACK_DB.next_location()

    def event_handler(self, event):
        # if event.type == KEYDOWN and event.key == K_RETURN:
        #     accn = self.accn_input.value
        #     if accn != '':
        #         RACK_DB.file_accn(accn)
        #         print RACK_DB.last_stored
        #         print accn
        # self.accn_input.update(event)
        pass

    def update_locations(self):
        pass

    def showScreen(self):
        self.hint_surface.blit(self.hint_text.update(), (0, 0))
        self.clock.text = strftime("%H:%M", localtime(time()))
        self.clock.update()
        self.screen.blit(self.surface, (0, 0))
        return self.screen
