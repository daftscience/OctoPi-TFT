import pygame
import sys
import os
import parseIcons
from PIL import Image, ImageFilter
from time import strftime, localtime
from PIL import ImageDraw, ImageFont
from global_variables import COLORS, ROWS, ICON_FONT_FILE
from global_variables import ICON_FONT_JSON, CORNER_QUALITY

sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class text_label(pygame.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.surface = kwargs['surface']
        self.font = kwargs['font']
        self.text = kwargs['text']
        self.color = kwargs['color']
        if 'valign' in kwargs:
            self.valign = kwargs['valign']
        else:
            self.valign = 'center'

        if 'rounded' in kwargs:
            self.rounded = kwargs['rounded']
        else:
            self.rounded = False

        if 'align' in kwargs:
            self.align = kwargs['align']
        else:
            self.align = 'center'

        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        else:
            self.background_color = None
        if 'rect' in kwargs:
            self.rect = kwargs['rect']
            # self.rect.size
        else:
            self.rect = None

    def blit_text(self):

        self.label = self.font.render(self.text, 1, self.color)
        # get the size of the text object
        self.fontRect = self.label.get_rect()
        # create the text object

        if self.align == 'left':
            self.fontRect.left = self.surface.get_rect().left
        elif self.align == 'right':
            self.fontRect.right = self.surface.get_rect().right
        else:
            self.fontRect.centerx = self.surface.get_rect().centerx

        if self.valign == 'top':
            self.fontRect.top = self.surface.get_rect().top
        elif self.valign == 'bottom':
            self.fontRect.bottom = self.surface.get_rect().bottom
        else:
            self.fontRect.centery = self.surface.get_rect().centery

    def update(self):
        self.blit_text()
        self.surface.fill(self.background_color)
        self.surface.blit(self.label, self.fontRect)


class title_banner(text_label):

    def __init__(self, *args, **kwargs):
        self.title_icon = kwargs['title_icon']
        super(title_banner, self).__init__(*args, **kwargs)
        self.icons = parseIcons.icon(ICON_FONT_JSON, ICON_FONT_FILE)
        # print "initialized title_text class"
        self.surface.get_size()
        self.blit_text()

        try:
            self.pygameImage = pygame.image.load(kwargs['banner_location'])
        except:
            self.banner = rounded_rect(
                (self.surface.get_size()),
                radius=2,
                fill=self.background_color,
                quality=CORNER_QUALITY,
                shadow=False)

            self.rect = self.surface.get_rect()
            self.add_text()

            self.pygameImage = pygame.image.fromstring(
                self.banner.image.tostring(),
                self.banner.image.size,
                'RGBA',
                False).convert_alpha()
            pygame.image.save(self.pygameImage, kwargs['banner_location'])

        self.blit_text()

    def add_text(self):
        print self.title_icon
        icon_unicode = self.icons.unicode(self.title_icon)
        self.fa = ImageFont.truetype(self.icons.font_location, 40)
        text = ImageDraw.Draw(self.banner.image)
        image_width, image_height = text.textsize(icon_unicode, font=self.fa)
        surface_width, surface_height = self.surface.get_size()
        text.text(
            (35,
             (surface_height - image_height) / 2),
            icon_unicode,
            font=self.fa)
        # self.banner.image.show()

    def update(self):
        self.surface.blit(self.pygameImage, (0, 0))
        # self.image_rect = self.image.get_rect()

        # self.image_rect.left = 25
        self.surface.blit(self.label, self.fontRect)
        # self.image_rect.centery = self.fontRect.centery
        # self.surface.blit(self.image, self.image_rect)


def format_location(item):
    row = ROWS[str(item['row'])]
    rack = str(item['rack'])
    column = str(item['column'])
    # day = strftime('%a', localtime(RACK_DB.rack_date))
    day = item['rackDay']
    file_string = day + '-' + rack + ': ' + row + '' + column
    # if time is sent with the list then we will send that too
    try:
        time = strftime("%H:%M %b %d", localtime(item['time']))
        file_string += " @ " + time
    except:
        pass
    return file_string


class render_textrect():

    def __init__(self, string, font, rect, text_color,
                 background_color, justification=0, vjustification=0,
                 margin=0, shrink=False, SysFont=None, FontPath=None,
                 MaxFont=50, MinFont=5, cutoff=True, surface=None):
        self.string = string
        self.font = font
        self.rect = rect
        self.text_color = text_color
        self.background_color = background_color
        self.justification = justification
        self.vjustification = vjustification
        self.margin = margin
        self.cutoff = cutoff
        self.shrink = shrink
        self.SysFont = SysFont
        self.FontPath = FontPath
        self.MaxFont = MaxFont
        self.MinFont = MinFont

        if isinstance(self.margin, tuple):
            if not len(self.margin) == 4:
                try:
                    self.margin = (int(self.margin),
                                   int(self.margin),
                                   int(self.margin),
                                   int(self.margin))
                except:
                    self.margin = (0, 0, 0, 0)
        elif isinstance(self.margin, int):
            self.margin = (self.margin, self.margin, self.margin, self.margin)
        else:
            self.margin = (0, 0, 0, 0)

    def update(self):
        self.fontsize = self.MaxFont
        if not self.shrink:
            # print "not shrunk"
            surface = self.draw_text_rect()
        else:
            fit = False
            while self.fontsize >= self.MinFont:
                if self.FontPath is None:
                    self.font = pygame.font.SysFont(
                        self.SysFont,
                        self.fontsize)
                else:
                    # print "found font"
                    self.font = pygame.font.Font(self.FontPath, self.fontsize)
                try:
                    surface = self.draw_text_rect()
                    fit = True
                    break
                except self.TextRectException:
                    self.fontsize -= 1
                    # print "trying new font" + str(self.fontsize)
            if not fit:
                self.cutoff = True
                # print "shrunk to font: " + str(self.fontsize)
                self.font = pygame.font.Font(self.FontPath, self.fontsize)
                surface = self.draw_text_rect()
        return self.draw_text_rect()

    class TextRectException(Exception):

        def __init__(self, message=None):
            self.message = message

        def __str__(self):
            return self.message

    def draw_text_rect(self):
        final_lines = []
        requested_lines = self.string.splitlines()
        # Create a series of lines that will fit on the provided
        # rectangle.
        # Let's try to write the text out on the surface.

        surface = pygame.Surface(self.rect.size)
        surface.fill(self.background_color)

        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > self.rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if self.font.size(word)[0] >= self.rect.width:
                        raise TextRectException(
                            "The word " +
                            word +
                            " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if self.font.size(test_line)[0] < self.rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(self.rect.size)
        surface.fill(self.background_color)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + \
                    self.font.size(line)[1] >= self.rect.height:
                raise self.TextRectException(
                    "Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = self.font.render(line, 1, self.text_color)
                if self.justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif self.justification == 1:
                    surface.blit(
                        tempsurface,
                        ((self.rect.width - tempsurface.get_width()) / 2,
                         accumulated_height))
                elif self.justification == 2:
                    surface.blit(
                        tempsurface,
                        (self.rect.width -
                         tempsurface.get_width(),
                         accumulated_height))
                else:
                    raise TextRectException(
                        "Invalid justification argument: " + str(self.justification))
            accumulated_height += self.font.size(line)[1]

        if self.vjustification == 0:
            # Top aligned, we're ok
            pass
        elif self.vjustification == 1:
            # Middle aligned
            tempsurface = pygame.Surface(self.rect.size)
            tempsurface.fill(self.background_color)
            vpos = (0, (self.rect.size[1] - accumulated_height) / 2)
            tempsurface.blit(
                surface, vpos, (0, 0, self.rect.size[0], accumulated_height))
            surface = tempsurface
        elif self.vjustification == 2:
            # Bottom aligned
            tempsurface = pygame.Surface(self.rect.size)
            tempsurface.fill(self.background_color)
            vpos = (
                0,
                (self.rect.size[1] -
                 accumulated_height -
                 self.margin[3]))
            tempsurface.blit(
                surface, vpos, (0, 0, self.rect.size[0], accumulated_height))
            surface = tempsurface
        else:
            raise self.TextRectException(
                "Invalid vjustification argument: " +
                str(justification))
        return surface
    surface = None


class rounded_rect():

    def __init__(self, og_size, radius, fill, quality, shadow=False):
        self.quality = quality
        self.og_size = og_size
        self.radius = radius * self.quality
        self.fill = fill
        # to get better quality corners we will scale the
        # image up then shink it back down
        self.size = (
            self.og_size[0] *
            self.quality,
            self.og_size[1] *
            self.quality)
        self.width, self.height = self.size
        if shadow:
            self.image = self.round_rectangle()
        else:
            self.image = self.makeShadow(
                self.round_rectangle(),
                10,
                30,
                (0,
                 2),
                COLORS['CLOUD'],
                0x000000)
        self.image = self.image.resize(self.og_size, resample=Image.LANCZOS)

    def round_corner(self):
        """Draw a round corner"""
        corner = Image.new('RGBA', (self.radius, self.radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice(
            (0,
             0,
             self.radius *
             2,
             self.radius *
             2),
            180,
            270,
            fill=self.fill)
        corner.convert('RGBA')
        return corner

    def round_rectangle(self):
        """Draw a rounded rectangle"""

        rectangle = Image.new('RGBA', self.size)
        # ImageDraw.Draw.rectangle(size, (0,0,0,0))

        origCorner = self.round_corner()
        corner = origCorner
        rectangle.paste(corner, (0, 0))
        corner = origCorner.rotate(90)
        rectangle.paste(corner, (0, self.height - self.radius))
        corner = origCorner.rotate(180)
        rectangle.paste(
            corner,
            (self.width -
             self.radius,
             self.height -
             self.radius))
        corner = origCorner.rotate(270)
        rectangle.paste(corner, (self.width - self.radius, 0))

        dr = ImageDraw.Draw(rectangle)
        dl = ImageDraw.Draw(rectangle)
        dr.rectangle(
            ((self.width - self.radius, 0), ((self.radius), (self.height))), fill=self.fill)
        dl.rectangle(
            ((0, self.radius), ((self.width), (self.height - self.radius))), fill=self.fill)
        return rectangle

    def makeShadow(self,
                   image,
                   iterations,
                   border,
                   offset,
                   backgroundColour,
                   shadowColour):
    # image: base image to give a drop shadow
    # iterations: number of times to apply the blur filter to the shadow
    # border: border to give the image to leave space for the shadow
    # offset: offset of the shadow as [x,y]
    # backgroundCOlour: colour of the background
    # shadowColour: colour of the drop shadow

    # Calculate the size of the shadow's image
        fullWidth = image.size[0] + abs(offset[0]) + 2 * border
        fullHeight = image.size[1] + abs(offset[1]) + 2 * border

    # Create the shadow's image. Match the parent image's mode.
        shadow = Image.new(
            image.mode,
            (fullWidth,
             fullHeight),
            backgroundColour)
    # Place the shadow, with the required offset
    # if <0, push the rest of the image right
        shadowLeft = border + max(offset[0], 0)
    # if <0, push the rest of the image down
        shadowTop = border + max(offset[1], 0)
    # Paste in the constant colour
        shadow.paste(shadowColour,
                     [shadowLeft, shadowTop,
                      shadowLeft + image.size[0],
                      shadowTop + image.size[1]])
        # i=2
    # Apply the BLUR filter repeatedly
        for i in range(iterations):
            shadow = shadow.filter(ImageFilter.BLUR)
        # shadow.show()

    # Paste the original image on top of the shadow
    # if the shadow offset was <0, push right
        imgLeft = border - min(offset[0], 0)
    # if the shadow offset was <0, push down
        imgTop = border - min(offset[1], 0)
        shadow.paste(image, (imgLeft, imgTop))
        # shadow.show()
        return shadow

if __name__ == "__main__":
    from global_variables import COLORS
    img = rounded_rect((310, 60), 10, COLORS['PURPLE'], 10, shadow=True)
    print img.image.size
    # img.image.show()
    print img.image.mode
    # print newIMG.verify()
    # img.image.save('zzz.png')
