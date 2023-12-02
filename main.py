import pygame
import sys

from src.component.title import Title
from src.settings.settings import *
from src.surface.field import Field


class Model:
    __running = True

    def __init__(self):
        pygame.init()
        Title.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AgroSync")
        self.clock = pygame.time.Clock()
        self.field = Field()

    def __call__(self, *args, **kwargs):
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [1, 3]:  # Левая кнопка мыши
                        self.field.handle_mouse_button_down(
                            pygame.mouse.get_pos())
                    elif event.button == 4:  # Колесико вверх
                        self.field.zoom("in", pygame.mouse.get_pos())
                    elif event.button == 5:  # Колесико вниз
                        self.field.zoom("out", pygame.mouse.get_pos())

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button in [1, 3]:  # Левая кнопка мыши
                        self.field.handle_mouse_button_up()
                elif event.type == pygame.MOUSEMOTION:
                    self.field.handle_mouse_motion(pygame.mouse.get_pos())

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.field(dt)
            pygame.display.update()


if __name__ == "__main__":
    model = Model()
    model()
