"""

    (C) Copyright 2007 Anthony Maro
    (C) Copyright 2014 William B Phelps

   Version 2.1 - March 2014 - for PiTFT 320x240 touchscreen
   Version 2.2 - March 2014 - generalized for "any" touchscreen

   Now has 2 line input area (code specific for 2 lines)
       
   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation; either version 2 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
   02111-1307, USA.

   Usage:
   
   from virtualKeyboard import VirtualKeyboard
   
   vkeybd = VirtualKeyboard(screen)
   userinput = vkeybd.run(default_text)
   
   screen is a full screen pygame screen.  The VirtualKeyboard will shade out the current screen and overlay
   a transparent keyboard.  default_text gets fed to the initial text import - used for editing text fields
   If the user clicks the escape hardware button, the default_text is returned
   
"""

import pygame
import time
from global_variables import COLORS
from pygame.locals import *

from string import maketrans
Uppercase = maketrans("1234567890",
                      'SMTWHF-X--')

# _keyWidth = 27 # default key width including borders
# _keyHeight = 29 # default key height

# ----------------------------------------------------------------------------


class VirtualKeyboard():

    ''' Implement a basic full screen virtual keyboard for touchscreens '''

    def __init__(self, screen):

        self.screen = screen
        self.rect = self.screen.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height

        # create a background surface
        self.background = pygame.Surface(self.rect.size)
        self.screen.fill(COLORS['CLOUD'])

        self.keyW = int(self.w / 4)  # key width with border
        self.keyH = int(self.h / 5)  # key height

        self.x = (self.w - self.keyW * 4) / 2  # centered
        self.y = 0  # stay away from the edges (better touch)

        pygame.font.init()  # Just in case
        self.keyFont = pygame.font.Font(None, self.keyW)  # keyboard font

        # set dimensions for text input box
        self.textW = self.keyW * 3  # + 4  # leave room for escape key
        self.textH = self.keyH * 1

        self.caps = False
        self.keys = []
#        self.textbox = pygame.Surface((self.rect.width,self.keyH*2))
        self.addkeys()  # add all the keys
        self.paintkeys()  # paint all the keys

        pygame.display.update()

    def run(self, text=''):
        # self.screen.blit(self.screenCopy, (0, 0))

        self.text = text
        # create an input text box
        # create a text input box with room for 2 lines of text. leave room for
        # the escape key
        self.input = TextInput(
            self.screen,
            self.text,
            self.x,
            self.y,
            self.textW,
            self.textH)

        counter = 0
        # main event loop (hog all processes since we're on top, but someone might want
        # to rewrite this to be more event based...
        while True:
            time.sleep(0.1)  # 10/second is often enough
            events = pygame.event.get()
            if events is not None:
                for e in events:
                    if (e.type == MOUSEBUTTONDOWN):
                        self.selectatmouse()
                    if (e.type == MOUSEBUTTONUP):
                        if self.clickatmouse():
                            # user clicked enter or escape if returns True
                            self.clear()
                            # Return what the user entered
                            return self.input.text
                    if (e.type == MOUSEMOTION):
                        if e.buttons[0] == 1:
                            # user click-dragged to a different key?
                            self.selectatmouse()

            counter += 1
            if counter > 5:
                self.input.flashcursor()
                counter = 0

    def unselectall(self, force=False):
        ''' Force all the keys to be unselected
            Marks any that change as dirty to redraw '''
        for key in self.keys:
            if key.selected:
                key.selected = False
                key.dirty = True

    def clickatmouse(self):
        # ''' Check to see if the user is pressing down on a key and draw it selected '''
        # self.screen.blit(self.screenCopy, (0,0))
        self.unselectall()
        for key in self.keys:
            keyrect = Rect(key.x, key.y, key.w, key.h)
            if keyrect.collidepoint(pygame.mouse.get_pos()):
                key.dirty = True
                if key.bskey:
                    # Backspace
                    self.input.backspace()
                    self.paintkeys()
                    return False
                if key.fskey:
                    self.input.inccursor()
                    self.paintkeys()
                    return False
                if key.spacekey:
                    self.input.addcharatcursor(' ')
                    self.paintkeys()
                    return False
                if key.shiftkey:
                    self.togglecaps()
                    self.paintkeys()
                    return False
                if key.escape:
                    self.input.text = ''  # clear input
                    return True
                if key.enter:
                    return True
                if self.caps:
                    keycap = key.caption.translate(Uppercase)
                else:
                    keycap = key.caption
                self.input.addcharatcursor(keycap)
                self.paintkeys()
                return False

        self.paintkeys()
        return False

    def togglecaps(self):
        ''' Toggle uppercase / lowercase '''
        if self.caps:
            self.caps = False
        else:
            self.caps = True
        for key in self.keys:
            key.dirty = True

    def selectatmouse(self):
        # User has touched the screen - is it inside the textbox, or inside a
        # key rect?
        self.unselectall()
        pos = pygame.mouse.get_pos()
        # print 'touch {}'.format(pos)
        if self.input.rect.collidepoint(pos):
            # print 'input {}'.format(pos)
            self.input.setcursor(pos)
        else:
            for key in self.keys:
                keyrect = Rect(key.x, key.y, key.w, key.h)
                if keyrect.collidepoint(pos):
                    key.selected = True
                    key.dirty = True
                    self.paintkeys()
                    return

        self.paintkeys()

    def addkeys(self):  # Add all the keys for the virtual keyboard

        x = self.x+1
        y = self.y + self.textH  # + self.keyH / 4

        # y = self.keyH  # overlap border
        # x += self.x + self.keyW

        row = ['1', '2', '3']
        for item in row:
            onekey = VKey(
                item,
                x,
                y,
                self.keyW,
                self.keyH,
                self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        onekey = VKey('<-',
                      x,
                      y,
                      self.keyW,
                      self.keyH,
                      self.keyFont)
        onekey.special = True
        onekey.bskey = True
        self.keys.append(onekey)
        x += onekey.w + self.keyW / 3

        y += self.keyH  # overlap border
        x = self.x+1

        row = ['4', '5', '6']
        for item in row:
            onekey = VKey(
                item,
                x,
                y,
                self.keyW,
                self.keyH,
                self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        x += self.x

        onekey = VKey(
            'a',
            x,
            y,
            self.keyW,
            self.keyH,
            self.keyFont)
        onekey.special = True
        onekey.shiftkey = True
        self.keys.append(onekey)

        y += self.keyH
        x = self.x+1

        row = ['7', '8', '9']
        for item in row:
            onekey = VKey(
                item,
                x,
                y,
                self.keyW,
                self.keyH,
                self.keyFont)
            self.keys.append(onekey)
            x += self.keyW

        onekey = VKey(
            'En',
            x,
            y,
            self.keyW,
            self.keyH * 2,
            self.keyFont)
        onekey.special = True
        onekey.enter = True
        self.keys.append(onekey)
        # x += onekey.w

        y += self.keyH
        x = self.x+1

        onekey = VKey('0',
                      x,
                      y,
                      int(self.keyW * 3),
                      self.keyH,
                      self.keyFont)
        self.keys.append(onekey)
        x += self.keyW * 3

        # xfont = pygame.font.SysFont(
        #     'Courier',
        #     22,
        #     bold=True)  # I like this X better #TODO???
        onekey = VKey(
            'X',
            self.x +
            self.textW+1,
            self.y,
            self.keyW,
            self.keyH,self.keyFont)  # exit key TODO???
        onekey.special = True
        onekey.escape = True
        self.keys.append(onekey)
        self.all_keys = pygame.sprite.Group()
        self.all_keys.add(self.all_keys, self.keys)
        # for key in self.keys:
            # all_keys.add(key)


    def paintkeys(self):
        ''' Draw the keyboard (but only if they're dirty.) '''

        for key in self.keys:
            # pass
            key.update(self.caps)
            # key.draw(self.screen, self.background, self.caps)
        self.all_keys.draw(self.screen)
        pygame.display.update()

    def clear(self):
        ''' Put the screen back to before we started '''
        # self.screen.blit(self.background, (0, 0))
        # pygame.display.get_surface().flip()
        pygame.display.update()

# ----------------------------------------------------------------------------


class TextInput():

    ''' Handles the text input box and manages the cursor '''

    def __init__(self, screen, text, x, y, w, h):
        self.screen = screen
        self.text = text
        self.cursorpos = len(text)
        self.x = x
        self.y = y
        self.w = w-3
        self.h = h -2
        self.rect = Rect(x+1, y, w, h)
        self.layer = pygame.Surface((self.w, self.h))
        self.background = pygame.Surface((self.w, self.h))
        self.surface = screen.subsurface(self.rect)
        self.max_length = 10

        self.background_color = COLORS['ORANGE']
        self.font_color = COLORS['CLOUD']
        self.cursor_color = COLORS['CLOUD']

        # self.font = pygame.font.Font(None, fontsize) # use this if you want more
        # text in the line
        rect = screen.get_rect()
        fsize = int(
            rect.height /
            8 +
            0.5)  # font size proportional to screen height
        self.txtFont = pygame.font.SysFont('Courier New', fsize, bold=True)


        # attempt to figure out how many chars will fit on a line
        # this does not work with proportional fonts
        tX = self.txtFont.render("XXXXXXXXXX", 1, (255, 255, 0))  # 10 chars
        rtX = tX.get_rect()  # how big is it?
        
        # chars per line (horizontal)
        self.lineChars = int(self.w / (rtX.width / 10)) - 1
        self.lineH = rtX.height  # pixels per line (vertical)
        
        # print 'txtinp: width={} rtX={} font={} lineChars={}
        # lineH={}'.format(self.w,rtX,fsize, self.lineChars,self.lineH)
        self.cursorlayer = pygame.Surface((2, 29))  # thin vertical line
        self.cursorlayer.fill(self.cursor_color)  # white vertical line
        self.cursorvis = True

        self.cursorX = len(text) % self.lineChars
        self.cursorY = int(len(text) / self.lineChars)  # line 1

        self.draw()

    def draw(self):
        ''' Draw the text input box '''
        self.layer.fill(self.background_color)  # clear the layer

        txt1 = self.text[:self.lineChars]  # line 1
        t1 = self.txtFont.render(txt1, 1, self.font_color)  # line 1
        self.layer.blit(t1, (4, 4))

        self.surface.blit(self.layer, self.rect)
        self.drawcursor()

        pygame.display.update()

    def flashcursor(self):
        ''' Toggle visibility of the cursor '''
        if self.cursorvis:
            self.cursorvis = False
        else:
            self.cursorvis = True
        # self.background.set_alpha(10)
        # self.screen.blit(self.screenCopy, self.rect)
        # self.surface.blit(self.screenCopy, self.rect)
        self.surface.blit(self.layer, self.rect)

        if self.cursorvis:
            self.drawcursor()
        pygame.display.update()

    def addcharatcursor(self, letter):
        ''' Add a character whereever the cursor is currently located '''
        if self.cursorpos < len(self.text) and len(self.text) > self.max_length:
            # Inserting in the middle
            self.text = self.text[:self.cursorpos] + \
                letter + self.text[self.cursorpos:]
            self.cursorpos += 1
            self.draw()
            return
        if len(self.text) < self.max_length:
            self.text += letter
            self.cursorpos += 1
        self.draw()

    def backspace(self):
        ''' Delete a character before the cursor position '''
        if self.cursorpos == 0:
            return
        self.text = self.text[:self.cursorpos - 1] + self.text[self.cursorpos:]
        self.cursorpos -= 1
        self.draw()
        return

    def deccursor(self):
        ''' Move the cursor one space left '''
        if self.cursorpos == 0:
            return
        self.cursorpos -= 1
        self.draw()

    def inccursor(self):
        ''' Move the cursor one space right (but not beyond the end of the text) '''
        if self.cursorpos == len(self.text):
            return
        self.cursorpos += 1
        self.draw()

    def drawcursor(self):
        ''' Draw the cursor '''
        line = int(self.cursorpos / self.lineChars)  # line number
        if line > 1:
            line = 1
        x = 4
        y = 4 + self.y + line * self.lineH
        print y
        # Calc width of text to this point
        if self.cursorpos > 0:
            linetext = self.text[line * self.lineChars:self.cursorpos]
            rtext = self.txtFont.render(linetext, 1, self.font_color)
            textpos = rtext.get_rect()
            x = x + textpos.width + 1

        # self.subsurface.blit(self.screenCopy, (x, y))
        self.surface.blit(self.cursorlayer, (x, y))

    def setcursor(self, pos):  # move cursor to char nearest position (x,y)
        line = int((pos[1] - self.y) / self.lineH)  # vertical
        if line > 1:
            line = 1  # only 2 lines
        x = pos[0] - self.x + line * self.w  # virtual x position
        p = 0
        l = len(self.text)
        #        print 'setcursor {} x={},y={}'.format(pos,x,y)
        #        print 'text {}'.format(self.text)
        while p < l:
            text = self.txtFont.render(
                self.text[
                    :p + 1], 1, (255, 255, 255))  # how many pixels to next char?
            rtext = text.get_rect()
            textX = rtext.x + rtext.width
            #            print 't = {}, tx = {}'.format(t,textX)
            if textX >= x:
                break  # we found it
            p += 1
        self.cursorpos = p
        self.draw()

# ----------------------------------------------------------------------------


class VKey(pygame.sprite.Sprite):

    ''' A single key for the VirtualKeyboard '''
#    def __init__(self, caption, x, y, w=67, h=67):

    def __init__(self, caption, x, y, w, h, font):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        self.w = w + 1  # overlap borders
        self.h = h + 1  # overlap borders
        self.special = False
        self.enter = False
        self.bskey = False
        self.fskey = False
        self.spacekey = False
        self.escape = False
        self.shiftkey = False
        self.font = font
        self.selected = False
        self.dirty = True

        self.image = pygame.Surface((w-2,h-2))
        self.rect = Rect(self.x, self.y, w, h)

        # self.font.render(keyletter, 1, (255, 255, 255))

        self.color = COLORS['TEAL']
        self.selected_color = COLORS['ORANGE']
        self.font_color = COLORS['CLOUD']
        self.caption = caption
        self.shifted_caption = self.caption.translate(Uppercase)
        self.text = self.font.render(self.caption, 1, self.font_color)
        self.shifted_text = self.font.render(self.shifted_caption, 1, self.font_color)




    def update(self, shifted=False, forcedraw=False):
        '''  Draw one key if it needs redrawing '''
        if not forcedraw:
            if not self.dirty:
                return

        text = self.text
        if not self.special:
            if shifted:
                text = self.shifted_text

        if self.selected:
            color = self.selected_color
        else:
            color = self.color


        self.image.fill(color)
        textpos = text.get_rect()
        blockoffx = (self.w / 2)
        blockoffy = (self.h / 2)
        offsetx = blockoffx - (textpos.width / 2)
        offsety = blockoffy - (textpos.height / 2)
        self.image.blit(text, (offsetx, offsety))
        self.dirty = False
