import sys
import pygame
import gui_objects
from time import strftime, localtime
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS, RETURN_EVENT, ICONS, DATABASE_SETTINGS
from displayscreen import PiInfoScreen
from database import RACK_DB
sys.dont_write_bytecode = True


# For more information on the variables and functions in this file view
# displayscreen.py in the root folder of this project


class myScreen(PiInfoScreen):
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
        # self.new_to_file = False

        # Hardcoded info boxes....
        # because they don't change, they should
        # NOT BE UDPATED
        self.info0_rect = pygame.Rect(5, 93, 120, 25)
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

        self.empty_dot = ICONS.unicode('checkbox-blank-circle-outline')
        self.full_dot = ICONS.unicode('checkbox-blank-circle')
        self.select_dot = ICONS.unicode('plus-circled')
        self.fa = pygame.font.Font(ICONS.font_location, 20)
        print self.fa
        print self.fonts['default_font']['font']

        self.info1_rect = pygame.Rect(0, 200, 320, 20)
        self.info1_surface = self.surface.subsurface(self.info1_rect)
        self.info1 = gui_objects.text_label(
            surface=self.info1_surface,
            # font=self.fonts['default_font']['font'],
            font=self.fa,
            text='',
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info1_rect,
            valign='bottom',
            align="center",
            background_color=COLORS['CLOUD'])
        self.info1.update()

        # ------------------------------------------
        # These information labels will change when the screen is updated
           # They will need to be updated
        #----------------------------------------
        self.info2_rect = pygame.Rect(0, 93, 100, 25)
        self.info2_rect.left = self.info0_rect.right + 3
        self.info2_surface = self.surface.subsurface(self.info2_rect)
        self.info2 = gui_objects.text_label(
            surface=self.info2_surface,
            font=self.fonts['info_font']['font'],
            text="Unavailable Location",
            color=COLORS[self.fonts['info_font']['color']],
            rect=self.info2_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])

        # self.info3_rect = pygame.Rect(130, 210, 160, 20)
        # self.info3_rect.left = self.info1_rect.right + 3
        # self.info3_surface = self.surface.subsurface(self.info3_rect)
        # self.info3 = gui_objects.text_label(
        #     surface=self.info3_surface,
        #     font=self.fonts['info_font']['font'],
        #     text="Unavailable",
        #     color=COLORS[self.fonts['info_font']['color']],
        #     rect=self.info3_rect,
        #     valign='bottom',
        #     align="left",
        #     background_color=COLORS['CLOUD'])

    def event_handler(self, event):
        # print event.type
        if event.type == RETURN_EVENT:
            accn = event.value
            if accn != '':
                RACK_DB.file_accn(accn)
            return
        # if event.type == KEYDOWN and event.key == K_RETURN:
        #     accn = self.accn_input.value
        #     if accn != '':
        #         RACK_DB.file_accn(accn)
        # self.accn_input.update(event)


    def update_locations(self):
        pass

    def showScreen(self):
        # if self.new_to_file:

        self.hint_surface.blit(self.hint_text.update(), (0, 0))
        file_string = gui_objects.format_location(RACK_DB.next)
        self.info1.text = ''
        while len(self.info1.text) < RACK_DB.next['column']:
            if (len(self.info1.text)+1) == RACK_DB.next['column']:
                self.info1.text += self.select_dot
            else:    
                self.info1.text += self.full_dot
        while len(self.info1.text) < DATABASE_SETTINGS['columns']:
            self.info1.text += self.empty_dot








        try:
            self.accn_box.text = "Filed: " + str(RACK_DB.last_filed['accn'])
            # self.accn_box.text = "test"
        except:
            self.accn_box.text = "Unavailable"
        # self.info3.update()
        self.info1.update()
        self.info2.text = file_string
        self.info2.update()
        # self.accn_input.draw(self.surface, self.accn_surface, COLORS['CLOUD'])
        self.clock.text = strftime("%H:%M", localtime(time()))
        # self.clock.update()
        self.screen.blit(self.surface, (0, 0))
        self.clock.update()
        self.accn_box.update()
        return self.screen
