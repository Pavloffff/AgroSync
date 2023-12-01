from enum import Enum

import pygame
from pygame import Surface
from pygame.math import Vector2

from src.component.battery import Battery
from src.component.title import Title
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT
from src.support.support import import_folder
from pygame.transform import rotate


class Drone(pygame.sprite.Sprite):
    size = (128, 128)

    class Status(Enum):
        Work = 1
        Home = 2
        Charging = 3
        Wait = 4

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
        self.speed = 300

        self.target = Vector2(self.rect.center)
        self.finish = True
        self.wait_time = 0

        self.battery = Battery(max_size=1000, wait_expense=50, move_expense=100, charging_increment=100)
        self.state = None
        self.title = Title(self.rect, str(self.state))

        self.home = Vector2(pos[0], pos[1])

    def import_assets(self):
        full_path = 'assets/drone'
        self.animations = import_folder(full_path, self.size)

    def animate(self, dt):
        self.frame_index = (self.frame_index + 100 * dt) % len(self.animations)
        self.title.update(str(self.state) + " " + str(self.battery))
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

    def move(self, dt):
        if self.finish:
            return

        self.direction = Vector2(x=self.target.x - self.rect.x, y=self.target.y - self.rect.y)

        if self.battery.state == self.battery.Status.EndCharging:
            self.finish = True
            return
        elif self.state == self.Status.Charging:
            return

        if self.wait_time > 0:
            self.wait_time -= 1 * dt
            return
        elif self.state == self.Status.Wait:
            self.wait_time = 0
            self.finish = True
            return

        if self.direction.x == 0 and self.direction.y == 0:
            self.finish = True
            return

        if self.direction.magnitude():
            self.direction = self.direction.normalize()

        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.position.x

        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y

    def go(self, target: Vector2):
        if 0 < target.x < FIELD_WIDTH and 0 < target.y < FIELD_HEIGHT:
            self.battery.state = self.battery.Status.Move
            self.target = target
            self.finish = False

    def wait_drone(self, time: int):
        if time > 0:
            self.target = Vector2(x=self.rect.x, y=self.rect.y)
            self.battery.state = self.battery.Status.Wait
            self.wait_time = time
            self.finish = False

    def charging(self):
        self.target = Vector2(x=self.rect.x, y=self.rect.y)
        self.state = self.Status.Charging
        self.battery.state = self.battery.Status.Charging
        self.finish = False

    def manager(self):
        if self.state == self.Status.Home and self.finish:
            self.charging()
            return
        if self.state == self.Status.Charging and self.finish:
            self.state = self.Status.Work
            return
        if self.state == self.Status.Work or self.state == self.Status.Wait:
            if self.battery.predict_move_expense(
                current_pos=Vector2(x=self.rect.x, y=self.rect.y),
                target_pos=self.home,
                speed=self.speed
            ) < 5:
                self.state = self.Status.Home
                self.go(self.home)
                return

    def update(self, dt):
        self.battery.update(dt)
        self.move(dt)
        self.manager()
        self.animate(dt)
