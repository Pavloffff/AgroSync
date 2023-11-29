import pygame
from pygame import Surface
from pygame.math import Vector2
from src.support.support import import_folder
from pygame.transform import rotate


class Drone(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.animations: list[Surface] = []
        self.import_assets()
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = Vector2()
        self.position = Vector2(self.rect.center)
        self.speed = 100

    def import_assets(self):
        full_path = 'assets/drone'
        self.animations = import_folder(full_path)

    def animate(self, dt):
        self.frame_index = (self.frame_index + 100 * dt) % len(self.animations)
        self.image = self.animations[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def change_direction(self, direction: Vector2):
        self.direction.x = direction.x
        self.direction.y = direction.y

    def move(self, dt):

        if self.direction.magnitude():
            self.direction = self.direction.normalize()

        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.position.x

        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y

    def update(self, dt):
        # self.input()
        self.move(dt)
        self.animate(dt)
