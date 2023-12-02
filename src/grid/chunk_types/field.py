from src.grid.chunk import Chunk


class FieldChunk(Chunk):
    def __init__(self, group, pos):
        self.type = 0
        self.image_path = "assets/chunk/raw_field.png"
        super().__init__(group, pos)
