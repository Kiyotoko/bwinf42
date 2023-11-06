"""

"""


class Dimension:
    def __init__(self, dx: int, dy: int, dz: int):
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def volume(self) -> int:
        return self.dx * self.dy * self.dz


box = Dimension(5, 5, 5)

golden = Dimension(1, 1, 1)

quaders = []
quaders += [Dimension(1, 1, 1) for _ in range(4)]
quaders += [Dimension(1, 2, 4) for _ in range(6)]
quaders += [Dimension(2, 2, 3) for _ in range(6)]
