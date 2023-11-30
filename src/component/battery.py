import math
from enum import Enum

from pygame import Vector2


def get_percent(current: int, max_size: int):
    return int(current / max_size * 100)


class Battery:
    class Status(Enum):
        Charging = 1
        Wait = 2
        Move = 3
        EndCharging = 4

    def __init__(self, max_size, move_expense: int, wait_expense: int, charging_increment: int):
        self.max_size = max_size
        self.current = max_size
        self.move_expense = move_expense
        self.wait_expense = wait_expense
        self.charging_increment = charging_increment
        self.state = self.Status.Wait

    def __str__(self):
        return f"{get_percent(self.current, self.max_size)}%"

    def update(self, dt):
        if self.state == self.Status.Move:
            self.current -= self.move_expense * dt
        elif self.state == self.Status.Wait:
            self.current -= self.wait_expense * dt
        elif self.state == self.Status.Charging:
            self.current += self.charging_increment * dt
            if self.current >= self.max_size:
                self.current = self.max_size
                self.state = self.Status.EndCharging

    def predict_move_expense(self, current_pos: Vector2, target_pos: Vector2, speed: int):
        t = math.hypot(current_pos.x - target_pos.x, current_pos.y - target_pos.y) / speed
        return get_percent(self.current - t * self.move_expense, self.max_size)
