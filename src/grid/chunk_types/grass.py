from src.grid.chunk import Chunk


class GrassChunk(Chunk):
    type = 2

    def __init__(self, group, pos):
        self.image_path = "assets/chunk/grass.png"
        super().__init__(group, pos)
