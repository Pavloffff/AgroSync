from src.grid.chunk import Chunk


class GroundChunk(Chunk):

    def __init__(self, group, pos):
        self.type = 3
        self.image_path = "assets/chunk/ground.png"
        super().__init__(group, pos)
