import os
import sys
import pygame
import gui_objects, eztext
from constants import COLORS, TITLE_RECT
from displayscreen import PiInfoScreen
import simplejson as json
from pygame.locals import K_RETURN, KEYDOWN

sys.dont_write_bytecode = True

# from config import *

class myScreen(PiInfoScreen):
    # PiInfoScreen.__init__()
    refreshtime = 1
    displaytime = 5
    pluginname = "File Accn"
    plugininfo = "place to file things. "
    accn = ''


    # Sets up variables. Some values are stored in /config/settings.ini
    def setPluginVariables(self):

        self.name = self.pluginConfig["plugin_info"]["name"]
        self.color = self.pluginConfig["plugin_info"]["color"]


        # create a dict with fonts defined in config/settings.ini
        self.fonts = {}
        for key in self.pluginConfig['fonts']:
            font = self.pluginConfig['fonts'][key]

            font_file   = font['font']
            font_size   = int(font['size'])
            font_color  = font['color']

            self.fonts[key] = {
                'font': pygame.font.Font(os.path.join(self.plugindir, "resources", font_file), font_size),
                'color': font_color}


        self.accn_input = eztext.Input(
                    font=self.fonts['input_font']['font'],
                    maxlength=20,
                    color=COLORS[self.fonts['input_font']['color']],
                    prompt='Accn #: ',
                    x=2, y=2)

    # default.py reads the events and will send them to this function.
    # by default, this function contains "pass"
    def event_handler(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.accn_input.value
            print accn
        self.accn_input.update(event)


    def display_title(self):

        title = gui_objects.text_label(
                            surface=self.surface,
                            font=self.fonts['title_font']['font'],
                            text=self.name,
                            color=COLORS[self.fonts['title_font']['color']],
                            # Rect(left, top, width, height) -> Rect
                            rect=TITLE_RECT,
                            background_color = COLORS[self.color])
        title.update()

    def showScreen(self):

        self.surface.fill(COLORS['CLOUD'])
        self.display_title()
        self.accn_input.draw(self.surface)
        self.screen.blit(self.surface, (0,0))

        return self.screen
