import simplejson
import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------------------------------------------
# Icon class:
# inputs a ttf icon file to
# -----------------------------------------------------------------------------


class icon():

    def __init__(self, json_file, font_name):
        # GET THE LOCATION OF THE JSON FILE
        self.json_file = os.path.join('resources/icons/', json_file)

        # LOAD THE JSON FILE
        json_data = open(self.json_file)
        data = simplejson.load(json_data)

        # CREATE A DICTIONARY FROM THE JSON FILE
        self.icon = {}
        for thing in data['glyphs']:
            self.icon[thing['css']] = thing['code']
        json_data.close()

    def unicode(self, string):
        # RETURN THE VALUE MATCHING STRING FROM THE DICTIONARY
        return unichr(self.icon[string])


if __name__ == "__main__":
    pass
