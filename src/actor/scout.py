import random
from enum import Enum

import pygame
from pygame import Vector2
from src.actor.drone import Drone
from src.component.point import Point
from src.grid.grid import Grid
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, SECTOR_SIZE, CHUNK_SIZE


class Scout(Drone):
    def __init__(self, pos: tuple[int, int], group, grid: Grid):
        super().__init__(pos=pos, group=group, grid=grid)
        self.range = 4

    def manager(self):
        super().manager()

        c = (len(self.grid.get_grid()) - 1) / SECTOR_SIZE
        # print(c)

        if self.state == self.Status.Active and len(self.tasks) == 0:
            # сделать через поиск пути

            for i in range(0, len(self.grid.get_grid()) // SECTOR_SIZE):

                if i % 2:

                    for j in range(len(self.grid.get_grid()) // SECTOR_SIZE - 1, -1, -1):
                        self.add_task(self.Move(target=Vector2(
                            x=(SECTOR_SIZE * i + (SECTOR_SIZE // 2)) * CHUNK_SIZE,
                            y=(SECTOR_SIZE * j + (SECTOR_SIZE // 2)) * CHUNK_SIZE
                        )))
                        sum = 0
                        for sect_i in range(SECTOR_SIZE * i, SECTOR_SIZE * (i + 1)):
                            for sect_j in range(SECTOR_SIZE * j, SECTOR_SIZE * (j + 1)):
                                sum += int(self.grid.get_grid()[sect_i][sect_j].type == 0)

                        point = Point(pos=Vector2(
                            x=SECTOR_SIZE * i * CHUNK_SIZE,
                            y=SECTOR_SIZE * j * CHUNK_SIZE,
                        ),
                            weight=sum
                        )
                        self.grid.points.add(point)
                        self.add_task(self.Wait(1))

                else:

                    for j in range(0, len(self.grid.get_grid()) // SECTOR_SIZE):
                        self.add_task(self.Move(target=Vector2(
                            x=(SECTOR_SIZE * i + (SECTOR_SIZE // 2)) * CHUNK_SIZE,
                            y=(SECTOR_SIZE * j + (SECTOR_SIZE // 2)) * CHUNK_SIZE
                        )))
                        sum = 0
                        for sect_i in range(SECTOR_SIZE * i, SECTOR_SIZE * (i + 1)):
                            for sect_j in range(SECTOR_SIZE * j, SECTOR_SIZE * (j + 1)):
                                sum += int(self.grid.get_grid()[sect_i][sect_j].type == 0)

                        point = Point(pos=Vector2(
                            x=SECTOR_SIZE * i * CHUNK_SIZE,
                            y=SECTOR_SIZE * j * CHUNK_SIZE,
                        ),
                            weight=sum
                        )
                        self.grid.points.add(point)
                        self.add_task(self.Wait(1))
            print(len(self.grid.points))
