import random
from enum import Enum
from typing import Optional

import pygame
from pygame import Vector2
from src.actor.drone import Drone
from src.component.point import Point
from src.grid.grid import Grid, get_chunk_idx
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, SECTOR_SIZE, CHUNK_SIZE


class Scout(Drone):
    def __init__(self, pos: tuple[int, int], group, grid: Grid):
        super().__init__(pos=pos, group=group, grid=grid)
        self.range = 4
        self.target: Optional[tuple[int, int]] = None

    def manager(self):
        super().manager()

        if self.state == self.Status.Home and self.target is not None:
            self.grid.update_point(self.target, assigned_cnt=-1)
            self.target = None

        if self.grid.phase != self.grid.Phase.Searching:
            self.go_home()
            return

        all_doing = True
        for point in self.grid.points:
            if not point.scheduled:
                all_doing = False
                break

        if all_doing:
            self.grid.phase = self.grid.Phase.Working
            for point in self.grid.points:
                point.scheduled = False
            return

        if self.state == self.Status.Active and self.target is None:
            points = self.grid.range_points(get_chunk_idx(self.position))
            for point in points:
                if point.assigned_cnt < 1:
                    self.target = point.pos
            if self.target is None:
                return
            self.grid.update_point(self.target, assigned_cnt=1)
            self.add_task(self.Move(target=self.target))
        elif self.state == self.Status.Active and get_chunk_idx(self.position) == self.target:
            self.add_task(self.Wait(1))

            weight = 0
            position = get_chunk_idx(self.position)
            sector_start_x = (position[0] // SECTOR_SIZE) * SECTOR_SIZE
            sector_start_y = (position[1] // SECTOR_SIZE) * SECTOR_SIZE
            for sect_i in range(0, SECTOR_SIZE):
                for sect_j in range(0, SECTOR_SIZE):
                    weight += int(self.grid.get_grid()[sect_i + sector_start_y][sect_j + sector_start_x].type == 0)

            print(position, weight)

            self.grid.update_point(self.target, assigned_cnt=-1, scheduled=True, weight=weight)
            self.target = None
