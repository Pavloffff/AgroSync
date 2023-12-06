import random
from copy import copy
from enum import Enum
from typing import Optional, Union

from pygame import Vector2
from src.actor.drone import Drone
from src.component.point import Point
from src.grid.chunk import Chunk
from src.grid.chunk_types.field import FieldChunk
from src.grid.grid import Grid, get_chunk_idx
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, SECTOR_CNT, SECTOR_SIZE


class Bee(Drone):

    class ProcessField(Drone.Task):
        def __init__(self, target: tuple[int, int], sector: tuple[int, int]):
            self.target = target
            self.sector = sector

        def do(self, drone: super.__class__, dt):
            current_chunk: Union[Chunk, FieldChunk] = drone.grid.get_chunk(drone.position)
            if current_chunk.type != FieldChunk.type:
                drone.finish = True
                return
            if current_chunk.processed:
                drone.finish = True
                return

            drone.battery.state = drone.battery.Status.Move
            drone.finish = False
            drone.grid.update_point(self.sector, weight=-1)

            current_chunk.process_field()
            # drone.add_task(drone.Wait(2))

    def __init__(self, pos: tuple[int, int], group, grid: Grid):
        super().__init__(pos=pos, group=group, grid=grid)
        self.working_on_sector = None
        self.target: Optional[tuple[int, int]] = None

    def manager(self):
        super().manager()

        # if self.state == self.Status.Home and self.working_on_sector is not None:
        #     print("clear")
        #     self.grid.update_point(self.working_on_sector, assigned_cnt=-1)
        #     self.target = None
        #     self.working_on_sector = None

        if self.grid.phase != self.grid.Phase.Working:
            self.go_home()
            return

        # TODO: добавить отметку в точку сектора о том что выполененно
        if self.state == self.Status.Active and self.target is None and self.working_on_sector is None:
            points = self.grid.range_points(get_chunk_idx(self.position))
            choose_point: Optional[Point] = None
            for point in points:
                if choose_point is None:
                    choose_point = point
                    continue
                if point.assigned_cnt < choose_point.assigned_cnt:
                    choose_point = point
                    break
            if choose_point is None:
                return
            self.target = choose_point.pos
            self.grid.update_point(self.target, assigned_cnt=1)
            self.add_task(self.Move(target=self.target))
        elif self.state == self.Status.Active and (
                (
                    get_chunk_idx(self.position) == self.target and self.working_on_sector is None
                ) or (
                    self.target is None and self.working_on_sector is not None
                )
        ):
            position = get_chunk_idx(self.position)
            sector_start_x = (position[0] // SECTOR_SIZE) * SECTOR_SIZE
            sector_start_y = (position[1] // SECTOR_SIZE) * SECTOR_SIZE
            if self.target is not None:
                self.working_on_sector = self.target
            else:
                self.working_on_sector = (sector_start_x, sector_start_y)
            for sect_i in range(0, SECTOR_SIZE):
                for sect_j in range(0, SECTOR_SIZE):
                    if self.grid.grid[sect_i + sector_start_y][sect_j + sector_start_x].assigned:
                        continue
                    self.target = (sect_j + sector_start_x, sect_i + sector_start_y)
                    self.grid.grid[sect_i + sector_start_y][sect_j + sector_start_x].assigned = True
                    self.add_task(self.Move((sect_j + sector_start_x, sect_i + sector_start_y)))
                    return
            if self.working_on_sector is None:
                return
            self.grid.update_point(self.working_on_sector, scheduled=True)
            self.working_on_sector = None
            for point in self.grid.points:
                print(point.pos, point.weight, point.assigned_cnt, point.scheduled)

        elif self.state == self.Status.Active and get_chunk_idx(self.position) == self.target and self.working_on_sector is not None:
            if self.target is None:
                return
            self.add_task(self.ProcessField(self.target, self.working_on_sector))
            self.target = None
