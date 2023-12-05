import random

from pygame import Vector2

from src.grid.chunk import ChunkSprite
from src.grid.chunk_types.base import BaseChunk
from src.grid.chunk_types.field import FieldChunk
from src.grid.chunk_types.grass import GrassChunk
from src.grid.chunk_types.ground import GroundChunk
from src.grid.chunk_types.water import WaterChunk
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT

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


class Grid:
    def __init__(self, group):
        self.group = group
        self.grid = [[] for i in range(height)]
        self.setup_grid()
        self.points = set()

    def setup_grid(self):
        grid = generate_grid()
        for i in range(100):
            grid = smooth_grid(grid)

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

    def get_chunk(self, pos: Vector2):
        size_tile = ChunkSprite.size
        current_chunk = get_chunk_idx(pos)
        return self.grid[current_chunk[1]][current_chunk[0]]

    def get_path_to_base(self, pos: Vector2):
        # TODO: тут нужен нормальный поиск
        for i in range(height):
            for j in range(width):
                if type(self.grid[i][j]) is BaseChunk:
                    return [get_chunk_pos((j, i))]
        return []

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

    def __str__(self):
        res = ""
        for i in range(height):
            res += str([int(self.grid[i][j].type > 0) for j in range(width)])
            res += "\n"
        return res
