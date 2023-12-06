import random
from copy import copy
from enum import Enum
from typing import Optional, Union

from pygame import Vector2
from src.actor.drone import Drone
from src.grid.chunk import Chunk
from src.grid.chunk_types.field import FieldChunk
from src.grid.grid import Grid, get_chunk_idx
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, SECTOR_CNT, SECTOR_SIZE


class Bee(Drone):

    class ProcessField(Drone.Task):
        def __init__(self, target: tuple[int, int]):
            self.target = target

        def do(self, drone: super.__class__, dt):
            drone: Drone = drone
            current_chunk: Union[Chunk, FieldChunk] = drone.grid.get_chunk(drone.position)
            if current_chunk.type != FieldChunk.type:
                print("dont field")
                drone.finish = True
                return
            if current_chunk.processed:
                print("field already processed")
                drone.finish = True
                return

            drone.battery.state = drone.battery.Status.Move
            drone.finish = False
            print("process field")

            current_chunk.process_field()
            drone.add_task(drone.Wait(2))

    def __init__(self, pos: tuple[int, int], group, grid: Grid):
        super().__init__(pos=pos, group=group, grid=grid)
        self.working_on_sector = None
        self.target: Optional[tuple[int, int]] = None

    def manager(self):
        super().manager()

        if self.grid.phase != self.grid.Phase.Working:
            self.go_home()
            return

        # TODO: добавить отметку в точку сектора о том что выполененно
        if self.state == self.Status.Active and self.target is None and self.working_on_sector is None:
            points = self.grid.range_points(get_chunk_idx(self.position))
            for point in points:
                if point.assigned_cnt < point.weight // 20 + 1:
                    self.target = point.pos
            if self.target is None:
                return
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
            self.working_on_sector = copy(self.target)
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

        elif self.state == self.Status.Active and get_chunk_idx(self.position) == self.target and self.working_on_sector is not None:
            if self.target is None:
                return
            self.add_task(self.ProcessField(self.target))
            self.target = None
