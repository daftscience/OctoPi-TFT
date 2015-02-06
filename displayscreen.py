'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import pygame
import configobj
import sys
import os
import urllib2
import gui_objects
import eztext
from global_variables import COLORS, TITLE_RECT
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

        if self.has_accn_input == True:
            self.accn_surface = self.surface.subsurface(5, 0, 260, 27)
            self.accn_input = eztext.Input(
                font=self.fonts['input_font']['font'],
                maxlength=13,
                color=COLORS[self.fonts['input_font']['color']],
                prompt='Accn #: ',
                x=5, y=2)


        self.title_surface = self.surface.subsurface(TITLE_RECT)
        self.title = gui_objects.title_banner(
            surface=self.title_surface,
            title_icon=self.title_icon,
            font=self.fonts['title_font']['font'],
            text=self.name,
            color=COLORS[self.fonts['title_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=TITLE_RECT,
            rounded=True,
            background_color=COLORS[self.color],
            banner_location = self.banner_location)

        self.hint_rect = pygame.Rect(0, 120, 320, 70)
        # self.hint_rect = pygame.Rect(0, 120, 320, 60)
        self.hint_surface = self.surface.subsurface(self.hint_rect)
        self.hint_text = gui_objects.render_textrect(
            string="scan to locate\nswipe up for keyboard",
            font=self.fonts['swipe_font']['font'],
            rect=self.hint_rect,
            text_color=COLORS[self.color],
            # text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            justification=1,
            FontPath=self.fonts['swipe_font']['path'],
            cutoff=False,
            MinFont=self.fonts['swipe_font']['size'] - 4,
            MaxFont=self.fonts['swipe_font']['size'],
            shrink=True,
            vjustification=1)

        self.clock_rect = pygame.Rect(265, 2, 50, 25)
        self.clock_surface = self.surface.subsurface(self.clock_rect)
        self.clock = gui_objects.text_label(
            surface=self.clock_surface,
            font=self.fonts['clock_font']['font'],
            text='',
            color=COLORS[self.fonts['clock_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.clock_rect,
            valign='center',
            align="right",
            background_color=COLORS['CLOUD'])

    # Read the plugin's config file and dump contents to a dictionary
    def readConfig(self):
        print "reading config file: " + self.configfile
        try:
            self.pluginConfig = configobj.ConfigObj(self.configfile)
        except:
            print "Error reading config/settings.ini"

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
        self.color = self.pluginConfig["plugin_info"]["color"]
        self.loadingMessage = self.pluginConfig[
            "plugin_info"]['loading_message']

        try:
            self.title_icon = self.pluginConfig['ui_settings']['title_icon']
        except:
            self.title_icon = 0xf058
            print "no title icon for this plugin"

        # create a dict with fonts defined in config/settings.ini
        self.fonts = {}
        for key in self.pluginConfig['fonts']:
            font = self.pluginConfig['fonts'][key]

            font_file = font['font']
            font_size = int(font['size'])
            font_color = font['color']

            font_location = os.path.join("resources/fonts", font_file)

            self.fonts[key] = {
                'font': pygame.font.Font(font_location, font_size),
                'color': font_color,
                'path': font_location,
                'size': font_size}

        if self.pluginConfig["ui_settings"]["has_input"] == 'True':
            # self.has_accn = True
            self.has_accn_input = True
        else:
            self.has_accn_input = False
            self.accn_input = None

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

    # Get web page
    def getPage(self, url):
        user_agent = 'Mozilla/5 (Solaris 10) Gecko'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        the_page = response.read()
        return the_page

    # Function to get image and return in format pygame can use
    # def LoadImageFromUrl(self, url, solid=False):
    #     f = urllib.urlopen(url)
    #     buf = StringIO.StringIO(f.read())
    #     image = self.LoadImage(buf, solid)
    #     return image

    def LoadImage(self, fileName, solid=False):
        image = pygame.image.load(fileName)
        image = image.convert()
        if not solid:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Draws a progress bar
    def showProgress(self, position, barsize,
                     bordercolour, fillcolour, bgcolour):
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
        pygame.time.set_timer(self.userevents["update"], 0)
        pygame.time.set_timer(
            self.userevents["update"], int(self.refreshtime * 1000))
