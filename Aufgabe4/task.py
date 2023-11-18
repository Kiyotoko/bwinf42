import itertools


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Position':
        return Position(self.x + other.x, self.y + other.y)


class Environment:
    def __init__(self, path: str):
        self.fields: list[list['Block']] = []
        self.sources = []
        self.results = []
        with open(path, 'r') as reader:
            self.n, self.m = [int(v) for v in reader.readline().replace('\n', '').split(' ')]
            for y in range(self.m):
                self.fields.append([])
                types = reader.readline().replace('\n', '').replace('  ', ' ').split(' ')
                last = None
                for x in range(self.n):
                    block = Block(self, Position(x, y), types[x].strip())
                    if block.requires_connection():
                        if last is None:
                            last = block
                        else:
                            block.con = last
                            last.con = block
                            last = None
                    elif block.is_source():
                        self.sources.append(block)
                    elif block.is_result():
                        self.results.append(block)
                    self.fields[y].append(block)

    def deactivate_all(self) -> None:
        for array in self.fields[1:]:
            for field in array:
                field.activated = False

    def reactivate_all(self) -> None:
        for array in self.fields[:-1]:
            for field in array:
                field.process_activation()

    def get_header(self) -> str:
        build = ""
        for source in self.sources:
            build += f'{source.type:<5}'
        build += '|   '
        for result in self.results:
            build += f'{result.type:<5}'
        temp = build
        build += '\n'
        for char in temp:
            build += '+' if char == '|' else '-'
        return build

    def get_state(self) -> str:
        build = ""
        for source in self.sources:
            build += f'{source.activated:<5}'
        build += '|   '
        for result in self.results:
            build += f'{result.activated:<5}'
        return build

    def __str__(self) -> str:
        build = ""
        for array in self.fields:
            for field in array:
                build += f'({field.type:<2}) '
            build += '\n'
        return build


def white_activation(white: 'Block') -> bool:
    return not (white.is_activated() and white.con.is_activated())


def red_major_activation(red_major: 'Block') -> bool:
    return not red_major.is_activated()


def red_minor_activation(red_minor: 'Block') -> bool:
    return not red_minor.con.is_activated()


def blue_activation(blue: 'Block') -> bool:
    return blue.is_activated()


class Block:
    activation_map = {
        'W': white_activation,
        'R': red_major_activation,
        'r': red_minor_activation,
        'B': blue_activation
    }

    def __init__(self, env: Environment, pos: Position, t: str, con: 'Block' = None):
        self.env = env
        self.pos = pos
        self.con = con
        self.type = t
        self.activated = False

    def is_activated(self) -> bool:
        return self.activated

    def activates(self) -> bool:
        func = Block.activation_map.get(self.type)
        if func is None:
            raise ValueError(f'Type : {self.type} ? {self.is_source()}')
        return func(self)

    def process_activation(self):
        if self.is_empty():
            return
        block = self.env.fields[self.pos.y + 1][self.pos.x]
        if self.is_source():
            block.activated = self.activated
        elif self.requires_connection():
            if self.activates():
                block.activated = True
        else:
            raise ValueError(self.type)

    def requires_connection(self) -> bool:
        return self.is_white() or self.is_blue() or self.is_red()

    def is_source(self) -> bool:
        return self.type[0] == 'Q'

    def is_result(self) -> bool:
        return self.type[0] == 'L'

    def is_white(self) -> bool:
        return self.type[0] == 'W'

    def is_blue(self) -> bool:
        return self.type[0] == 'B'

    def is_red(self) -> bool:
        return self.type.capitalize()[0] == 'R'

    def is_empty(self) -> bool:
        return self.type[0] == 'X'


environment = Environment(input('Please enter file: '))
print(environment)

print(environment.get_header())
for i in itertools.product(range(2), repeat=len(environment.sources)):
    environment.deactivate_all()
    for j in range(len(environment.sources)):
        environment.sources[j].activated = i[j] == 1
    environment.reactivate_all()
    print(environment.get_state())
