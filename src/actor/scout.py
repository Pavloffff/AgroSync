import random
from pygame import Vector2
from src.actor.drone import Drone


class Scout:
    def __init__(self, pos: tuple[int, int], group):
        self.drone = Drone(pos=pos, group=group)
        self.start_find()

    def start_find(self):
        self.drone.go(Vector2(1000, 1000))

