import sys
import pygame
import gui_objects
from time import strftime, localtime
# from time import time, gmtime, strftime, mktime, localtime
from pprint import pprint
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS, TITLE_RECT, ROWS
from displayscreen import PiInfoScreen
from database_functions import RACK_DB
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
        # draw the title background
        self.accn_surface.fill(COLORS['CLOUD'])
        RACK_DB.locate_next()

        self.title = gui_objects.text_label(
            surface=self.title_surface,
            font=self.fonts['title_font']['font'],
            text=self.name,
            color=COLORS[self.fonts['title_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=TITLE_RECT,
            rounded=True,
            background_color=COLORS[self.color])
        ###---------------------------------------------
        # These are hardcoded information labels
        #-----------------------------------------------
        
        self.hint_rect = pygame.Rect(0, 120, 320, 70)
        self.hint_surface = self.surface.subsurface(self.hint_rect)
        self.hint_text = self.render_textrect(
            string="Here is the place where\nsettings will be set",
            font=self.fonts['swipe_font']['font'],
            rect=self.hint_rect,
            text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            # background_color=COLORS['RED'],
            justification=1,
            vjustification=1)

        self.info0_rect = pygame.Rect(5, 93, 140, 25)
        self.info0_surface = self.surface.subsurface(self.info0_rect)
        self.info0 =  gui_objects.text_label(
            surface=self.info0_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info0_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])

        self.info1_rect = pygame.Rect(5, 200, 140, 20)
        self.info1_surface = self.surface.subsurface(self.info1_rect)
        self.info1 =  gui_objects.text_label(
            surface=self.info1_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info1_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])



        ##------------------------------------------
        # These information labels will change when the screen is updated
        #----------------------------------------
        self.info2_rect = pygame.Rect(120, 93, 160, 25)
        self.info2_surface = self.surface.subsurface(self.info2_rect)
        self.info2 =  gui_objects.text_label(
            surface=self.info2_surface,
            font=self.fonts['default_font']['font'],
            text="",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info2_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])

        self.info3_rect = pygame.Rect(150, 200, 160, 20)
        self.info3_surface = self.surface.subsurface(self.info3_rect)
        self.info3 =  gui_objects.text_label(
            surface=self.info3_surface,
            font=self.fonts['default_font']['font'],
            text="",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info3_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.text_objects = [self.title, self.info0, self.info1, self.info2, self.info3]


        for thing in self.text_objects: 
            thing.update()


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
        # self.info3.text = RACK_DB.last_stored
        # self.info3.update()


        # self.info2.text = file_string
        # self.info2.update()

        self.hint_surface.blit(self.hint_text, (0, 0))
        # self.update_locations()

        self.screen.blit(self.surface, (0, 0))
        return self.screen
