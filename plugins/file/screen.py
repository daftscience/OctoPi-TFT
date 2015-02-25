import sys
import pygame
import os
import gui_objects
from pprint import pprint
from time import strftime, localtime
from eztext import Input
from pygame.locals import K_RETURN, KEYDOWN
from multi_font_text import multi_font
from global_variables import COLORS, SWIPE_UP, ICONS, DATABASE_SETTINGS, ROWS, piscreenevents
from displayscreen import PiInfoScreen
from keyboard import VirtualKeyboard
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
        self.vkey_surface = pygame.display.get_surface()
        # self.vkey_surface = self.surface.copy()
        self.vkey = VirtualKeyboard(self.vkey_surface)
        self.surface.fill(COLORS['CLOUD'])
        self.title.update()
        self.hint_text.string = "scan to store\nswipe up for keyboard"
        RACK_DB.next_location()
        # self.new_to_file = False

        # Hardcoded info boxes....
        # because they don't change, they should
        # NOT BE UDPATED


        self.barcode_input = Input()

        info0_text = "Next Location: "
        info0_size = self.fonts['default_font']['font'].render(info0_text, 1, (0,0,0))
        w = info0_size.get_rect().width
        self.info0_rect = pygame.Rect(5, 95, w, 25)
        self.info0_surface = self.surface.subsurface(self.info0_rect)
        self.info0 = gui_objects.text_label(
            surface=self.info0_surface,
            font=self.fonts['default_font']['font'],
            text=info0_text,
            color=self.fonts['default_font']['color'],
            # Rect(left, top, width, height) -> Rect
            rect=self.info0_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.info0.update()
        # ------------------------------------------
        # These information labels will change when the screen is updated
        # They will need to be updated
        #----------------------------------------
        self.info2_rect = pygame.Rect(0, 95, 100, 25)
        self.info2_rect.left = self.info0_rect.right + 1
        self.info2_surface = self.surface.subsurface(self.info2_rect)
        self.info2 = gui_objects.text_label(
            surface=self.info2_surface,
            font=self.fonts['default_font']['font'],
            text="Unavailable Location",
            color=self.fonts['info_font']['color'],
            rect=self.info2_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])

        # location dots!
        self.empty_dot = ICONS.unicode('checkbox-blank-circle-outline')
        self.full_dot = ICONS.unicode('checkbox-blank-circle')
        self.select_dot = ICONS.unicode('plus-circled')

        self.location_indicator_rect = pygame.Rect(0, 200, 320, 35)
        self.location_indicator_surface = self.surface.subsurface(self.location_indicator_rect)
        li_items = []
        self.location_indicator = multi_font(self.location_indicator_surface, li_items, COLORS['CLOUD'])
        # li_row_font = 'OpenSans-Regular.ttf'
        li_row_font = 'OpenSans-Semibold.ttf'
        self.li_row_font = os.path.join("resources/fonts", li_row_font)
        self.dirty = True
        self.update_indicator()



    def update_indicator(self):
        li_items = []
        item = {
            'font_location': self.li_row_font,
            'text': ROWS[str(RACK_DB.next['row'])]+' ',
            'size': 23,
            'color': self.color
        }
        li_items.append(item)
        # self.info1.text = ''
        size = 18
        while len(li_items) - 1 < RACK_DB.next['column']:
            if (len(li_items)) == RACK_DB.next['column']:
                text = self.select_dot
                color = self.color
            else:
                text = self.full_dot
                color = COLORS[self.color_name]["300"]
            item = {
                'font_location': ICONS.font_location,
                'text': text,
                'size': size,
                'color': color
            }
            li_items.append(item)
        text = self.empty_dot
        color = COLORS['BLUE-GREY']['500']
        while len(li_items)-1 < DATABASE_SETTINGS['columns']:
            item = {
                'font_location': ICONS.font_location,
                'text': text,
                'size': size,
                'color': color
            }
            li_items.append(item)
        self.location_indicator.items = li_items
        self.location_indicator.dirty = True


    def event_handler(self, event):
        # print event.type
        if event.type == SWIPE_UP:
            # vkey = VirtualKeyboard(screen)
            tmp = self.vkey.run('')
            accn = tmp
            if accn != '':
                RACK_DB.file_accn(accn)
                self.update_indicator()
            return
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.barcode_input.value
            if accn != '':
                RACK_DB.file_accn(accn)
            self.update_indicator()
        self.barcode_input.update(event)
        # if event.type == piscreenevents["time_changed"]
            # print("time changed")
    def update_locations(self):
        pass

    def showScreen(self):
        # if self.new_to_file:
        RACK_DB.next_location()
        self.hint_surface.blit(self.hint_text.update(), (0, 0))
        file_string = gui_objects.format_location(RACK_DB.next)

        try:
            self.accn_box.text = "Filed: " + str(RACK_DB.last_filed['accn'])
        except:
            self.accn_box.text = "Unavailable"
        # self.info1.update()
        self.location_indicator.update()


        self.info2.text = file_string
        self.info2.update()
        self.clock.text = strftime("%H:%M", localtime(time()))
        self.screen.blit(self.surface, (0, 0))
        self.clock.update()
        self.accn_box.update()
        return self.screen
