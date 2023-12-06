from pygame import Vector2


class Point:
    pos: tuple[int, int]
    weight: int
    assigned_cnt: int
    scheduled: bool

    def __init__(self, pos: tuple[int, int], weight: int):
        self.pos = pos
        self.weight = weight
        self.assigned_cnt = 0   # когда они таску получат увеличивать
        self.scheduled = False
