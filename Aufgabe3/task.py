class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other: 'Position') -> 'Position':
        return Position(self.x - other.x, self.y - other.y, self.z - other.z)


class Building:
    def __init__(self, path: str):
        self.fields = [[], []]  # Felder
        self.schedule: list[list['Action']] = [[], [], []]  # Queue mit Aktionen
        with open(path, 'r') as reader:
            self.n, self.m = [int(v) for v in reader.readline().split(' ')]
            for z in range(len(self.fields)):
                for y in range(self.n):
                    self.fields[z].append([])
                    for x in range(self.m):
                        c = Field(Position(x, y, z), reader.read(1))
                        if c.is_start():
                            self.start = c  # Cache für Startfeld
                        self.fields[z][y].append(c)
                    reader.read(1)
                reader.read(1)  # Überspringt '\n'
        if self.start is None:  # Hier sollten wir niemals landen
            raise ValueError()

    def find_fastest(self) -> str:
        Action(building.start).conquer(building)  # Startet Aktionen vom Startfeld
        while True:  # Wiederholt so lange, bis Weg gefunden wurde
            self.schedule.append([])             # -+- Rotiert Queue
            for action in self.schedule.pop(0):  # -+
                if action.target.occupied is None:  # Markiert falls noch nicht markiert wurde
                    action.target.occupied = action.origin
                    action.conquer(building)  # Erstellt Aktionen für anliegende Felder
                if action.target.is_end():  # Beendet falls Zielfeld gefunden
                    return f'({action.get_runtime():3.0f}s) {action.traceback()}'

    def is_inside(self, p: Position) -> bool:
        # Gibt zurück, ob Position im Feld liegt
        return 0 <= p.x < self.m and 0 <= p.y < self.n and 0 <= p.z <= 1

    def is_available(self, p: Position) -> bool:
        # Gibt zurück, ob die Position noch verfügbar ist
        return self.is_inside(p) and self.get_field(p).is_available()

    def get_field(self, p: Position) -> 'Field':
        # Gibt das Feld für die Position zurück
        if self.is_inside(p):
            return self.fields[p.z][p.y][p.x]
        else:
            raise IndexError(f'{p} is not in field!')

    def __str__(self) -> str:
        build = ''
        for z in range(len(self.fields)):
            for y in range(self.n):
                for x in range(self.m):
                    build += self.fields[z][y][x].type
                build += '\n'
            build += '\n'
        return build


class Field:
    def __init__(self, p: Position, t: str):
        if t == '\t':
            raise AssertionError(f'Invalid type for {p}')
        self.p = p  # Aktuelle Position
        self.type = t  # Type des Feldes (Wand, Flur, Start, Ziel)
        self.occupied = None  # Ob das Feld bereits markiert wurde oder nicht

    def is_available(self) -> bool:
        # Gibt zurück, ob dieses Feld verfügbar ist
        return (self.is_floor() or self.is_end()) and self.occupied is None

    def is_floor(self) -> bool:
        # Gibt zurück, ob dieses Feld ein Flur ist
        return self.type == '.'

    def is_start(self) -> bool:
        # Gibt zurück, ob dieses Feld das Startfeld ist
        return self.type == 'A'

    def is_end(self) -> bool:
        # Gibt zurück, ob dieses Feld das Zielfeld ist
        return self.type == 'B'

    def neighbours(self, b: Building) -> list['Field']:
        # Gibt die Liste aller benachbarten Felder zurück
        neighbours = []
        for i in range(-1, 2, 2):
            p_0 = Position(self.p.x + i, self.p.y, self.p.z)
            if b.is_available(p_0):
                neighbours.append(b.get_field(p_0))
            p_1 = Position(self.p.x, self.p.y + i, self.p.z)
            if b.is_available(p_1):
                neighbours.append(b.get_field(p_1))
        return neighbours


class Action:
    def __init__(self, target: Field, origin: 'Action' = None):
        self.target = target
        self.origin = origin

    def conquer(self, b: Building) -> None:
        # Erstellt Aktionen für die angrenzenden Felder
        t = self.target  # Shortcut
        for f in t.neighbours(b):
            b.schedule[0].append(Action(f, origin=self))
        pos = Position(t.p.x, t.p.y, (1, 0)[t.p.z])
        if b.is_available(pos):
            f = b.get_field(pos)
            b.schedule[2].append(Action(f, origin=self))

    def get_action(self) -> str:
        # Stellt diese Aktion dar
        diff = self.target.p - self.origin.target.p
        if diff.x < 0:  # Schöner mit switch/case
            return '<'
        elif diff.x > 0:
            return '>'
        elif diff.y < 0:
            return '^'
        elif diff.y > 0:
            return 'v'
        elif diff.z != 0:
            return '!'
        else:
            raise ValueError()

    def traceback(self) -> str:
        # Rekursives bestimmen des zurückgelegten Weges
        if self.target.is_start():
            return ''
        return self.origin.traceback() + self.get_action()

    def get_runtime(self) -> int:
        # Gibt die Zeit zurück, die für den Weg benötigt wird
        time = 0
        for char in self.traceback():
            if char == '!':
                time += 3
            else:
                time += 1
        return time


building = Building(input('Enter file: '))
print(building)
print('\nResult =', building.find_fastest())
