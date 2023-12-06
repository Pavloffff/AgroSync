from src.grid.chunk import Chunk


class WaterChunk(Chunk):
    type = 4

    def __init__(self, group, pos):
        self.image_path = "assets/chunk/water.png"
        super().__init__(group, pos)
