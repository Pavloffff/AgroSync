import random
from pygame import Vector2
from src.actor.drone import Drone


class Scout:
    def __init__(self, pos: tuple[int, int], group):
        self.drone = Drone(pos=pos, group=group)
        self.start_find()

    def start_find(self):
        self.drone.change_direction(direction=Vector2(x=1, y=1))

