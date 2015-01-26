import pygame
import sys
from global_variables import COLORS, ROWS
sys.dont_write_bytecode = True


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
            # fontRect.left = bg_rect.left
            # self.image.blit(fontSurface, fontRect)
        elif self.align == 'right':
            self.fontRect.right = self.surface.get_rect().right
            # fontRect = fontSurface.get_rect()
            # bg_rect = self.image.get_rect()
            # fontRect.right = bg_rect.right
            # self.image.blit(fontSurface, fontRect)
        else:
            self.fontRect.centerx = self.surface.get_rect().centerx

        if self.valign == 'top':
            self.fontRect.top = self.surface.get_rect().top
        elif self.valign == 'bottom':
            self.fontRect.bottom = self.surface.get_rect().bottom
        else:
            self.fontRect.centery = self.surface.get_rect().centery

        if self.rounded:
            DrawRoundRect(
                self.surface,
                self.background_color,
                pygame.Rect(0, 0, 310, 60),
                0,
                2,
                2)
        else:
            if self.background_color:
                self.surface.fill(self.background_color)
                # self.image = pygame.Surface(self.rect.size)
                # self.image.fill(self.background_color)
                # self.surface.blit(self.image, self.fontRect)
            else:
                self.surface.fill(COLORS['CLOUD'])
        self.surface.blit(self.label, self.fontRect)

    def update(self):
        self.blit_text()


def DrawRoundRect(surface, color, rect, width, xr, yr):
    clip = surface.get_clip()
    # left and right
    surface.set_clip(clip.clip(rect.inflate(0, -yr * 2)))
    pygame.draw.rect(surface, color, rect.inflate(1 - width, 0), width)
    # top and bottom
    surface.set_clip(clip.clip(rect.inflate(-xr * 2, 0)))
    pygame.draw.rect(surface, color, rect.inflate(0, 1 - width), width)
    # top left corner
    surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
    corner = pygame.Rect(rect.left, rect.top, 2 * xr, 2 * yr)
    pygame.draw.ellipse(surface, color, corner, width)
    # top right corner
    surface.set_clip(clip.clip(rect.right - xr, rect.top, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(
        rect.right - 2 * xr, rect.top, 2 * xr, 2 * yr), width)
    # bottom left
    surface.set_clip(clip.clip(rect.left, rect.bottom - yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(
        rect.left, rect.bottom - 2 * yr, 2 * xr, 2 * yr), width)
    # bottom right
    surface.set_clip(clip.clip(rect.right - xr, rect.bottom - yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(
        rect.right - 2 * xr, rect.bottom - 2 * yr, 2 * xr, 2 * yr), width)
    surface.set_clip(clip)
    return clip


def format_location(item):
    row = ROWS[str(item['row'])]
    rack = str(item['rack'])
    column = str(item['column'])
    # day = strftime('%a', localtime(RACK_DB.rack_date))
    day = item['rackDay']
    file_string = day + rack + ': ' + row + '' + column
    return file_string


class render_textrect():

    def __init__(self, string, font, rect, text_color,
                 background_color, justification=0, vjustification=0,
                 margin=0, shrink=False, SysFont=None, FontPath=None,
                 MaxFont=50, MinFont=5):
        self.string = string
        self.font = font
        self.rect = rect
        self.text_color = text_color
        self.background_color = background_color
        self.justification = justification
        self.vjustification = vjustification
        self.margin = margin
        # self.cutoff = cutoff
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
        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > (
                    self.rect.width - (self.margin[0] + self.margin[1])):
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                # for word in words:
                #     if font.size(word)[0] >= (rect.width - (margin * 2)):
                #         raise TextRectException, "The word " + word + "
                # is too long to fit in the rect passed."

                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if self.font.size(test_line.strip())[0] < (
                            self.rect.width - (self.margin[0] + self.margin[1])):
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

        self.accumulated_height = 0
        for line in final_lines:
            if self.accumulated_height + \
                    self.font.size(line)[1] >= (self.rect.height - self.margin[2] - self.margin[3]):
                if not self.cutoff:
                    raise self.TextRectException(
                        "Once word-wrapped, the text string was too tall to fit in the rect.")
                else:
                    break
            if line != "":
                tempsurface = self.font.render(
                    line.strip(),
                    1,
                    self.text_color)
                if self.justification == 0:
                    surface.blit(
                        tempsurface,
                        (0 +
                         self.margin[0],
                         self.accumulated_height +
                         self.margin[2]))
                elif self.justification == 1:
                    surface.blit(
                        tempsurface,
                        ((self.rect.width - tempsurface.get_width()) / 2,
                         self.accumulated_height + self.margin[2]))
                elif self.justification == 2:
                    surface.blit(
                        tempsurface,
                        (self.rect.width -
                         tempsurface.get_width() -
                         self.margin[1],
                         self.accumulated_height +
                         self.margin[2]))
                else:
                    raise self.TextRectException(
                        "Invalid justification argument: " +
                        str(self.justification))
            self.accumulated_height += self.font.size(line)[1]

        if self.vjustification == 0:
            # Top aligned, we're ok
            pass
        elif self.vjustification == 1:
            # Middle aligned
            tempsurface = pygame.Surface(self.rect.size)
            tempsurface.fill(self.background_color)
            vpos = (0, (self.rect.size[1] - self.accumulated_height) / 2)
            tempsurface.blit(
                surface,
                vpos,
                (0,
                 0,
                 self.rect.size[0],
                    self.accumulated_height))
            surface = tempsurface
        elif self.vjustification == 2:
            # Bottom aligned
            tempsurface = pygame.Surface(self.rect.size)
            tempsurface.fill(self.background_color)
            vpos = (
                0,
                (self.rect.size[1] -
                 self.accumulated_height -
                 self.margin[3]))
            tempsurface.blit(
                surface,
                vpos,
                (0,
                 0,
                 self.rect.size[0],
                    self.accumulated_height))
            surface = tempsurface
        else:
            raise self.TextRectException(
                "Invalid vjustification argument: " + str(self.justification))
        return surface
        surface = None

        if not self.shrink:
            surface = self.draw_text_rect(
                self.string,
                self.font,
                self.rect,
                self, text_color,
                self.background_color,
                justification=self.justification,
                vjustification=self.vjustification,
                margin=self.margin,
                cutoff=False)

        else:
            self.fontsize = self.MaxFont
            fit = False
            while self.fontsize >= self.MinFont:
                if self.FontPath is None:
                    myfont = pygame.font.SysFont(self.SysFont, self.fontsize)
                else:
                    myfont = pygame.font.Font(self.FontPath, self.fontsize)
                try:
                    surface = self.draw_text_rect(
                        self.string,
                        self.myfont,
                        self.rect,
                        self.text_color,
                        self.background_color,
                        justification=self.justification,
                        vjustification=self.vjustification,
                        margin=self.margin,
                        cutoff=False)
                    fit = True
                    print("Fit Font: " + str(self.fontsize))
                    break
                except:
                    self.fontsize -= 1
            if not fit:
                surface = draw_text_rect(
                    self.string,
                    self.myfont,
                    self.rect,
                    self.text_color,
                    self.background_color,
                    justification=self.justification,
                    vjustification=self.vjustification,
                    margin=self.margin)

        return surface
