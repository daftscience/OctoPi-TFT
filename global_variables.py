import sys
import pygame
from configobj import ConfigObj
import os
import simplejson
from pprint import pprint
from parseIcons import icon
from validate import Validator
sys.dont_write_bytecode = True

DEBUG = False

# THIS SECTION IS TO READ THE CONFIG FILE
CONFIG_FILE = 'config/settings.ini'
CONFIG_SPEC = 'config/_config_validator.ini'
PLUGIN_VALIDATOR = 'config/_plugin_validator.ini'


# except:
    # print "Error reading config/settings.ini"

MATERIAL_COLORS = 'material_colors.json'

_COLORS = os.path.join('resources/', MATERIAL_COLORS)
_COLORS_FILE = open(_COLORS)
_JSON_COLORS = simplejson.load(_COLORS_FILE)
# pprint(_JSON_COLORS)
MATERIAL_COLORS={}
for color in _JSON_COLORS:
    # pprint(COLORS)
    MATERIAL_COLORS[color] = {}
    for shade in _JSON_COLORS[color]:
        tmp = pygame.color.Color(str(_JSON_COLORS[color][shade]))
        # print tmp
        MATERIAL_COLORS[color][shade] = (tmp[0], tmp[1], tmp[2])

MATERIAL_COLORS['CLOUD'] = (236, 240, 241)
MATERIAL_COLORS['ASPHALT'] = (52,  73,  94)
COLORS = MATERIAL_COLORS

# pprint(MATERIAL_COLORS)


CLOCK_DIRTY = False












validator = Validator()

# try:
configspec = ConfigObj(CONFIG_SPEC, interpolation=False, list_values=True,
                       _inspec=True)
_CONFIG = ConfigObj(CONFIG_FILE, configspec=configspec)

result = _CONFIG.validate(validator)
if result != True:
    print 'Config file validation failed!'
    pprint(result)
pygame.font.init()



_bg_color = _CONFIG['app_info']['background_color']
_bg_shade = _CONFIG['app_info']['shade']
BACKGROUND_COLOR = COLORS[_bg_color][_bg_shade]



# THIS SECTION IS TO READ THE FONTS
FONTS = {}
for key in _CONFIG['fonts']:
    font = _CONFIG['fonts'][key]

    font_file = font['font']
    font_size = font['size']
    font_shade = font['shade']
    font_color = COLORS[font['color']][font_shade]
    font_location = os.path.join("resources/fonts", font_file)
    FONTS[key] = {
        'font': pygame.font.Font(font_location, font_size),
        'color': font_color,
        'path': font_location,
        'size': font_size}
    # pprint(FONTS)

# Check if the banner needs to be redrawn
# then reset the value so the next load
# times are faster
if not DEBUG:
    REBUILD_BANNER = _CONFIG['title_banner']['REBUILD_BANNER']
    if REBUILD_BANNER:
        _CONFIG['title_banner']['REBUILD_BANNER'] = False
        _CONFIG.write()
else:
    REBUILD_BANNER = True
SHADING_QUALITY = _CONFIG['title_banner']['SHADING_QUALITY']
BORDER = _CONFIG['title_banner']['BORDER']
CORNER_RADIUS = _CONFIG['title_banner']['CORNER_RADIUS']
SHADING_ITERATIONS = _CONFIG['title_banner']['SHADING_ITERATIONS']

SCREEN_TIMEOUT = _CONFIG['settings']['screen_timeout']



# TITLE_RECT = pygame.Rect(3, 30, 314, 60)
# these probably shouldnt be here
TITLE_RECT = pygame.Rect(0, 25, 320, 70)
SWIPE_HINT_RECT = pygame.Rect(0, 210, 320, 30)


# this is where the icon stuff is kept
ICON_FONT_FILE = 'pifile.ttf'
ICON_FONT_JSON = 'config.json'
ICONS = icon(ICON_FONT_JSON, ICON_FONT_FILE)


# # DECLARE THE USER DEFINED EVENTS
# TFTBUTTONCLICK = pygame.USEREVENT + 1
# UPDATESCREEN = TFTBUTTONCLICK + 1
# NEXTSCREEN = UPDATESCREEN + 1
# NEWSCREEN = NEXTSCREEN + 1
# SLEEPEVENT = NEWSCREEN + 1
# SWIPE_UP = SLEEPEVENT + 1


###################################
# SCREEN BANNER VARIABLES
###################################


LOADING_MESSEGES = [
    "Creating Time-Loop Inversion Field",
    "Loading next loading message",
    "Randomizing memory access",
    "Tube Clamp Error",
    "Priming reagents",
    "Testing CP function",
    "Homing",
    "Running Enhanced clean on all probes"
]


# Set up some custom events
TFTBUTTONCLICK = pygame.USEREVENT + 1
UPDATESCREEN = TFTBUTTONCLICK + 1
NEXTSCREEN = UPDATESCREEN + 1
NEWSCREEN = NEXTSCREEN + 1
SLEEPEVENT = NEWSCREEN + 1
SWIPE_UP = SLEEPEVENT + 1
SWIPE_DOWN = SWIPE_UP + 1
TIME_CHANGED = SWIPE_DOWN + 1

# print "return event"
# print RETURN_EVENT
# print "---------------"
#############################################################################

##############################################################################
# Call back functions for TFT Buttons

def TFTBtn1Click(channel):
    tftscreen.backlight_off()


def TFTBtn2Click(channel):
    tftscreen.backlight_low()


def TFTBtn3Click(channel):
    tftscreen.backlight_med()


def TFTBtn4Click(channel):
    tftscreen.backlight_high()
# This code needs work-------------------------------------
# Set up the four TFT button events
click1event = pygame.event.Event(TFTBUTTONCLICK, button=1)
click2event = pygame.event.Event(TFTBUTTONCLICK, button=2)
click3event = pygame.event.Event(TFTBUTTONCLICK, button=3)
click4event = pygame.event.Event(TFTBUTTONCLICK, button=4)

# return_event = pygame.event.Event(RETURN_EVENT)

# Dict of events that are accessible to screens
piscreenevents = {
    "button": TFTBUTTONCLICK,
    "update": UPDATESCREEN,
    "nextscreen": NEXTSCREEN,
    "time_changed": TIME_CHANGED,
}