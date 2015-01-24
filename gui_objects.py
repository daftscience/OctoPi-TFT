import pygame
import pprint
import sys
from global_variables import COLORS
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

        if self.align =='left':
            self.fontRect.left = self.surface.get_rect().left
            # fontRect.left = bg_rect.left
            # self.image.blit(fontSurface, fontRect)
        elif self.align =='right':
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
                    3,
                    3)
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
