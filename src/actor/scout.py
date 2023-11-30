import random
from enum import Enum

from pygame import Vector2
from src.actor.drone import Drone
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT


class Scout(Drone):
    def __init__(self, pos: tuple[int, int], group):
        super().__init__(pos=pos, group=group)
        self.state = Scout.Status.Home
    
    def manager(self):
        super().manager()
        if self.state == self.Status.Work and self.finish:
            self.go(Vector2(
                x=random.randint(0, FIELD_WIDTH),
                y=random.randint(0, FIELD_HEIGHT)
            ))
