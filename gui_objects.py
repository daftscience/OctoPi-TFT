import pygame
import sys
from pprint import pprint
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
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.background_color)
        self.label = self.font.render(self.text, 1, self.color)
        self.fontRect = self.label.get_rect()
        # if self.align =='left':
            # fontRect = fontSurface.get_rect()
            # bg_rect = self.image.get_rect()
            # fontRect.left = bg_rect.left
            # self.image.blit(fontSurface, fontRect)
        # elif self.align =='right':
            # fontRect = fontSurface.get_rect()
            # bg_rect = self.image.get_rect()
            # fontRect.right = bg_rect.right
            # self.image.blit(fontSurface, fontRect)

        xPos = (self.rect.width - self.label.get_width())/2
        yPos = (self.rect.height - self.label.get_height())/2

        self.image.blit(self.label, (xPos, yPos))
        self.surface.blit(self.image, self.rect)


    def update(self):
        self.blit_text()




