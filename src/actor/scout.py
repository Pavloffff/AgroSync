import random
from enum import Enum

from pygame import Vector2
from src.actor.drone import Drone
from src.settings.settings import FIELD_WIDTH, FIELD_HEIGHT


class Scout(Drone):
    class Status(Enum):
        Find = 1
        Home = 2
        Charging = 3

    def __init__(self, pos: tuple[int, int], group):
        super().__init__(pos=pos, group=group)
        self.home = Vector2(pos[0], pos[1])
        self.state = Scout.Status.Home

    def update(self, dt):
        # print(self.state, self.finish, self.battery)
        super().update(dt)
        if self.state == Scout.Status.Charging:
            self.battery += 100 * dt
        if self.battery < 300:
            self.state = Scout.Status.Home

        if self.state == Scout.Status.Home and self.finish:
            self.state = Scout.Status.Charging
            self.wait_drone(1000)
        elif self.state == Scout.Status.Charging and self.battery > 999:
            self.state = Scout.Status.Find
        elif self.state == Scout.Status.Home and not self.finish:
            self.go(self.home)
        elif self.state == Scout.Status.Find and self.finish:
            self.go(Vector2(
                x=random.randint(0, FIELD_WIDTH),
                y=random.randint(0, FIELD_HEIGHT)
            ))
