from enum import Enum

import pygame
from pygame import Surface
from pygame.math import Vector2

from src.component.battery import Battery
from src.component.title import Title
from src.grid.chunk_types.base import BaseChunk
from src.grid.grid import Grid, get_chunk_pos, get_chunk_idx
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, LAYERS
from src.support.support import import_folder
from pygame.transform import rotate


class Drone(pygame.sprite.Sprite):
    size = (64, 64)

    class Task:
        def do(self, drone: super.__class__, dt):
            pass

    class Move(Task):
        def __init__(self, target: tuple[int, int]):
            self.target = target

        def do(self, drone: super.__class__, dt):
            drone.battery.state = drone.battery.Status.Move
            drone.finish = False

            pos_target = get_chunk_pos(self.target)

            direction = Vector2(x=pos_target.x - drone.rect.x, y=pos_target.y - drone.rect.y)
            if get_chunk_idx(drone.position) == self.target:
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

        self.tasks_memory = []

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
        self.speed = 600

        # manage attributes
        self.tasks: list[Drone.Task] = [self.Wait(1)]
        self.finish = False

        # component attributes
        self.battery = Battery(max_size=1000, wait_expense=5, move_expense=10, charging_increment=100)
        self.state = self.Status.Active
        self.title = Title(self.rect, str(self.state))

        # map attribute
        self.grid: Grid = grid

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
            self.tasks = self.tasks_memory
            self.tasks_memory = []
            self.Wait(1).do(self, dt)
        else:
            self.tasks[0].do(self, dt)

    def move_to_path(self, path: list[tuple[int, int]]):
        self.tasks_memory = self.tasks
        self.tasks = []
        for target in path:
            self.tasks.append(self.Move(target))

    def add_task(self, task: Task):
        self.tasks.append(task)

    def go_home(self):
        base_path = self.grid.get_path_to_base(self.position)
        self.state = self.Status.Home
        self.move_to_path(base_path)

    def manager(self):
        if self.battery.get_percent() > 99 or self.battery.state is self.battery.Status.EndCharging:
            self.state = self.Status.Active
        if self.battery.get_percent() < 30 and self.state == self.Status.Active:
            self.go_home()
        elif self.state == self.Status.Home and type(self.grid.get_chunk(self.position)) is BaseChunk and self.battery.state is not self.battery.Status.Charging:
            self.add_task(self.Charging())

    def update(self, dt):
        self.battery.update(dt)
        self.do_tasks(dt)
        self.manager()
        self.animate(dt)
