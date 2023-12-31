import ctypes

import pygame
from pygame.math import Vector2
from pygetwindow import getActiveWindow
from screeninfo import get_monitors


def get_screen_resolution():
    active_window = getActiveWindow()

    window_left = abs(active_window.left)
    window_top = abs(active_window.top)

    for monitor in get_monitors():
        if (monitor.x <= window_left <= monitor.x + monitor.width + 100) and \
                (monitor.y <= window_top <= monitor.y + monitor.height + 100):
            return monitor.width, monitor.height

    return 800, 800


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_resolution()

LAYERS = {
    'field': 0,
    'drone': 1
}

SCOUT_CNT = 4
BEE_CNT = 10
SECTOR_SIZE = 8
CHUNK_SIZE = 128

FIELD_WIDTH, FIELD_HEIGHT = SECTOR_SIZE * CHUNK_SIZE * 5, SECTOR_SIZE * CHUNK_SIZE * 5

SECTOR_CNT = (FIELD_WIDTH // (SECTOR_SIZE * CHUNK_SIZE)) * (FIELD_HEIGHT // (SECTOR_SIZE * CHUNK_SIZE))
# FIELD_WIDTH, FIELD_HEIGHT = 2048, 2048
