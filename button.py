

import pygame
import os
from global_variables import FONTS


class button:

    def __init__(self, text='', width=100, height=10, command=None, **kwargs):

        self.assign_kwargs(kwargs)
        self.label, self.label_rect = self.render_font(
            text, self.font, self.fontsize)
        self.color = self.bg_color
        self.callback = command

        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.label_rect.center = self.rect.center
        self.is_hover = False

    def assign_kwargs(self, kwargs):
        self.hover_bg_color = kwargs['hover']
        self.bg_color = kwargs['bg']
        self.text_color = kwargs['fg']
        self.font = kwargs['font']
        self.border = kwargs['border']
        self.fontsize = kwargs['fontsize']
        self.screen = kwargs['surface']
        self.clear_color = kwargs['clear_color']

    def render_font(self, text, filename, size):
        # if not filename:
            # f = pygame.font.SysFont('Arial', size)
        # else:
        f = pygame.font.Font(filename, size)
            # f = Font.load(self.font, size)
        font = f.render(text, 1, self.text_color)
        rect = font.get_rect()
        return (font, rect)

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.border)
        self.screen.blit(self.label, self.label_rect)
        # return screen
    def clear(self):
        pygame.draw.rect(self.screen, self.clear_color, self.rect, self.border)
        # self.screen.blit()

    def mouse_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.is_hover = True
        else:
            self.is_hover = False

        if self.is_hover:
            self.color = self.hover_bg_color
        else:
            self.color = self.bg_color

    def update(self):
        self.label_rect.center = self.rect.center
        self.mouse_collision()
        self.render()

    def get_event(self, event):
        # print("Start button event")
        self.mouse_collision()
        if self.is_hover:
            if event.type == pygame.MOUSEBUTTONUP:
                self.callback()
                pygame.mouse.set_pos(0, 0)
                return True
        # print("end button event")
        return False

if __name__ == "__main__":
    # class Font:
        # '''simulating tools'''
        # path = 'resources/fonts'
        # @staticmethod
        # def load(filename, size):
            # p = os.path.join(Font.path, filename+'.ttf')
            # return pygame.font.Font(os.path.abspath(p), size)
            # from global_variables import FONTS
    def callback():
        print('running callback')

    def callback2():
        print('running callback 2')

    class Control:

        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.screen_rect = self.screen.get_rect()
            self.Clock = pygame.time.Clock()
            self.done = False

            self.button_settings = {
                'hover': (255, 255, 255),
                'font': FONTS['swipe_font']['path'],
                'fg': (0, 0, 0),
                'bg': (155, 155, 155),
                'border': False,
                'fontsize': 15
            }

            self.btn = button(text='Button1', width=100, height=20,
                              command=callback, **self.button_settings)
            self.btn.rect.center = (200, 100)
            self.btn2 = button(text='Button2', width=100, height=20,
                               command=callback2, **self.button_settings)
            self.btn2.rect.center = (200, 150)
            self.quit_btn = button(
                text='Exit',
                width=100,
                height=20,
                command=self.terminate,
                **self.button_settings)
            self.quit_btn.rect.center = (200, 200)
            self.buttons = [self.btn, self.btn2, self.quit_btn]

        def event_loop(self):
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    self.done = True
                for b in self.buttons:
                    b.get_event(event)

        def run(self):
            while not self.done:
                self.screen.fill(0)
                self.event_loop()
                for b in self.buttons:
                    b.update()
                    b.render(self.screen)
                pygame.display.update()
                self.Clock.tick(60)

        def terminate(self):
            self.done = True

    app = Control()
    app.run()
    pygame.quit()
