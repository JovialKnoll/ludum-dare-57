import sys
import os

import jovialengine
import pygame

TITLE = "Template Project"
SCREEN_SIZE = (640, 360)
COLORKEY = (255, 0, 255)
FONT_SIZE = 8
FONT_HEIGHT = 10
FONT_ANTIALIAS = False

EVENT_NAMES = (
    "Left",
    "Right",
    "Up",
    "Down",
    "A",
    "B",
    "X",
    "Y",
)
EVENT_LEFT = jovialengine.EVENT_TYPE_START_POS
EVENT_RIGHT = jovialengine.EVENT_TYPE_START_POS + 1
EVENT_UP = jovialengine.EVENT_TYPE_START_POS + 2
EVENT_DOWN = jovialengine.EVENT_TYPE_START_POS + 3
EVENT_A = jovialengine.EVENT_TYPE_START_POS + 4
EVENT_B = jovialengine.EVENT_TYPE_START_POS + 5
EVENT_X = jovialengine.EVENT_TYPE_START_POS + 6
EVENT_Y = jovialengine.EVENT_TYPE_START_POS + 7
ALL_EVENTS = {
    EVENT_LEFT,
    EVENT_RIGHT,
    EVENT_UP,
    EVENT_DOWN,
    EVENT_A,
    EVENT_B,
    EVENT_X,
    EVENT_Y,
}
INPUT_DEFAULTS = (
    jovialengine.InputDefault(0, EVENT_LEFT, jovialengine.InputType.KEYBOARD, pygame.K_LEFT),
    jovialengine.InputDefault(0, EVENT_RIGHT, jovialengine.InputType.KEYBOARD, pygame.K_RIGHT),
    jovialengine.InputDefault(0, EVENT_UP, jovialengine.InputType.KEYBOARD, pygame.K_UP),
    jovialengine.InputDefault(0, EVENT_DOWN, jovialengine.InputType.KEYBOARD, pygame.K_DOWN),
    jovialengine.InputDefault(0, EVENT_A, jovialengine.InputType.KEYBOARD, pygame.K_z),
    jovialengine.InputDefault(0, EVENT_B, jovialengine.InputType.KEYBOARD, pygame.K_x),
    jovialengine.InputDefault(0, EVENT_X, jovialengine.InputType.KEYBOARD, pygame.K_a),
    jovialengine.InputDefault(0, EVENT_Y, jovialengine.InputType.KEYBOARD, pygame.K_s),
    jovialengine.InputDefault(0, EVENT_LEFT, jovialengine.InputType.CON_HAT, 0),
    jovialengine.InputDefault(0, EVENT_RIGHT, jovialengine.InputType.CON_HAT, 1),
    jovialengine.InputDefault(0, EVENT_UP, jovialengine.InputType.CON_HAT, 2),
    jovialengine.InputDefault(0, EVENT_DOWN, jovialengine.InputType.CON_HAT, 3),
    jovialengine.InputDefault(0, EVENT_A, jovialengine.InputType.CON_BUTTON, 0),
    jovialengine.InputDefault(0, EVENT_B, jovialengine.InputType.CON_BUTTON, 1),
    jovialengine.InputDefault(0, EVENT_X, jovialengine.InputType.CON_BUTTON, 2),
    jovialengine.InputDefault(0, EVENT_Y, jovialengine.InputType.CON_BUTTON, 3),
)

TEXT_COLOR = (164, 162, 165)
DARK_TEXT_COLOR = (82, 81, 83)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_location = '.'
if getattr(sys, 'frozen', False):
    _location = sys.executable
elif __file__:
    _location = __file__
SRC_DIRECTORY = os.path.dirname(_location)

ASSETS_DIRECTORY = os.path.join(SRC_DIRECTORY, 'assets')
FONT_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'fnt')
GRAPHICS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'gfx')
SOUND_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'sfx')
TEXT_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'txt')

FONT = os.path.join(FONT_DIRECTORY, 'simple_mono.ttf')

WINDOW_ICON = os.path.join(GRAPHICS_DIRECTORY, 'icon.png')

LOGOS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'logos')
JK_LOGO_BLACK = os.path.join(LOGOS_DIRECTORY, 'jklogo_black.png')
JK_LOGO_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_grey.png')
JK_LOGO_LIGHT_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_light_grey.png')
STAR = os.path.join(LOGOS_DIRECTORY, 'star.png')

BACKGROUNDS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'backgrounds')

LONGSLIDE = os.path.join(SOUND_DIRECTORY, 'longslide.ogg')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')

IMAGE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'images')

VERSION_TEXT = os.path.join(TEXT_DIRECTORY, 'version.txt')

VERSION = ''
try:
    with open(VERSION_TEXT) as version_file:
        VERSION = version_file.readline().rstrip('\n')
except FileNotFoundError:
    pass
