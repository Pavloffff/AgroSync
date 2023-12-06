import math
import random
from enum import Enum
from functools import cmp_to_key

from pygame import Vector2

from src.component.point import Point
from src.grid.chunk import ChunkSprite, Chunk
from src.grid.chunk_types.base import BaseChunk
from src.grid.chunk_types.field import FieldChunk
from src.grid.chunk_types.grass import GrassChunk
from src.grid.chunk_types.ground import GroundChunk
from src.grid.chunk_types.water import WaterChunk
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT, SECTOR_SIZE, CHUNK_SIZE

width, height = FIELD_WIDTH // ChunkSprite.size[0] + 1, FIELD_HEIGHT // ChunkSprite.size[1] + 1


def generate_grid():
    grid = [[] for i in range(height)]
    for i in range(height):
        for j in range(width):
            if i == height // 2 and j == width // 2:
                grid[i].append(BaseChunk.type)
                continue
            if random.randint(0, 9) < 4:
                rand_factor = random.randint(0, 9)
                if 0 < rand_factor < 3:
                    grid[i].append(WaterChunk.type)
                elif 3 < rand_factor < 6:
                    grid[i].append(GroundChunk.type)
                else:
                    grid[i].append(GrassChunk.type)
            else:
                grid[i].append(FieldChunk.type)
    return grid


def smooth_grid(grid: list[list[int]]):
    for i in range(height):
        for j in range(width):
            neighbors = {}
            for y in range(i - 1, i + 2):
                for x in range(j - 1, j + 2):
                    if grid[y % height][x % width] in neighbors.keys():
                        neighbors[grid[y % height][x % width]] += 1
                    else:
                        neighbors[grid[y % height][x % width]] = 1
            types = list(neighbors.keys())
            nums = list(neighbors.values())
            for x in range(1, len(nums)):
                nums[x] += nums[x - 1]
            rand_choose = random.randint(0, nums[len(nums) - 1])
            for x in range(0, len(nums)):
                if rand_choose < nums[x]:
                    grid[i][j] = types[x]
                    break
    return grid


def get_chunk_pos(chunk_idx: tuple[int, int]):
    return Vector2(x=chunk_idx[0] * ChunkSprite.size[0], y=chunk_idx[1] * ChunkSprite.size[1])


def get_chunk_idx(chunk_pos: Vector2):
    return int(chunk_pos.x // ChunkSprite.size[0]), int(chunk_pos.y // ChunkSprite.size[1])


def get_len_path(path: list[tuple[int, int]]):
    s = 0.0
    for i in range(0, len(path) - 1):
        start, end = get_chunk_pos(path[i]), get_chunk_pos(path[i + 1])
        s += math.hypot(start.x - end.x, start.y - end.y)
    return s


class Grid:
    class Phase(Enum):
        Searching = 0
        Working = 1

    def __init__(self, group):
        self.group = group
        self.grid: list[list[Chunk]] = [[] for i in range(height)]
        self.setup_grid()
        self.points: set[Point] = set()
        self.phase = self.Phase.Searching
        self.setup_points()

    def setup_points(self):
        for i in range(0, len(self.grid) // SECTOR_SIZE):
            for j in range(0, len(self.grid[i]) // SECTOR_SIZE):
                point = Point(
                    pos=(j * SECTOR_SIZE + SECTOR_SIZE // 2, i * SECTOR_SIZE + SECTOR_SIZE // 2),
                    weight=1
                )
                self.points.add(point)

    def setup_grid(self):
        grid = generate_grid()
        # for i in range(100):
        #     grid = smooth_grid(grid)

        for i in range(height):
            for j in range(width):
                if i == height // 5 and j == width // 5:
                    self.grid[i].append(BaseChunk(group=self.group, pos=(j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                    continue
                if grid[i][j] == WaterChunk.type:
                    self.grid[i].append(WaterChunk(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                elif grid[i][j] == GroundChunk.type:
                    self.grid[i].append(GroundChunk(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                elif grid[i][j] == GrassChunk.type:
                    self.grid[i].append(GrassChunk(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                else:
                    self.grid[i].append(FieldChunk(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))

    def get_chunk(self, pos: Vector2) -> Chunk:
        current_chunk = get_chunk_idx(pos)
        return self.grid[current_chunk[1]][current_chunk[0]]

    def get_path(self, start: tuple[int, int], end: tuple[int, int]):
        return [start, end]

    def get_path_to_base(self, pos: Vector2):
        to_base_paths = []
        for i in range(height):
            for j in range(width):
                if type(self.grid[i][j]) is BaseChunk:
                    to_base_paths.append(self.get_path(start=get_chunk_idx(pos), end=(j, i)))
        min_s = float('inf')
        min_path = []
        for path in to_base_paths:
            s = get_len_path(path)
            if s < min_s:
                min_s = s
                min_path = path

        return min_path[1:]

    def get_visible(self, size: tuple[int, int], pos: Vector2):
        size_tile = ChunkSprite.size
        current_pos = (pos.x // size_tile[0], pos.y // size_tile[1])
        if current_pos[0] < 0:
            current_pos = (0, pos.y // size_tile[1])
        if current_pos[1] < 0:
            current_pos = (pos.x // size_tile[0], 0)
        current_size = (size[0] // size_tile[0], size[0] // size_tile[1])

        # visible_sprites = []
        for i in range(int(current_pos[1]), int(current_pos[1] + current_size[1]) % height):
            for j in range(int(current_pos[1]), int(current_pos[1] + current_size[1]) % width):
                self.grid[i][j].get_sprite()

    def get_grid(self):
        return self.grid

    def range_points(self, pos: tuple[int, int]):
        point_with_s = []
        for point in self.points:
            s = get_len_path(self.get_path(pos, point.pos))
            point_with_s.append(
                (s, point)
            )

        def compare(x: tuple[float, Point], y: tuple[float, Point]):
            x_w = x[1].weight + 500 / (x[0] + 1)
            y_w = y[1].weight + 500 / (y[0] + 1)
            if x_w < y_w:
                return -1
            elif x_w > y_w:
                return 1
            else:
                return 0

        point_with_s.sort(key=cmp_to_key(compare))

        result_points: list[Point] = []
        for point in point_with_s:
            if point[1].scheduled:
                continue
            result_points.append(point[1])

        return result_points

    def update_point(self, pos: tuple[int, int], assigned_cnt: int = None, weight: int = None, scheduled: bool = None):
        for point in self.points:
            if point.pos[0] == pos[0] and point.pos[1] == pos[1]:
                if assigned_cnt is not None:
                    point.assigned_cnt += assigned_cnt
                    if point.assigned_cnt < 0:
                        point.assigned_cnt = 0
                if weight is not None:
                    point.weight += weight
                    if point.weight < 0:
                        point.weight = 0
                if scheduled is not None:
                    point.scheduled = scheduled

    def __str__(self):
        res = ""
        for i in range(height):
            res += str([int(self.grid[i][j].type > 0) for j in range(width)])
            res += "\n"
        return res
