import pygame
from pprint import pprint
from global_variables import ICONS
import time


class multi_font():

    def __init__(self, surface, items, background_color = (255,255,255, 0)):
        self.items = items
        self.images = []
        self.background_color = background_color
        self.dirty = True
        self.surface = surface
        self.surface.convert_alpha()
        self.surface_rect = self.surface.get_rect()
        self.update()

    def update(self):
        if self.dirty:
            self.create_image()
            self.dirty = False
        self.rect.centerx = self.surface_rect.centerx
        self.rect.centery = self.surface_rect.centery
    	self.surface.fill(self.background_color)
        self.surface.blit(self.combine_images, self.rect)

    def create_image(self):
    	self.images = []
    	# self.combine_images.fill(self.background_color)
        for item in self.items:
            font_location = item['font_location']
            font = pygame.font.Font(font_location, item['size'])
            image = font.render(item['text'], 1, item['color'])
            image.convert_alpha()
            self.images.append(image)

        max_height = 0
        total_width = 0
        for item in self.images:
            item_width, item_height = item.get_size()
            print item_height
            if max_height < item_height:
                max_height = item_height
            total_width += item_width

        self.rect = pygame.Rect(0, 0, total_width, max_height)
        self.combine_images = pygame.Surface((total_width, max_height))
        self.combine_images.fill(self.background_color)
        self.combine_images.convert_alpha()
        # THIS WILL BLIT ALL OF THE IMAGES INTO ONE
        # LARGER IMAGE SIDE BY SIDE
        x = 0
        for image in self.images:
            rect = image.get_rect()
            rect.centery = item_height/2
            rect.left = x
            # self.combine_images.fill((50,50,50))
            self.combine_images.blit(image, rect)
            x += rect.width


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill((255, 255, 255, 0))
    rect = (0, 0, 300, 100)
    subsurface = screen.subsurface(rect)

    items = []
    # font = pygame.font.Font(ICONS.font_location, 20)
    font = ICONS.font_location
    i = 40
    while i < 55:
        item = {
            'font_location': font,
            'text': ICONS.unicode('smile'),
            'size': i,
            'color': (128, 128, 128)
        }
        items.append(item)
        i += 1
    test = multi_font(subsurface, items)
    pygame.display.update()
    time.sleep(2)
