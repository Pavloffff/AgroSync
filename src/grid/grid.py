from pygame import Vector2

from src.grid.chunk import ChunkSprite, Chunk
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT

width, height = FIELD_WIDTH // ChunkSprite.size[0] + 1, FIELD_HEIGHT // ChunkSprite.size[1] + 1


class Grid:
    def __init__(self, group):
        self.group = group
        self.grid = [[Chunk(group, (j * ChunkSprite.size[0], i * ChunkSprite.size[1])) for j in range(width)] for i in range(height)]

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
