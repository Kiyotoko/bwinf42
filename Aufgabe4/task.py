import itertools


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Environment:
    def __init__(self, path: str):
        self.fields: list[list['Block']] = []  # Stapel der Ebenen
        self.sources = []  # Cache der Eingabefelder
        self.results = []  # Cache der Ausgabefelder
        with open(path, 'r') as reader:
            self.n, self.m = [int(v) for v in reader.readline().replace('\n', '').split(' ')]
            for y in range(self.m):
                self.fields.append([])
                types = reader.readline().replace('\n', '').replace('  ', ' ').split(' ')
                # Behebt Probleme in der Dateiformatierung und teilt die Zeile in ihre zugehörigen Typen auf
                last = None  # Cache, um Blöcke miteinander zu verknüpfen
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
        # Deaktiviert alle Blöcke
        for array in self.fields[1:]:
            for field in array:
                field.activated = False

    def reactivate_all(self) -> None:
        # Leitet das Licht von der obersten bis zur untersten Ebene durch
        for array in self.fields[:-1]:
            for field in array:
                field.process_activation()

    def get_header(self) -> str:
        # Gibt den Tabellenkopf zurück
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
        # Gibt die aktuellen Zustände der Eingabe- und Ausgabefelder zurück
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


def white_activation(white: 'Block') -> bool:  # Aktivierungsfunktion für 'W'
    return not (white.is_activated() and white.con.is_activated())


def red_major_activation(red_major: 'Block') -> bool:  # Aktivierungsfunktion für 'R'
    return not red_major.is_activated()


def red_minor_activation(red_minor: 'Block') -> bool:  # Aktivierungsfunktion für 'r'
    return not red_minor.con.is_activated()


def blue_activation(blue: 'Block') -> bool:  # Aktivierungsfunktion für 'B'
    return blue.is_activated()


class Block:
    activation_map = {  # Dictionary weist den Typen der Aktivierungsfunktion zu
        'W': white_activation,
        'R': red_major_activation,
        'r': red_minor_activation,
        'B': blue_activation
    }

    def __init__(self, env: Environment, pos: Position, t: str, con: 'Block' = None):
        self.env = env  # Konstruktion
        self.pos = pos  # Position in der Ebene
        self.con = con  # Verbundener Block
        self.type = t  # Type
        self.activated = False  # Ob der Sensor Licht empfängt oder nicht

    def is_activated(self) -> bool:
        # Gibt zurück, ob der Sensor Licht empfängt
        return self.activated

    def activates(self) -> bool:
        # Stellt fest, ob dieser Block selber andere Sensoren durch Licht aktivieren würde
        func = Block.activation_map.get(self.type)
        if func is None:
            raise ValueError(f'Type : {self.type} ? {self.is_source()}')
        return func(self)

    def process_activation(self):
        # Aktiviert den Block in der darunter liegenden Ebene basierend auf Aktivierungsfunktion und Zustand
        if self.is_empty():
            return
        block = self.env.fields[self.pos.y + 1][self.pos.x]
        if self.is_source():
            block.activated = self.activated
        elif self.requires_connection():
            if self.activates():
                block.activated = True
        else:  # Hier sollten wir nie landen
            raise ValueError(self.type)

    def requires_connection(self) -> bool:
        # Gibt zurück, ob dieser Block mit einem anderen verbunden werden muss. Blöcke, die verbunden sein müssen,
        # müssen auch eine Aktivierungsfunktion haben.
        return self.is_white() or self.is_blue() or self.is_red()

    def is_source(self) -> bool:
        # Gibt zurück, ob dieser Block ein Eingabeblock ist.
        return self.type[0] == 'Q'

    def is_result(self) -> bool:
        # Gibt zurück, ob dieser Block ein Ausgabeblock ist.
        return self.type[0] == 'L'

    def is_white(self) -> bool:
        # Gibt zurück, ob dieser Block ein Weiß ist.
        return self.type[0] == 'W'

    def is_blue(self) -> bool:
        # Gibt zurück, ob dieser Block ein Blau ist.
        return self.type[0] == 'B'

    def is_red(self) -> bool:
        # Gibt zurück, ob dieser Block ein Rot ist.
        return self.type.capitalize()[0] == 'R'

    def is_empty(self) -> bool:
        # Gibt zurück, ob dieser Block ein Leer ist.
        return self.type[0] == 'X'


environment = Environment(input('Please enter file: '))
print(environment)

print(environment.get_header())
for i in itertools.product(range(2), repeat=len(environment.sources)):  # Erstellt Permutation
    environment.deactivate_all()  # Deaktiviert alles
    for j in range(len(environment.sources)):  # Setzt Eingabefelder
        environment.sources[j].activated = i[j] == 1
    environment.reactivate_all()  # Leitet Licht weiter
    print(environment.get_state())  # Gibt Zustand aus
