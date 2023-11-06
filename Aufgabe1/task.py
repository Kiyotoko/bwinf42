"""
Die Webseite https://www.arukone.bwinf.de/arukone sucht immer die Paare in der Reihenfolge vom
geringsten zum höchsten Wert ab. Dabei wird das Paar genommen, welches die geringste Distanz hat.

```
4
2
2 1 0 0
0 0 0 0
1 2 0 0
0 0 0 0
```
"""

n: int = int(input('Enter dimensions n: '))
p: int = int(input('Enter pairs p: '))

matrix = [[0 for _ in range(n)] for _ in range(n)]
pairs = [1+i for i in range(p)]


class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y


def pretty_print(src: list[list[int]]):
    build = ''
    for i in range(len(src)):
        for v in src[i]:
            build += str(v) + ' '
        build += '\n'
    print(build)


def is_inside(pos: Position):
    return 0 <= pos.x < n and 0 <= pos.y < n


def is_blocked(pos: Position) -> bool:
    if is_inside(pos):
        return get_field(pos) != 0
    return True


def set_field(pos: Position, val: int):
    if is_inside(pos):
        matrix[pos.y][pos.x] = val
    else:
        raise IndexError(f"Position ({pos.y}|{pos.y}) is not in field!")


def get_field(pos: Position) -> int:
    if is_inside(pos):
        return matrix[pos.y][pos.x]
    else:
        raise IndexError(f"Position ({pos.y}|{pos.y}) is not in field!")


v_1, v_2 = pairs.pop(), pairs.pop()
set_field(Position(1, 0), v_1)
set_field(Position(0, 2), v_1)
set_field(Position(0, 0), v_2)
set_field(Position(1, 2), v_2)

print('Matrix')
pretty_print(matrix)
