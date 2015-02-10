import sys
import pygame
from configobj import ConfigObj
import os
from pprint import pprint
from parseIcons import icon
from validate import Validator
sys.dont_write_bytecode = True

DEBUG = True

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
if not DEBUG:
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

# 500
COLOR_HEX = {
    'RED': '#ef5350',
    'PINK': '#ef5350',
    'PURPLE': '#AB47BC',
    'DEEP_PURPLE': '#7E57C2',
    'INDIGO': '#5C6BC0',
    'BLUE': '#42A5F5',
    'LIGHT_BLUE': '#29B6F6',
    'CYAN': '#26C6DA',
    'TEAL': '#26A69A',
    'GREEN': '#66BB6A',
    'LIGHT_GREEN': '#9CCC65',
    'LIME': '#D4E157',
    'YELLOW': '#D4E157',
    'AMBER': '#D4E157',
    'ORANGE': '#FFA726',
    'DEEP_ORANGE': '#FF7043',
    'BROWN': '#8D6E63',
    'GRAY': '#263238',
    'BLUE_GRAY': '#546E7A',
    'CLOUD': '#CFD8DC',
    'ASPHALT': '#546E7A',
    'CONCRETE': '#90A4AE',
    'DARK_GRAY': '#263238'
}






# 600
COLOR_HEX_SIX_HUNDRED = {
    'RED': '#f44336',
    'PINK': '#D81B60',
    'PURPLE': '#9C27B0',
    'DEEP_PURPLE': '#5E35B1',
    'INDIGO': '#3949AB',
    'BLUE': '#1E88E5',
    'LIGHT_BLUE': '#039BE5',
    'CYAN': '#00ACC1',
    'TEAL': '#00897B',
    'GREEN': '#43A047',
    'LIGHT_GREEN': '#7CB342',
    'YELLOW': '#FDD835',
    'AMBER': '#FDD835',
    'ORANGE': '#FB8C00',
    'DEEP_ORANGE': '#F4511E',
    'BROWN': '#6D4C41',
    'GRAY': '#6D4C41',
    'BLUE_GRAY': '#546E7A',
    'CLOUD': '#CFD8DC',
    'ASPHALT': '#546E7A',
    'CONCRETE': '#90A4AE'
}

COLORS = {}
for color in COLOR_HEX:
    # print color
    tmp = pygame.color.Color(COLOR_HEX[color])
    COLORS[color] = (tmp[0], tmp[1], tmp[2])
# pprint(COLORS)
for item in COLORS:
    print COLORS[item]


# COLORS = {
#     'RED':         (231, 76,  60),
#     'BLUE':        (52,  152, 219),
#     'TEAL':        (26,  188, 156),
#     'PURPLE':      (155, 89,  182),
#     'GREEN':       (46,  204, 113),
#     'ORANGE':      (230, 126, 34),
#     'YELLOW':      (241, 196, 15),
#     'CLOUD':       (236, 240, 241),
#     'ASPHALT':     (52,  73,  94),
#     'CYAN':        (0,   172, 193),
#     'CONCRETE':    (149, 165, 166),
#     'TRANSPARENT': (0,   0,   0,   0)
# }





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
