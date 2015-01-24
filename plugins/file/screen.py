import sys
import pygame
import gui_objects
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS, TITLE_RECT
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
        self.create_objects()
        self.info_rect = pygame.Rect(0, 120, 320, 70)
        self.info_surface = self.surface.subsurface(self.info_rect)

        self.create_info_area()

    # default.py reads the events and will send them to this function.
    # by default, this function contains "pass"
    def event_handler(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.accn_input.value
            RACK_DB.file_accn(accn)
            print RACK_DB.last_stored
            print accn
        self.accn_input.update(event)

    def create_objects(self):
        self.title = gui_objects.text_label(
            surface=self.title_surface,
            font=self.fonts['title_font']['font'],
            text=self.name,
            color=COLORS[self.fonts['title_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=TITLE_RECT,
            background_color=COLORS[self.color])

        self.swipe_hint = gui_objects.text_label(
            surface=self.swipe_hint_surface,
            font=self.fonts['swipe_font']['font'],
            text='<    Swipe    >',
            color=COLORS[self.fonts['swipe_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=TITLE_RECT,
            background_color=COLORS[self.color])

    def create_info_area(self):

        self.info_text = self.render_textrect(
            string="Scan to store...\nSwipe up for keyboard...",
            font=self.fonts['info_font']['font'],
            rect=self.info_rect,
            text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            justification=1,
            vjustification=1)

        self.info_surface.blit(self.info_text, (0, 0))

    def showScreen(self):

        self.surface.fill(COLORS['CLOUD'])
        gui_objects.DrawRoundRect(
            self.title_surface,
            COLORS[
                self.color],
            self.title_surface.get_rect(),
            0,
            3,
            3)
        self.accn_input.draw(self.surface)
        self.title.update()
        self.swipe_hint.update()
        self.info_surface.blit(self.info_text, (0, 0))

        # self.info_area.update()

        self.screen.blit(self.surface, (0, 0))
        return self.screen
