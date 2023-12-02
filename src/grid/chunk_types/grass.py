from src.grid.chunk import Chunk


class GrassChunk(Chunk):

    def __init__(self, group, pos):
        self.type = 2
        self.image_path = "assets/chunk/grass.png"
        super().__init__(group, pos)
