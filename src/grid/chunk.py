from pygame import Vector2
from pygame.sprite import Sprite

from src.settings.settings import LAYERS
from src.support.support import import_image


class ChunkSprite(Sprite):
    size = (256, 256)
    z = LAYERS['field']

    def __init__(self, group, image_path, pos):
        super().__init__(group)
        self.image = import_image(image_path, self.size)
        self.rect = self.image.get_rect(center=Vector2(x=pos[0] + self.size[0] // 2, y=pos[1] + self.size[1] // 2))


class Chunk:
    barrier = False
    image_path: str

    def __init__(self, group, pos):
        self.sprite = ChunkSprite(group=group, pos=pos, image_path=self.image_path)

    def get_sprite(self):
        return self.sprite

    def update(self, dt):
        pass
