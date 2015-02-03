import sys
import pygame
sys.dont_write_bytecode = True

ROWS = {'1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D',
        '5': 'E',
        '6': 'F',
        '7': 'G',
        '8': 'H',
        '9': 'I',
        '10': 'J',
        '11': 'K',
        '12': 'L'
        }

# TITLE_RECT = pygame.Rect(3, 30, 314, 60)
TITLE_RECT = pygame.Rect(0, 25, 320, 70)
SWIPE_HINT_RECT = pygame.Rect(0, 210, 320, 30)


COLORS = {
    'RED':         (231, 76,  60),
    'BLUE':        (52,  152, 219),
    'TEAL':        (26,  188, 156),
    'PURPLE':      (155, 89,  182),
    'GREEN':       (46,  204, 113),
    'ORANGE':      (230, 126, 34),
    'YELLOW':      (241, 196, 15),
    'CLOUD':       (236, 240, 241),
    'ASPHALT':     (52,  73,  94),
    'CONCRETE':    (149, 165, 166),
    'TRANSPARENT': (0,   0,   0,   0)
}
LOADING_MESSEGES = [
    "Creating Time-Loop Inversion Field",
    "Loading the Loading message..",
    "Randomizing memory access...",
    "Tube Clamp Error",
    "Priming reagents.",
    "Testing CP functions",
    "Homing",
    "Running Enhanced clean on all probes"
]