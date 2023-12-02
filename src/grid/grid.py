from pygame import Vector2

from src.grid.chunk import ChunkSprite, Chunk
from src.grid.chunk_types.base import Base
from src.grid.chunk_types.grass import Grass
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT

width, height = FIELD_WIDTH // ChunkSprite.size[0] + 1, FIELD_HEIGHT // ChunkSprite.size[1] + 1


def get_chunk_pos(chunk_idx: tuple[int, int]):
    return Vector2(x=chunk_idx[0] * ChunkSprite.size[0], y=chunk_idx[1] * ChunkSprite.size[1])


def get_chunk_idx(chunk_pos: Vector2):
    return int(chunk_pos.x // ChunkSprite.size[0]), int(chunk_pos.y // ChunkSprite.size[1])


class Grid:
    def __init__(self, group):
        self.group = group
        self.grid = [
            [None for j in range(width)] for i in range(height)]
        self.setup_grid()

    def setup_grid(self):
        for i in range(height):
            for j in range(width):
                if i == height // 2 and j == width // 2:
                    print(i, j)
                    self.grid[i][j] = Base(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1]))
                    continue
                self.grid[i][j] = Grass(self.group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1]))

    def get_chunk(self, pos: Vector2):
        size_tile = ChunkSprite.size
        current_chunk = get_chunk_idx(pos)
        return self.grid[current_chunk[1]][current_chunk[0]]

    def get_path_to_base(self, pos: Vector2):
        # TODO: тут нужен нормальный поиск
        for i in range(height):
            for j in range(width):
                if type(self.grid[i][j]) is Base:
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
