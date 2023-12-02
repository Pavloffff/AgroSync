from src.grid.chunk import Chunk


class GroundChunk(Chunk):
    type = 3
    def __init__(self, group, pos):
        self.image_path = "assets/chunk/ground.png"
        super().__init__(group, pos)
