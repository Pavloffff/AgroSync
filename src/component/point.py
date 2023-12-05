from pygame import Vector2


class Point:
    pos: Vector2
    weight: int
    assigned_cnt: int

    def __init__(self, pos, weight):
        self.pos = pos
        self.weight = weight
        self.assigned_cnt = 0   # когда они таску получат увеличивать
