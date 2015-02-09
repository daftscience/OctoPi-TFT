import sys
import pygame
from configobj import ConfigObj
import os
from pprint import pprint
from parseIcons import icon
from validate import Validator
sys.dont_write_bytecode = True


# THIS SECTION IS TO READ THE CONFIG FILE
CONFIG_FILE = 'config/settings.ini'
CONFIG_SPEC = 'config/_config_validator.ini'
PLUGIN_VALIDATOR = 'config/_plugin_validator.ini'

validator = Validator()

# try:
configspec = ConfigObj(CONFIG_SPEC, interpolation=False, list_values=True,
                       _inspec=True)
_CONFIG = ConfigObj(CONFIG_FILE, configspec=configspec)

result = _CONFIG.validate(validator)
if result != True:
    print 'Config file validation failed!'
    pprint(result)

# except:
    # print "Error reading config/settings.ini"


pygame.font.init()
# THIS SECTION IS TO READ THE FONTS
FONTS = {}
for key in _CONFIG['fonts']:
    font = _CONFIG['fonts'][key]

    font_file = font['font']
    font_size = font['size']
    font_color = font['color']
    font_location = os.path.join("resources/fonts", font_file)
    FONTS[key] = {
        'font': pygame.font.Font(font_location, font_size),
        'color': font_color,
        'path': font_location,
        'size': font_size}
    # pprint(FONTS)

pprint(_CONFIG['title_banner'])
DATABASE_SETTINGS = {}
for key in _CONFIG['storage_settings']:
    DATABASE_SETTINGS[key] = _CONFIG['storage_settings'][key]

# Check if the banner needs to be redrawn
# then reset the value so the next load
# times are faster
REBUILD_BANNER = _CONFIG['title_banner']['REBUILD_BANNER']
if REBUILD_BANNER:
    _CONFIG['title_banner']['REBUILD_BANNER'] = False
    _CONFIG.write()

SHADING_QUALITY = _CONFIG['title_banner']['SHADING_QUALITY']
CORNER_QUALITY = _CONFIG['title_banner']['CORNER_QUALITY']
CORNER_RADIUS = _CONFIG['title_banner']['CORNER_RADIUS']


ROWS = {'1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D',
        '5': 'E',
        '6': 'F',
        '7': 'G',
        '8': 'H',
        '9': 'I',
        '10': 'J',
        '11': 'K',
        '12': 'L'
        }

# TITLE_RECT = pygame.Rect(3, 30, 314, 60)
# these probably shouldnt be here
TITLE_RECT = pygame.Rect(0, 25, 320, 70)
SWIPE_HINT_RECT = pygame.Rect(0, 210, 320, 30)


# this is where the icon stuff is kept
ICON_FONT_FILE = 'pifile.ttf'
ICON_FONT_JSON = 'config.json'
ICONS = icon(ICON_FONT_JSON, ICON_FONT_FILE)


# DECLARE THE USER DEFINED EVENTS
TFTBUTTONCLICK = pygame.USEREVENT + 1
UPDATESCREEN = TFTBUTTONCLICK + 1
NEXTSCREEN = UPDATESCREEN + 1
NEWSCREEN = NEXTSCREEN + 1
SLEEPEVENT = NEWSCREEN + 1
RETURN_EVENT = SLEEPEVENT + 1

###################################
# SCREEN BANNER VARIABLES
###################################


COLORS = {
    'RED':         (231, 76,  60),
    'BLUE':        (52,  152, 219),
    'TEAL':        (26,  188, 156),
    'PURPLE':      (155, 89,  182),
    'GREEN':       (46,  204, 113),
    'ORANGE':      (230, 126, 34),
    'YELLOW':      (241, 196, 15),
    'CLOUD':       (236, 240, 241),
    'ASPHALT':     (52,  73,  94),
    'CONCRETE':    (149, 165, 166),
    'TRANSPARENT': (0,   0,   0,   0)
}
LOADING_MESSEGES = [
    "Creating Time-Loop Inversion Field",
    "Loading the Loading message..",
    "Randomizing memory access...",
    "Tube Clamp Error",
    "Priming reagents.",
    "Testing CP functions",
    "Homing",
    "Running Enhanced clean on all probes"
]
