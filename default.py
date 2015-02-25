import sys
import pygame
import imp
import os
import random
import traceback
from global_variables import *
from time import time, sleep
from keyboard import VirtualKeyboard
sys.dont_write_bytecode = True

debug = True
screensleep = 60000

# This is where we start
# Initialise pygame

RASPBERRYPI = False
# pprint(pygame.di`play.list_modes(), 3)
# Tell the RPi to use the TFT screen and that it's a touchscreen device
if os.name == 'posix':
    RASPBERRYPI = True
    print "You're running raspberry pi"
    # Hide mouse
    from pitftgpio import PiTFT_GPIO
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
    tftscreen = PiTFT_GPIO()
##############################################################################
# Create a clock and set max FPS (This reduces a lot CPU ussage)
pygame.init()
# Screen size (currently fixed)
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

# Set up the callback functions for the buttons
if RASPBERRYPI:
    tftscreen.Button1Interrupt(TFTBtn1Click)
    tftscreen.Button2Interrupt(TFTBtn2Click)
    tftscreen.Button3Interrupt(TFTBtn3Click)
    tftscreen.Button4Interrupt(TFTBtn4Click)

pygame.mouse.set_visible(False if RASPBERRYPI else True)

FPS = 15
clock = pygame.time.Clock()
screenindex = 0


quit = False
# b = pygame.time.get_ticks()
d = 0
newscreen = False
newwait = 0
# refresh = 60000
# refreshNow = False
# SWIPE_TO_SCREEN = 0
# CURRENT_SCREEN = -1


def log(message):
    '''Prints message if user has set debug flag to true.'''
    if debug:
        print message

# ##############################################################################
# Plugin handling code adapted from:
# http://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
# THANK YOU!
# # ######################################################################


def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    a = 1
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(
                location) or PluginScript not in os.listdir(location):
            continue
        inf = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": inf, "id": a})
        a = a + 1
    return plugins


def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])
##############################################################################

##############################################################################
# Initialise plugin screens


def getScreens():
    '''Gets list of available plugin screen objects.'''
    a = []
    for i in getPlugins():
        plugin = loadPlugin(i)
        try:
            # The plugin should have the myScreen function
            # We send the screen size for future proofing (i.e. plugins should
            # be able to cater for various screen resolutions
            #
            # TO DO: Work out whether plugin can return more than one screen!
            loadedscreen = plugin.myScreen(size, userevents=piscreenevents)
            a.append(loadedscreen)
            showLoadedPlugin(loadedscreen)

        except:
            # If it doesn't work, ignore that plugin and move on
            log(traceback.format_exc())
            continue
    return a
##############################################################################


##############################################################################
# Event handling methods
# def setUpdateTimer(pluginloadtime):
    # ''' Sets an update timer
    # Depending on the speed of the processor, the timer
    # can flood the event queue with UPDATE events but
    # if the plugin takes a while to load there may be no time for
    # anything else.
    # This function provides some headroom in the timer
    # '''
    # interval = max(5 * pluginloadtime, pluginScreens[screenindex].refreshtime)

    # pygame.time.set_timer(UPDATESCREEN, 0)
    # pygame.time.set_timer(UPDATESCREEN, interval)

loading_font = pygame.font.Font(FONTS['swipe_font']['path'], 18)


def showWelcomeScreen():
    '''Display a temporary screen to show it's working
    May not display for long because of later code to show plugin loading
    '''
    screen.fill(COLORS['CLOUD'])
    label = loading_font.render(
        "Initialising screens...",
        1,
        COLORS['BLUE-GREY']['600'])
    labelpos = label.get_rect()
    labelpos.centerx = screen.get_rect().centerx
    labelpos.centery = screen.get_rect().centery
    screen.blit(label, labelpos)
    pygame.display.flip()
    # pass
    # sleep(.5)


def showLoadedPlugin(plugin):
    '''Display a temporary screen to show when a module is successfully
    loaded.
    '''
    # pass
    # print "showloadedplugin"
    message = random.choice(LOADING_MESSEGES)
    LOADING_MESSEGES.remove(message)

    screen.fill(COLORS['CLOUD'])
    label = loading_font.render(message, 1, plugin.color)
    labelpos = label.get_rect()
    labelpos.centerx = screen.get_rect().centerx
    labelpos.centery = screen.get_rect().centery
    screen.blit(label, labelpos)
    pygame.display.flip()
    sleep(.5)


def setNextScreen(a, screenindex):
    '''Queues the next screen.'''
    # pygame.time.set_timer(NEWSCREEN, 0)
    # pygame.time.set_timer(UPDATESCREEN, 0)
    pygame.event.post(pygame.event.Event(NEXTSCREEN))

    screenindex += a
    if screenindex < 0:
        screenindex = len(pluginScreens) - 1
    if screenindex > len(pluginScreens) - 1:
        screenindex = 0

    displayLoadingScreen(screenindex)
    return screenindex


def displayLoadingScreen(a):
    # '''Displays a loading screen.'''

    # -----------KEEP THIS!!!--------------
    # It may be needed if screens take too long to loading
    # ---------------------------------------------
    # screen.fill(COLORS['CLOUD'])

    # holdtext = myfont.render("Loading screen: %s"
                            # % pluginScreens[a].screenName(),
                            # 1,
                            # (255,255,255))
    # holdrect = holdtext.get_rect()
    # holdrect.centerx = screen.get_rect().centerx
    # holdrect.centery = screen.get_rect().centery
    # screen.blit(holdtext, holdrect)
    # pygame.display.flip()
    # NEWSCREEN()
    # NEWSCREEN()
    # pygame.time.set_timer(NEWSCREEN, 1)
    pass


def showNewScreen():
    # '''Show the next screen.'''
    # pygame.time.set_timer(NEWSCREEN, 0)
    strttime = time()
    screen = pluginScreens[screenindex].showScreen()
    stptime = time()
    plugdiff = int((stptime - strttime) * 2000)
    # print plugdiff
    # setUpdateTimer(plugdiff)
    pygame.display.flip()

#############################################################################


def longPress(downTime):
    if pygame.time.get_ticks() - longPressTime > downTime:
        return True
    else:
        return False


# Initialise screen object
# if RASPBERRYPI:
#     tftscreen = PiTFT_GPIO()
# Plugin location and names
PluginFolder = "./plugins"
PluginScript = "screen.py"
MainModule = "screen"
pluginScreens = []


# Set our screen size
# Should this detect attached display automatically?


# Set ner (useful for testing, not so much for full screen mode!)
pygame.display.set_caption("Info screen")

# Stop keys repeating
pygame.key.set_repeat()

# Base font for messages
# myfont = pygame.font.SysFont(None, 20)

# Show welcome screen
# showWelcomeScreen()

# Get list of screens that can be provided by plugins
pluginScreens = getScreens()
# Parse some options
# try:
#     opts, args = getopt.getopt(sys.argv[1:], 'lh', ['help', 'list'])
# except getopt.GetoptError as err:
#     log(err)
#     usage()
#     sys.exit()

# for o, a in opts:
# Show installed plugins
#     if o in ("-l", "--list"):
#         listPlugins()
#         sys.exit()
# Show help
#     if o in ("-h", "--help"):
#         usage()
#         sys.exit()
# TO DO: add option for automatic screen change (with timeout)

# Set some useful variables for controlling the display


mouseDownTime = 0
mouseDownPos = (0, 0)
mouseUpPos = (0, 0)
# Mouse related variables
minSwipe = 30
maxClick = 10
longPressTime = 200


# Function to detect swipes
# -1 is that it was not detected as a swipe or click
# It will return 1 , 2 for horizontal swipe
# If the swipe is vertical will return 3, 4
# If it was a click it will return 0
def getSwipeType():
    x_down, y_down = mouseDownPos
    x_up, y_up = mouseUpPos
    x = x_up - x_down
    y = y_up - y_down


    print x
    print y
    # y_swipe = 0
    # x_swipe = 0
    swipe = 0

    if abs(x) < minSwipe and abs(y) < minSwipe:
        print "Click"
        return 0
    if abs(x) < abs(y):
        if y > 0:
            # print "swipe down"
            return 3
        if y < 0:
            print y
            # print "swipe up"
            return 4
    if abs(y) < abs(x):
        if x > 0:
            print x
            # print "swipe right"
            return 1
        if x < 0:
            # print "swipe left"
            print x
            return 2
    # print "nothing"
    return 0
# def getSwipeType():
#     x, y = pygame.mouse.get_rel()
#     print abs(x)
#     print abs(y)
#     y_swipe = 0
#     x_swipe = 0
#     swipe = 0
#     if abs(x) <= minSwipe:
#         if abs(y) <= minSwipe:
#             if abs(x) < maxClick and abs(y) < maxClick:
#                 print "click"
#                 # pygame.mouse.set_pos(0, 0)
#                 return 0
#             else:
#                 # not detected as a swipe or click
#                 print "not a swipe or a click"
#                 # y_swipe = -1
#                 return -1
#         elif y > minSwipe:
#             print "vertical 3"
#             y_swipe = 3
#         elif y < -minSwipe:
#             # pygame.mouse.set_pos(0, 0)
#             print "vertical 4"
#             y_swipe = 4
#         else:
#             print "first wtf"
#     if abs(y) <= minSwipe:
#         if x > minSwipe:
#             # pygame.mouse.set_pos(0, 0)
#             print "horizontal 1"
#             x_swipe = 1
#         elif x < -minSwipe:
#             # pygame.mouse.set_pos(0, 0)
#             print "horizontal 2"
#             x_swipe = 2
#         else: print "second wtf"
#     print (x_swipe)
#     print (y_swipe)
#     if x_swipe == 0:
#         print "returning y_swipe " + str(y_swipe)
#         return y_swipe
#     elif y_swipe == 0:
#         print "returning x_swipe " + str(x_swipe)
#         return x_swipe
#     elif abs(x) > abs(y):
#         print "returning x_swipe " + str(x_swipe)
#         return x_swipe
#     else:
#         print "returning y_swipe " + str(y_swipe)
#         return y_swipe

#     print "nothing cought"
#     return 0


def longPress(downTime):
    if pygame.time.get_ticks() - longPressTime > downTime:
        return True
    else:
        return False


# Queue the first screen
displayLoadingScreen(screenindex)

# Run our main loop
while not quit:
    for event in pygame.event.get():
        # Handle quit message received
        if event.type == pygame.QUIT:
            quit = True
        # if event.type == TIME_CHANGED:
            # print "time Changed"
            # pygame.time.Clock()
            # continue
        # send the event to the current screenindex
        # this allows user interaction without interfering with
        # swipe gestures
        # 'Q' to quit

        # mouse button pressed
        if (event.type == pygame.MOUSEBUTTONDOWN):
            print "mouse_down"
            mouseDownTime = pygame.time.get_ticks()
            mouseDownPos = pygame.mouse.get_pos()
            # pygame.mouse.get_rel()

        if (event.type == pygame.MOUSEBUTTONUP):
            print "mouse_up"
            mouseUpPos = pygame.mouse.get_pos()
            swipe = getSwipeType()
            print "Swipe: " + str(swipe)
            # print "Screen Index Before: " + str(screenindex)
            if swipe == 1:
                pluginScreens[screenindex].exit_function()
                screenindex = setNextScreen(1, screenindex)
                continue
            elif swipe == 2:
                pluginScreens[screenindex].exit_function()
                screenindex = setNextScreen(-1, screenindex)
                # clock = pygame.time.Clock()
                continue
            elif swipe == 3:
                tmp_event = pygame.event.Event(SWIPE_DOWN, value=1)
                pluginScreens[screenindex].event_handler(tmp_event)
                continue
                # quit = True
                # continue
            elif swipe == 4:
                # vkey = VirtualKeyboard(screen)
                # tmp = vkey.run('')
                tmp_event = pygame.event.Event(SWIPE_UP, value=1)
                pluginScreens[screenindex].event_handler(tmp_event)
                continue
            # print "Screen Index After: " + str(screenindex)

        if (event.type == TFTBUTTONCLICK):
            if (event.button == 1):
                pluginScreens[a].Button1Click()

            if (event.button == 2):
                pluginScreens[a].Button2Click()

            if (event.button == 3):
                pluginScreens[a].Button3Click()

            if (event.button == 4):
                pluginScreens[a].Button4Click()

        if (event.type == NEWSCREEN):
            showNewScreen()
        pluginScreens[screenindex].event_handler(event)

    screen = pluginScreens[screenindex].showScreen()
    # Control FPS
    # if CLOCK_DIRTY == True:
        # clock = pygame.time.Clock()
        # CLOCK_DIRTY = False
    pygame.display.flip()
    pygame.time.Clock()

# If we're here we've exited the display loop...
log("Exiting...")
pygame.quit()
sys.exit(0)
