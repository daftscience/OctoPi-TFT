import sys
import os
# import pygameui
import pygame
from time import strftime, localtime, time, sleep
from change_time import change_time
from global_variables import COLORS, piscreenevents, CLOCK_DIRTY, ICONS, SWIPE_UP, SWIPE_DOWN
from displayscreen import PiInfoScreen
from database import RACK_DB
from button import button
sys.dont_write_bytecode = True

print "test"
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
        self.setting_visible = False
        self.clock_dirty = False
        self.minus = ICONS.unicode('down-open')
        self.plus = ICONS.unicode('up-open')
        self.surface.fill(COLORS['CLOUD'])
        self.hint_text.string = "Swipe up for settings\n Swipe horizontally to exit"
        self.title.update()
        self.adjust_time = change_time()
# pygame.font.Font(ICONS.font_location, 45)
        self.button_settings = {
            # 'hover': COLORS['BLUE-GREY']['200'],
            'hover': COLORS['BLUE-GREY']['100'],
            'font': ICONS.font_location,
            'bg': COLORS['BLUE-GREY']['100'],
            'fg': COLORS[self.color_name]['300'],
            'clear_color': COLORS['CLOUD'],
            'border': False,
            'fontsize': 18,
            'surface': self.surface
        }
        button_width = 100
        button_height = 30
        margin = 5

        startx = 55
        starty = 130
        x = startx
        y = starty
        self.inc_hour_btn = button(
            text=self.plus,
            width=button_width,
            height=button_height,
            command=self.inc_hour,
            **self.button_settings)
        self.inc_hour_btn.rect.center = (x, y)
        x += button_width + margin

        self.inc_min_btn = button(
            text=self.plus,
            width=button_width,
            height=button_height,
            command=self.inc_min,
            **self.button_settings)
        self.inc_min_btn.rect.center = (x, y)
        x += button_width + margin

        self.inc_day_btn = button(
            text=self.plus,
            width=button_width,
            height=button_height,
            command=self.inc_day,
            **self.button_settings)
        self.inc_day_btn.rect.center = (x, y)
        x = startx
        y += button_height + margin


        self.hour_rect = pygame.Rect(x, y, button_width, button_height)
        self.hour_rect.center = (x,y)
        self.hour_surface = self.surface.subsurface(self.hour_rect)
        self.hour = gui_objects.text_label(
            surface=self.hour_surface,
            font=self.fonts['default_font']['font'],
            text=strftime("%H", localtime(time())),
            color=self.fonts['default_font']['color'],
            # Rect(left, top, width, height) -> Rect
            rect=self.hour_rect,
            valign='center',
            align="center",
            background_color=COLORS['CLOUD'])
        self.hour.update()
        x += button_width + margin

        self.min_rect = pygame.Rect(0, 0, button_width, button_height)
        self.min_rect.center = (x,y)
        self.min_surface = self.surface.subsurface(self.min_rect)
        self.min = gui_objects.text_label(
            surface=self.min_surface,
            font=self.fonts['default_font']['font'],
            text=strftime("%M", localtime(time())),
            color=COLORS['BLUE-GREY']['700'],
            # Rect(left, top, width, height) -> Rect
            rect=self.min_rect,
            valign='center',
            align="center",
            background_color=COLORS['CLOUD'])
        self.min.update()
        x += button_width + margin

        self.day_rect = pygame.Rect(x, y, button_width, button_height)
        self.day_rect.center = (x,y)
        self.day_surface = self.surface.subsurface(self.day_rect)
        self.day = gui_objects.text_label(
            surface=self.day_surface,
            font=self.fonts['default_font']['font'],
            text=strftime("%b", localtime(time())),
            color=self.fonts['default_font']['color'],
            # Rect(left, top, width, height) -> Rect
            rect=self.day_rect,
            valign='center',
            align="center",
            background_color=COLORS['CLOUD'])
        self.day.update()
        x = startx
        y += button_height + margin

        self.dec_hour_btn = button(
            text=self.minus,
            width=button_width,
            height=button_height,
            command=self.dec_hour,
            **self.button_settings)
        self.dec_hour_btn.rect.center = (x, y)
        x += button_width + margin
        self.dec_min_btn = button(
            text=self.minus,
            width=button_width,
            height=button_height,
            command=self.dec_min,
            **self.button_settings)
        self.dec_min_btn.rect.center = (x, y)
        x += button_width + margin
        self.dec_day_btn = button(
            text=self.minus,
            width=button_width,
            height=button_height,
            command=self.dec_day,
            **self.button_settings)
        self.dec_day_btn.rect.center = (x, y)

        self.buttons = [
            self.inc_hour_btn,
            self.inc_day_btn,
            self.inc_min_btn,
            self.dec_min_btn,
            self.dec_day_btn,
            self.dec_hour_btn]

    def inc_min(self):
        self.adjust_time.change("minutes", 1)
        # print('running callback')

    def dec_min(self):
        self.adjust_time.change("minutes", -1)
        # print('running callback 2')

    def inc_day(self):
        self.adjust_time.change("days", 1)
        # print('running callback')

    def dec_day(self):
        self.adjust_time.change("days", -1)
        # print('running callback 2')

    def inc_hour(self):
        self.adjust_time.change("hours", 1)
        # print('running callback')

    def dec_hour(self):
        self.adjust_time.change("hours", -1)
        # print('running callback 2')

    def event_handler(self, event):
        if event.type == SWIPE_UP and self.setting_visible == False:
            self.setting_visible = True
            return
        if event.type == SWIPE_DOWN:
            self.setting_visible = False
            self.exit_function()
            return

        if event.type == pygame.MOUSEBUTTONUP:
            for b in self.buttons:
                if b.get_event(event):
                    pygame.time.Clock()
                    self.clock_dirty = True
        else:
            return
    def show_settings(self):
        self.hint_surface.fill(COLORS['CLOUD'])
        self.hour.update()
        self.clock.text = strftime("%H:%M", localtime(time()))
        self.hour.text = strftime("%H", localtime(time()))
        self.hour.update()
        self.min.text = strftime("%M", localtime(time()))
        self.min.update()
        self.day.text = strftime("%b-%d", localtime(time()))
        self.day.update()
        self.clock.update()
        for b in self.buttons:
            b.update()
        self.screen.blit(self.surface, (0, 0))

    def showScreen(self):
        if self.setting_visible == True:
            self.settings_screen = self.show_settings()
            return self.screen
        else:
            self.hint_surface.blit(self.hint_text.update(), (0, 0))
            self.clock.text = strftime("%H:%M", localtime(time()))
            self.clock.update()
            self.screen.blit(self.surface, (0, 0))
            return self.screen

    def exit_function(self):
        self.setting_visible = False
        self.screen.fill(COLORS['CLOUD'])
        for b in self.buttons:
            b.clear()
        self.screen.blit(self.surface, (0,0))
        if self.clock_dirty:
            print "clock is dirty"
            self.screen.fill(COLORS['CLOUD'])
            self.title.update()
            self.screen.blit(self.title.surface, self.title.rect)
            self.hint_text.string = "Saving..."
            self.clock.text = strftime("%H:%M", localtime(time()))
            self.clock.update()
            self.hint_surface.blit(self.hint_text.update(), (0, 0))
            self.title.update()
            self.title.update()
            self.screen.blit(self.hint_surface, self.hint_rect)
            pygame.display.update()
            sleep(2)
            os.popen("hwclock -w", 'r', 1)
            self.hint_surface.fill(COLORS['CLOUD'])
            self.hint_text.string = "Swipe to adjust time\n Swipe horizontally to exit"
            self.screen.blit(self.hint_surface, self.hint_rect)
            self.clock_dirty = False
        else:
            return
