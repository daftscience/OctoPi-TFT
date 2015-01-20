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
        self.font_size  =   int(self.pluginConfig["title_settings"]["size"])
        self.font       =   self.pluginConfig["title_settings"]["font"]
        self.font_color =   self.pluginConfig["title_settings"]["color"]
        self.default_font = os.path.join(self.plugindir, "resources", self.font)
        self.large_default_font = pygame.font.Font(self.default_font, self.font_size)
        self.small_default_font = pygame.font.Font(self.default_font, self.font_size)

        self.input_font_face = self.pluginConfig["input_settings"]["font"]
        self.input_font_size = int(self.pluginConfig["input_settings"]["size"])
        self.input_font_color = self.pluginConfig["input_settings"]["color"]
        self.input_font_location = os.path.join(self.plugindir, "resources", self.input_font_face)
        self.input_font = pygame.font.Font(self.input_font_location, self.input_font_size)
        

        self.name = self.pluginConfig["plugin_info"]["name"]
        self.color = self.pluginConfig["plugin_info"]["color"]


        self.accn_input = eztext.Input(
                    font=self.input_font,
                    maxlength=20, 
                    color=COLORS[self.input_font_color], 
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
                            font=self.large_default_font, 
                            text=self.name, 
                            color=COLORS[self.font_color],
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
