import sys
import pygame
import gui_objects
from time import strftime, localtime, time
from pprint import pprint
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS
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

        self.timer = False
        self.timeout = 0
        self.timeout_delay = 4  # in seconds
        self.new_result = False

        self.surface.fill(COLORS['CLOUD'])
        self.hint_text.string = "scan to locate\nswipe up for keyboard"
        self.title.update()
        self.hint_surface.blit(self.hint_text.update(), (0, 0))

        RACK_DB.next_location()

        # This is the box where location results go
        self.result_rect = pygame.Rect(0, 200, 320, 60)
        self.result_text = gui_objects.render_textrect(
            string="",
            font=self.fonts['result_font']['font'],
            rect=self.result_rect,
            text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            justification=1,
            FontPath=self.fonts['result_font']['path'],
            cutoff=False,
            MinFont=self.fonts['result_font']['size'] - 8,
            MaxFont=self.fonts['result_font']['size'],
            shrink=True,
            vjustification=1)

        # An info box
        self.info0_rect = pygame.Rect(5, 93, 310, 25)
        self.info0_surface = self.surface.subsurface(self.info0_rect)
        self.info0 = gui_objects.text_label(
            surface=self.info0_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            rect=self.info0_rect,
            valign='bottom',
            align="center",
            background_color=COLORS['CLOUD'])

        # another info box
        self.info1_rect = pygame.Rect(5, 205, 310, 20)
        self.info1_surface = self.surface.subsurface(self.info1_rect)
        self.info1 = gui_objects.text_label(
            surface=self.info1_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info1_rect,
            valign='center',
            align="center",
            background_color=COLORS['CLOUD'])

    def reset(self):
        self.hint_surface.fill(COLORS['CLOUD'])
        self.result_text.font = self.fonts['result_font']['font']
        self.info0.text = ''
        self.info0.update()
        self.info1.text = ''
        self.info1.update()
        self.result_text.cutoff = False

    def event_handler(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.accn_input.value
            if accn != '':
                self.new_result = True
                self.reset()
                self.timeout = time() + self.timeout_delay
                self.timer = True
                result = RACK_DB.find_accn(accn)
                if not result:
                    self.result_text.string = "not found"
                    self.info0.text = accn
                    self.info1.text = "sorry, not found"
                else:
                    self.info0.text = "Accn #: " + accn
                    self.result_text.string = ''
                    if len(result) <= 4:
                        if len(result) == 1:
                            self.info1.text = str(
                                len(result)) + ' location found'
                        else:
                            self.info1.text = str(
                                len(result)) + ' locations found'
                        reversed_list = reversed(result)
                    else:
                        self.info1.text = "Showing last 4 locations"
                        reversed_list = reversed(result[-4:])
                    formated = []
                    for item in reversed_list:
                        formated.append(gui_objects.format_location(item))
                    self.result_text.string = "\n".join(formated)
        self.accn_input.update(event)

    def update_locations(self):
        pass

    def showScreen(self):
        if self.timer:
            if self.timeout > time():
                if self.new_result:
                    self.new_result = False
                    # NOT FOUND
                    if self.result_text.string == "not found":
                        pass
                    else:
                        # FOUND
                        self.hint_surface.blit(
                            self.result_text.update(), (0, 0))
                pass
            else:
                self.timer = False
                self.reset()
                self.hint_surface.blit(self.hint_text.update(), (0, 0))

        self.clock.text = strftime("%H:%M", localtime(time()))
        self.clock.update()
        self.info0.update()
        self.info1.update()
        self.accn_input.draw(self.surface, self.accn_surface, COLORS['CLOUD'])
        self.screen.blit(self.surface, (0, 0))
        return self.screen
