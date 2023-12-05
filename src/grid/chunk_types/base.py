from src.grid.chunk import Chunk


class BaseChunk(Chunk):
    type = 1

    def __init__(self, group, pos):
        self.image_path = "assets/chunk/base.png"
        super().__init__(group, pos)
