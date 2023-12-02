import random

from pygame import Vector2

from src.grid.chunk import ChunkSprite, Chunk
from src.grid.chunk_types.field import FieldChunk
from src.grid.chunk_types.grass import GrassChunk
from src.grid.chunk_types.ground import GroundChunk
from src.grid.chunk_types.water import WaterChunk
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT

width, height = FIELD_WIDTH // ChunkSprite.size[0] + 1, FIELD_HEIGHT // ChunkSprite.size[1] + 1


class Grid:
    def __init__(self, group):
        self.group = group
        self.grid = [[] for i in range(height)]
        for i in range(height):
            for j in range(width):
                if random.randint(0, 9) < 2:
                    rand_factor = random.randint(0, 9)
                    if rand_factor == 0:
                        self.grid[i].append(WaterChunk(group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                    elif 0 < rand_factor < 3:
                        self.grid[i].append(GroundChunk(group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                    else:
                        self.grid[i].append(GrassChunk(group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))
                else:
                    self.grid[i].append(FieldChunk(group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])))

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

    def __str__(self):
        res = ""
        for i in range(height):
            res += str([self.grid[i][j].type for j in range(width)])
            res += "\n"
        return res
