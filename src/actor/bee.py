import random
from enum import Enum

from pygame import Vector2
from src.actor.drone import Drone
from src.grid.grid import Grid
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT


class Bee(Drone):
    def __init__(self, pos: tuple[int, int], group, grid: Grid):
        super().__init__(pos=pos, group=group, grid=grid)

    def manager(self):
        super().manager()
        if self.state == self.Status.Active and len(self.tasks) == 0:
            # сделать через поиск пути
            self.add_task(self.Move(target=Vector2(
                x=random.randint(1, FIELD_WIDTH - 1),
                y=random.randint(1, FIELD_HEIGHT - 1)
            )))
