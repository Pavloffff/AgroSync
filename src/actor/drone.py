from enum import Enum

import pygame
from pygame import Surface
from pygame.math import Vector2

from src.component.battery import Battery
from src.component.title import Title
from src.grid.chunk_types.base import Base
from src.grid.grid import Grid
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, LAYERS
from src.support.support import import_folder
from pygame.transform import rotate


class Drone(pygame.sprite.Sprite):
    size = (128, 128)

    class Task:
        def do(self, drone: super.__class__, dt):
            pass

    class Move(Task):
        def __init__(self, target: Vector2):
            if 0 <= target.x <= FIELD_WIDTH and 0 <= target.y <= FIELD_HEIGHT:
                self.target = target
            else:
                self.target = Vector2(
                    x=target.x % FIELD_WIDTH if target.x >= 0 else 0,
                    y=target.y % FIELD_HEIGHT if target.y >= 0 else 0
                )

        def do(self, drone: super.__class__, dt):
            drone.battery.state = drone.battery.Status.Move
            drone.finish = False

            direction = Vector2(x=self.target.x - drone.rect.x, y=self.target.y - drone.rect.y)
            if direction.x == 0 and direction.y == 0:
                drone.finish = True
                return

            if direction.magnitude():
                direction = direction.normalize()

            drone.position.x += direction.x * drone.speed * dt
            drone.rect.centerx = drone.position.x

            drone.position.y += direction.y * drone.speed * dt
            drone.rect.centery = drone.position.y

    class Wait(Task):
        def __init__(self, wait_time: int):
            self.wait_time = wait_time

        def do(self, drone: super.__class__, dt):
            drone.battery.state = drone.battery.Status.Wait
            drone.finish = False

            if self.wait_time > 0:
                self.wait_time -= 1 * dt
            else:
                drone.finish = True

    class Charging(Task):
        def do(self, drone: super.__class__, dt):
            drone.finish = False
            if drone.battery.state == drone.battery.Status.EndCharging:
                drone.finish = True
            drone.battery.state = drone.battery.Status.Charging

    class Status(Enum):
        Active = 1
        Home = 2

    def __init__(self, pos, group, grid: Grid):
        super().__init__(group)

        self.animations: list[Surface] = []
        self.import_assets()
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['drone']

        # movement attributes
        self.direction = Vector2()
        self.position = Vector2(self.rect.center)
        self.speed = 300

        # manage attributes
        self.tasks: list[Drone.Task] = [self.Wait(1)]
        self.finish = False

        # component attributes
        self.battery = Battery(max_size=1000, wait_expense=50, move_expense=100, charging_increment=100)
        self.state = self.Status.Active
        self.title = Title(self.rect, str(self.state))

        # map attribute
        self.grid = grid

    def import_assets(self):
        full_path = 'assets/drone'
        self.animations = import_folder(full_path, self.size)

    def animate(self, dt):
        self.frame_index = (self.frame_index + 100 * dt) % len(self.animations)
        self.title.update(str(self.state) + " " + str(self.battery))
        self.image = self.animations[int(self.frame_index)]

    def do_tasks(self, dt):
        if self.finish:
            self.tasks = self.tasks[1:] if len(self.tasks) > 1 else []
        if len(self.tasks) == 0:
            self.Wait(1).do(self, dt)
        else:
            self.tasks[0].do(self, dt)

    def move_to_path(self, path: list[Vector2]):
        self.tasks.clear()
        for target in path:
            self.tasks.append(self.Move(target))

    def add_task(self, task: Task):
        self.tasks.clear()
        self.tasks.append(task)

    def manager(self):
        if self.battery.get_percent() > 99:
            self.state = self.Status.Active
            return
        if self.battery.get_percent() < 30 and self.state == self.Status.Active:
            base_path = self.grid.get_path_to_base(self.position)
            self.state = self.Status.Home
            self.move_to_path(base_path)
        elif self.state == self.Status.Home and type(self.grid.get_chunk(self.position)) is Base:
            self.add_task(self.Charging())

    def update(self, dt):
        self.battery.update(dt)
        self.do_tasks(dt)
        self.manager()
        self.animate(dt)
