import os
import sys
import pygame
import gui_objects
from constants import COLORS, TITLE_RECT
from displayscreen import PiInfoScreen
import simplejson as json

sys.dont_write_bytecode = True

# from config import *

class myScreen(PiInfoScreen):
    # PiInfoScreen.__init__()
    refreshtime = 1
    displaytime = 5
    pluginname = "File Accn"
    plugininfo = "place to file things. "    

    def setPluginVariables(self):
        self.font_size  =   int(self.pluginConfig["title_settings"]["size"])
        self.font       =   self.pluginConfig["title_settings"]["font"]
        self.font_color =   self.pluginConfig["title_settings"]["color"]
        self.default_font = os.path.join(self.plugindir, "resources", self.font)         
        self.large_default_font = pygame.font.Font(self.default_font, self.font_size)
        self.small_default_font = pygame.font.Font(self.default_font, 22)
        self.name = self.pluginConfig["plugin_info"]["name"]
        self.color = self.pluginConfig["plugin_info"]["color"]



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
        

        
        self.screen.blit(self.surface, (0,0))

        return self.screen
