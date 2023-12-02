from src.grid.chunk import Chunk


class BaseChunk(Chunk):
    def __init__(self, group, pos):
        self.type = 1
        self.image_path = "assets/chunk/ground.png"
        super().__init__(group, pos)
