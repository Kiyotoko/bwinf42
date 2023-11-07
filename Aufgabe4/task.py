class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Position':
        return Position(self.x + other.x, self.y + other.y)


class Environment:
    def __init__(self, path: str):
        self.fields = []
        with open(path, 'r') as reader:
            self.n, self.m = [int(v) for v in reader.readline().split(' ')]
            for y in range(self.m):
                self.fields.append([])
                for x in range(self.n):
                    print(x, y)
                    self.fields[y].append(Block(self, Position(x, y), reader.read(2 if x < self.n - 1 else 1).strip()))
                    reader.read(1)

    def __str__(self):
        build = ""
        for array in self.fields:
            for field in array:
                build += f'({field.type}) '
            build += '\n'
        return build


class Block:

    def __init__(self, env: Environment, pos: Position, t: str):
        self.env = env
        self.pos = pos
        self.type = t
        self.sensor = False
        self.light = False

    def set_sensor(self, sensor: bool) -> None:
        self.sensor = sensor

    def get_light(self) -> bool:
        return self.light

    def is_white(self) -> bool:
        return self.type[0] == 'W'

    def is_blue(self) -> bool:
        return self.type[0] == 'B'

    def is_red(self) -> bool:
        return self.type.capitalize()[0] == 'R'

    def is_empty(self) -> bool:
        return self.type[0] == 'X'

    def get_index(self) -> int:
        return int(self.type[1])


environment = Environment(input("Please enter file: "))
print(environment)
