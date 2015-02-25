import pygame
import sys
import os
import urllib2
import gui_objects
import eztext
from configobj import ConfigObj
from validate import Validator
from global_variables import COLORS, TITLE_RECT, FONTS, PLUGIN_VALIDATOR

from pprint import pprint
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class PiInfoScreen():

    # Set default names
    pluginname = "UNDEFINED"
    plugininfo = "You should set pluginname and plugininfo in your plugin subclass"
    # List of screen sizes supported by the script
    supportedsizes = [(320, 240)]

    # Refresh time = how often the data on the screen should be updated
    # (seconds)
    refreshtime = 30

    # How long screen should be displayed before moving on to next screen (seconds)
    # only relevant when screen is autmatically changing screens
    # rather than waiting for key press
    displaytime = 5
    loadingMessage = "Ummm?"

    # This function should not be overriden
    def __init__(self, screensize, scale=True, userevents=None):

        # Set config filepath...
        self.plugindir = os.path.dirname(
            sys.modules[self.__class__.__module__].__file__)
        self.banner_location = os.path.join(self.plugindir, 'resources', 'banner.png')
        self.configfile = os.path.join(self.plugindir, "config", "screen.ini")
        # ...and read the config file
        self.readConfig()
        # Save the requested screen size
        self.screensize = screensize
        self.userevents = userevents
        # pprint(self.userevents)
        # Check requested screen size is compatible and set supported property
        if screensize not in self.supportedsizes:
            self.supported = False
        else:
            self.supported = True

        # Initialise pygame for the class
        if self.supported or scale:
            pygame.init()
            self.screen = pygame.display.set_mode(self.screensize)
            self.surfacesize = self.supportedsizes[0]
            self.surface = pygame.Surface(self.surfacesize)

        self.title_surface = self.surface.subsurface(TITLE_RECT)
        self.title = gui_objects.title_banner(
            surface=self.title_surface,
            title_icon=self.title_icon,
            font=self.fonts['title_font']['font'],
            text=self.name,
            color=self.fonts['title_font']['color'],
            rect=TITLE_RECT,
            rounded=True,
            background_color=self.color,
            banner_location = self.banner_location)

        self.hint_rect = pygame.Rect(0, 120, 320, 70)
        # self.hint_rect = pygame.Rect(0, 120, 320, 60)
        self.hint_surface = self.surface.subsurface(self.hint_rect)
        self.hint_text = gui_objects.render_textrect(
            string="scan to locate\nswipe up for keyboard",
            font=FONTS['swipe_font']['font'],
            rect=self.hint_rect,
            text_color=self.color,
            background_color=COLORS['CLOUD'],
            justification=1,
            FontPath=FONTS['swipe_font']['path'],
            cutoff=False,
            MinFont=FONTS['swipe_font']['size'] - 4,
            MaxFont=FONTS['swipe_font']['size'],
            shrink=True,
            vjustification=1)

        self.clock_rect = pygame.Rect(255, 0, 60, 25)
        self.clock_surface = self.surface.subsurface(self.clock_rect)
        self.clock = gui_objects.text_label(
            surface=self.clock_surface,
            font=FONTS['clock_font']['font'],
            text='',
            color=FONTS['clock_font']['color'],
            rect=self.clock_rect,
            valign='bottom',
            align="right",
            background_color=COLORS['CLOUD'])

        self.accn_rect = pygame.Rect(5, 0, 250, 25)
        self.accn_surface = self.surface.subsurface(self.accn_rect)
        self.accn_box = gui_objects.text_label(
            surface=self.accn_surface,
            font=self.fonts['input_font']['font'],
            text='',
            color=self.fonts['input_font']['color'],
            rect=self.accn_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.accn_box.update()
        # print self.name
        # print "fontRect " + str(self.accn_box.fontRect.height)
        # print "rect " + str(self.accn_box.rect.height)

    # Read the plugin's config file and dump contents to a dictionary
    def readConfig(self):
        validator = Validator()
        # print self.configfile
        configspec = ConfigObj(PLUGIN_VALIDATOR, interpolation=False, list_values=True,
                       _inspec=True)
        self.pluginConfig = ConfigObj(self.configfile, configspec=configspec)
        result = self.pluginConfig.validate(validator)
        if result != True:
            pprint(result)
            print 'Config file validation failed!'
        # print "reading config file: " + self.configfile

        self.setPluginVariables()

    # Can be overriden to allow plugin to change option type
    # Default method is to treat all options as strings
    # If option needs different type (bool, int, float) then this should be
    # done here
    # Alternatively, plugin can just read variables from the pluginConfig
    # dictionary that's created
    # Any other variables (colours, fonts etc.) should be defined here
    def setPluginVariables(self):

        self.name = self.pluginConfig["plugin_info"]["name"]
        self.color_name = self.pluginConfig["plugin_info"]["color"]
        self.shade = self.pluginConfig["plugin_info"]["shade"]
        self.color = COLORS[self.pluginConfig["plugin_info"]["color"]][self.shade]
        self.loadingMessage = self.pluginConfig[
            "plugin_info"]['loading_message']

        try:
            self.title_icon = self.pluginConfig['ui_settings']['title_icon']
        except:
            self.title_icon = 0xf058
            # print "no title icon for this plugin"

        # create a dict with fonts defined in config/settings.ini
        self.fonts = {}
        for key in self.pluginConfig['fonts']:
            font = self.pluginConfig['fonts'][key]

            font_file = font['font']
            font_size = font['size']
            font_shade = font['shade']
            # font_size = int(font['size'])
            font_color = COLORS[font['color']][font_shade]

            font_location = os.path.join("resources/fonts", font_file)

            self.fonts[key] = {
                'font': pygame.font.Font(font_location, font_size),
                'color': font_color,
                'path': font_location,
                'size': font_size}

        # if self.pluginConfig["ui_settings"]["has_input"] == 'True':
        #     self.has_accn_input = True
        # else:
        #     self.has_accn_input = False
        #     self.accn_input = None

    # Tells the main script that the plugin is compatible with the requested
    # screen size
    def supported(self):
        return self.supported

    # Returns the refresh time
    def refreshtime(self):
        return self.refreshtime

    # Returns the display time
    def displaytime(self):
        return self.displaytime

    # Returns a short description of the script
    # displayed when user requests list of installed plugins
    def showInfo(self):
        return self.plugininfo

    # Returns name of the plugin
    def screenName(self):
        return self.pluginname

    def loadingMessage():
        return self.loadingMessage

    # Handle button events
    # These should be overriden by screens if required

    def Button1Click(self):
        pass

    def Button2Click(self):
        pass

    def Button3Click(self):
        pass

    def Button4Click(self):
        pass


    def LoadImage(self, fileName, solid=False):
        image = pygame.image.load(fileName)
        image = image.convert()
        if not solid:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Draws a progress bar
    def showProgress(self, position, barsize,bordercolour, fillcolour, bgcolour):
        try:
            if position < 0:
                position = 0
            if position > 1:
                position = 1
        except:
            position = 0
        progress = pygame.Surface(barsize)
        pygame.draw.rect(progress, bgcolour, (0, 0, barsize[0], barsize[1]))
        progresswidth = int(barsize[0] * position)
        pygame.draw.rect(
            progress, fillcolour, (0, 0, progresswidth, barsize[1]))
        pygame.draw.rect(
            progress, bordercolour, (0, 0, barsize[0], barsize[1]), 1)
        return progress

    def exit_function(self):
        pass

    # Main function - returns screen to main script
    # Will be overriden by plugins
    # Defaults to showing name and description of plugin
    def showScreen(self):
        self.screen.fill([0, 0, 0])
        screentext = pygame.font.SysFont("freesans", 20).render(
            "%s: %s." % (self.pluginname, self.plugininfo), 1, (255, 255, 255))
        screenrect = screentext.get_rect()
        screenrect.centerx = self.screen.get_rect().centerx
        screenrect.centery = self.screen.get_rect().centery
        self.screen.blit(screentext, screenrect)

        return self.screen

    def event_handler(self, event):
        pass

    def setUpdateTimer(self):
        pass
        # pygame.time.set_timer(self.userevents["update"], 0)
        # pygame.time.set_timer(
            # self.userevents["update"], int(self.refreshtime * 1000))
