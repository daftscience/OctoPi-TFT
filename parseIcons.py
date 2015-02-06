import simplejson
from pprint import pprint
import os
import unicodedata
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# data = json.load(json_data)
# pprint(data['icons'])
# i = 0


# this class will parse a json file and create a dictionary of icons
# the name is the key, and the value is an integer to be converted to unicode
class icon():

    def __init__(self, json_file, font_name):
        self.font_location = os.path.join('resources/icons/font/', font_name)
        # print self.font_location
        self.json_file = os.path.join('resources/icons/', json_file)
        self.icon = {}
        json_data = open(self.json_file)
        data = simplejson.load(json_data)
        for thing in data['glyphs']:
            self.icon[thing['css']] = thing['code']
        json_data.close()
    def unicode(self, string):
        # try:
            # print string + str(self.icon[string])
            return unichr(self.icon[string])
        # except:
            # return self.icon[string]
if __name__ == "__main__":
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    from global_variables import ICON_FONT_JSON, ICON_FONT_FILE
    # import pygame
    # pygame.init()

    # icon_location = os.path.join("resources/icons/font", ICON_FONT_FILE)
    # self.icons = icon(ICON_FONT_JSON, ICON_FONT_FILE)
    # test = icon(ICON_FONT_JSON, ICON_FONT_FILE)
    # pprint(test.icon)
    # print test.unicode('smile')
