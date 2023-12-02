from src.grid.chunk import Chunk


class WaterChunk(Chunk):

    def __init__(self, group, pos):
        self.type = 4
        self.image_path = "assets/chunk/water.png"
        super().__init__(group, pos)
