import pygame
from pygame import Rect


class Title:
    font: pygame.font.Font

    def __init__(self, rect: Rect, text: str):
        self.rect = rect
        self.title = self.font.render(text, True, (0, 0, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = rect.centerx
        self.title_rect.bottom = rect.top

    def update(self, text: str):
        self.title = self.font.render(text, True, (0, 0, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = self.rect.centerx
        self.title_rect.bottom = self.rect.top
