import pygame
import pprint
import sys
sys.dont_write_bytecode = True


class text_label(pygame.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.surface = kwargs['surface']
        self.font = kwargs['font']
        self.text = kwargs['text']
        self.color = kwargs['color']
        self.background_color = kwargs['background_color']
        if 'rect' in kwargs:
            self.rect = kwargs['rect']
            # self.rect.size
        else:
            self.rect = None

    def blit_text(self):

        # create the text object
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.background_color)
        self.label = self.font.render(self.text, 1, self.color)

        # get the size of the text object
        self.fontRect = self.label.get_rect()

        # set the center of the text object to be the center of
        # the subscreen were placing it on
        self.fontRect.centerx = self.surface.get_rect().centerx
        self.fontRect.centery = self.surface.get_rect().centery

        # blit it
        self.surface.blit(self.label, self.fontRect)

    def update(self):
        self.blit_text()


# http://www.pygame.org/wiki/ShadowEffects?parent=CookBook
<<<<<<< HEAD

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
=======

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

>>>>>>> origin/master
    # bottom right
    surface.set_clip(clip.clip(rect.right - xr, rect.bottom - yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(
        rect.right - 2 * xr, rect.bottom - 2 * yr, 2 * xr, 2 * yr), width)
<<<<<<< HEAD
=======

>>>>>>> origin/master
    surface.set_clip(clip)
    return clip
