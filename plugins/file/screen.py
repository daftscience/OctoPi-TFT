import sys
import pygame
import gui_objects
from time import strftime, localtime
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
        self.title.update()
        self.hint_text.string = "scan to store\nswipe up for keyboard"
        RACK_DB.next_location()

        # Hardcoded info boxes....
        # because they don't change, they should
        # NOT BE UDPATED
        self.info0_rect = pygame.Rect(5, 93, 140, 25)
        self.info0_surface = self.surface.subsurface(self.info0_rect)
        self.info0 = gui_objects.text_label(
            surface=self.info0_surface,
            font=self.fonts['default_font']['font'],
            text="Location to file: ",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info0_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.info0.update()
        self.info1_rect = pygame.Rect(5, 210, 130, 20)
        self.info1_surface = self.surface.subsurface(self.info1_rect)
        self.info1 = gui_objects.text_label(
            surface=self.info1_surface,
            font=self.fonts['default_font']['font'],
            text="Last sample stored: ",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info1_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.info1.update()

        # ------------------------------------------
        # These information labels will change when the screen is updated
           # They will need to be updated
        #----------------------------------------
        self.info2_rect = pygame.Rect(0, 93, 100, 25)
        self.info2_rect.centerx = 160
        self.info2_surface = self.surface.subsurface(self.info2_rect)
        self.info2 = gui_objects.text_label(
            surface=self.info2_surface,
            font=self.fonts['info_font']['font'],
            text="Unavailable Location",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info2_rect,
            valign='bottom',
            align="center",
            background_color=COLORS['CLOUD'])

        self.info3_rect = pygame.Rect(130, 210, 160, 20)
        self.info3_rect.left = self.info1_rect.right + 3
        self.info3_surface = self.surface.subsurface(self.info3_rect)
        self.info3 = gui_objects.text_label(
            surface=self.info3_surface,
            font=self.fonts['info_font']['font'],
            text="Unavailable",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info3_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])

    def event_handler(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.accn_input.value
            if accn != '':
                RACK_DB.file_accn(accn)
        self.accn_input.update(event)

    def update_locations(self):
        pass

    def showScreen(self):
        self.hint_surface.blit(self.hint_text.update(), (0, 0))

        # change this to use gui_objects.format_location somehow
        # row = ROWS[str(RACK_DB.next_row)]
        # rack = str(RACK_DB.next_rack)
        # column = str(RACK_DB.next_column)
        # day = strftime('%a', localtime(RACK_DB.rack_date))
        # day = RACK_DB.rack_day
        # print day
        # print row
        # print rack
        # print column

        # file_string = day + rack + ': ' + row + '' + column
        # pprint(RACK_DB.next)

        file_string = gui_objects.format_location(RACK_DB.next)
        try:
            self.info3.text = str(RACK_DB.last_filed['accn'])
        except:
            self.info3.text = "Unavailable"
        # print "info"+self.info3.text
        self.info3.update()

        self.info2.text = file_string
        self.info2.update()

        # print ( pygame.mouse.get_pos())
        # self.accn_surface.fill(COLORS['CLOUD'])
        # self.accn_input.draw(self.surface)
        self.accn_input.draw(self.surface, self.accn_surface, COLORS['CLOUD'])

        # self.title.update()

        self.clock.text = strftime("%H:%M", localtime(time()))
        self.clock.update()
        self.screen.blit(self.surface, (0, 0))
        self.clock.update()
        return self.screen
