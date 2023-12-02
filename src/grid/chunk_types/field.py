from src.grid.chunk import Chunk


class FieldChunk(Chunk):
    type = 0

    def __init__(self, group, pos):
        self.image_path = "assets/chunk/raw_field.png"
        super().__init__(group, pos)
