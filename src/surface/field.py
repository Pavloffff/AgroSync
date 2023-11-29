import pygame
from src.settings.settings import *
from src.actor.drone import Drone
from src.actor.scout import Scout


class Field:
    def __init__(self):
        self.drones = []
        self.display_surface = pygame.display.get_surface()
        self.feild_surface = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT))
        self.scale = 1.0
        self.offset = [0, 0]
        self.mouse_down = False
        self.last_mouse_pos = None
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        for i in range(100, 500, 30):
            self.drones.append(Scout((i, i), self.all_sprites))

    def handle_mouse_button_down(self, mouse_pos):
        self.mouse_down = True
        self.last_mouse_pos = mouse_pos

    def handle_mouse_button_up(self):
        self.mouse_down = False
        self.last_mouse_pos = None

    def handle_mouse_motion(self, mouse_pos):
        if self.mouse_down and self.last_mouse_pos:
            dx, dy = mouse_pos[0] - \
                     self.last_mouse_pos[0], mouse_pos[1] - self.last_mouse_pos[1]
            self.offset[0] += dx
            self.offset[1] += dy
            self.last_mouse_pos = mouse_pos

    def zoom(self, direction, mouse_pos):
        old_scale = self.scale
        if direction == "in":
            self.scale = min(5.0, self.scale + 0.1)
        elif direction == "out":
            self.scale = max(0.1, self.scale - 0.1)

        scale_change = self.scale / old_scale

        self.offset[0] = mouse_pos[0] - scale_change * \
                         (mouse_pos[0] - self.offset[0])
        self.offset[1] = mouse_pos[1] - scale_change * \
                         (mouse_pos[1] - self.offset[1])

    def __call__(self, dt, *args, **kwargs):
        self.feild_surface.fill('yellow')  # Заливаем большую поверхность белым
        self.all_sprites.draw(self.feild_surface)  # Рисуем спрайты на большой поверхности

        self.all_sprites.update(dt)

        # Масштабирование большой поверхности до размеров дисплейного экрана
        scaled_surface = pygame.transform.scale(self.feild_surface,
                                                (int(self.feild_surface.get_width() * self.scale),
                                                 int(self.feild_surface.get_height() * self.scale)))

        # Очистка и отображение масштабированной поверхности на дисплейном экране
        self.display_surface.fill('white')
        self.display_surface.blit(scaled_surface, self.offset)
