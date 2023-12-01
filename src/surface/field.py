import pygame

from src.grid.grid import Grid
from src.settings.settings import *
from src.actor.drone import Drone
from src.actor.scout import Scout


class Field:
    def __init__(self):
        # self.square = None
        self.drones = []
        self.titles = []
        self.display_surface = pygame.display.get_surface()
        self.field_surface = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT))
        self.scale = 0.5
        self.offset = [0, 0]
        self.mouse_down = False
        self.last_mouse_pos = None
        self.all_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.grid = Grid(self.all_sprites)
        self.setup()

    def setup(self):
        for i in range(500, 1500, 50):
            drone = Scout((i, i), self.all_sprites)
            self.drones.append(drone)
            self.titles.append(drone.title)

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
            self.scale = min(0.8, self.scale + 0.1)
        elif direction == "out":
            self.scale = max(0.1, self.scale - 0.1)

        scale_change = self.scale / old_scale

        self.offset[0] = mouse_pos[0] - scale_change * \
                         (mouse_pos[0] - self.offset[0])
        self.offset[1] = mouse_pos[1] - scale_change * \
                         (mouse_pos[1] - self.offset[1])

    def get_visible_rect(self):
        return pygame.Rect(
            -self.offset[0] / self.scale,
            -self.offset[1] / self.scale,
            (self.display_surface.get_width()) / self.scale,
            (self.display_surface.get_height()) / self.scale
        )

    def is_sprite_visible(self, sprite):
        visible_rect = self.get_visible_rect()
        sprite_rect = sprite.rect
        scaled_sprite_rect = pygame.Rect(
            (sprite_rect.x - self.offset[0] * self.scale) * self.scale,
            (sprite_rect.y - self.offset[1] * self.scale) * self.scale,
            float(sprite_rect.width) * self.scale,
            float(sprite_rect.height) * self.scale
        )
        return visible_rect.colliderect(scaled_sprite_rect)

    def __call__(self, dt, *args, **kwargs):
        self.field_surface.fill('yellow')
        self.all_sprites.update(dt)

        visible_rect = self.get_visible_rect()
        self.grid.get_visible(
            pos=Vector2(x=visible_rect.x, y=visible_rect.y),
            size=visible_rect.size
        )

        for sprite in self.all_sprites:
            visible = self.is_sprite_visible(sprite)
            if visible:
                self.visible_sprites.add(sprite)
            elif self.visible_sprites.has(sprite):
                self.visible_sprites.remove(sprite)

        print(self.visible_sprites)

        self.visible_sprites.draw(self.field_surface)

        for title in self.titles:
            if self.is_sprite_visible(title):
                self.field_surface.blit(title.title, title.title_rect)

        scaled_surface = pygame.transform.scale(self.field_surface,
                                                (int(self.field_surface.get_width() * self.scale),
                                                 int(self.field_surface.get_height() * self.scale)))

        self.display_surface.fill('white')
        self.display_surface.blit(scaled_surface, self.offset)
