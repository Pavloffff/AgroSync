from src.grid.chunk import Chunk, ChunkSprite


class FieldChunk(Chunk):
    type = 0

    def __init__(self, group, pos):
        self.image_path = "assets/chunk/raw_field.png"
        self.processed = False
        super().__init__(group, pos)

    def process_field(self):
        self.image_path = "assets/chunk/processed_field.png"
        self.sprite = ChunkSprite(group=self.group, pos=self.pos, image_path=self.image_path)
        self.processed = True
