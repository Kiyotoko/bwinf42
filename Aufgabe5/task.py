class TourPoint:
    def __init__(self, name: str, year: int, essential: bool, distance: int):
        self.name = name
        self.year = year
        self.essential = essential
        self.distance = distance

    def is_local_equ(self, another: 'TourPoint'):
        # Überprüft, ob zwei Tourpunkte lokal gleich sind (gleicher Ort)
        return self.name == another.name

    def __str__(self):
        return f'{self.name},{self.year},{"X" if self.essential else " "},{self.distance}'


class Tour:
    def __init__(self, path: str):
        with open(path, 'r') as reader:
            self.m = int(reader.readline())
            self.points = []  # Liste aller Punkte, die aktuell in der Tour sind
            self.sequences: list[list[TourPoint]] = [[]]  # Liste aller Sequenzen
            self.distances: dict[str, dict[str, int]] = {}  # Dictionary für die Distanzen zwischen zwei Ortend
            for i in range(self.m):
                args = reader.readline().split(',')
                name, year, essential, distance = args[0], int(args[1]), args[2] == 'X', int(args[3])
                point = TourPoint(name, year, essential, distance)
                self.sequences[len(self.sequences) - 1].append(point)
                if name not in self.distances.keys():
                    self.distances[name] = {}
                if i > 0:
                    previous = self.points[i - 1].name
                    difference = distance - self.points[i - 1].distance
                    self.distances[name][previous] = difference
                    self.distances[previous][name] = difference
                if essential:  # Erstellt neue Sequenz
                    self.sequences.append([point])
                self.points.append(point)

    def __str__(self):
        build = ''
        for point in self.points:
            build += str(point) + '\n'
        return build

    def optimise(self):
        # Hauptmethode zur Optimierung der Tourlänge
        self.find_start()
        for sequence in self.sequences:
            self.shorter(sequence)
        self.reset_distances()

    def get_pairs(self) -> list[tuple[TourPoint, TourPoint]]:
        # Gibt alle Paare von Tourpunkten zurück, die in der ersten und letzten Sequenz vorkommen
        pairs = []
        for i in self.sequences[0]:
            for j in self.sequences[-1]:
                if i.is_local_equ(j):
                    pairs.append((i, j))
        if len(pairs) == 0:
            raise ValueError('No pairs')
        return pairs

    def find_start(self) -> None:
        # Findet den optimalen Startpunkt und Endpunkt der Tour
        if len(self.sequences[0]) == 1 or len(self.sequences[-1]) == 1:
            return
        pairs = self.get_pairs()
        index: int = ...
        distance: int = ...
        for i in range(len(pairs)):
            diff = pairs[i][1].distance - pairs[i][0].distance
            if distance is Ellipsis or diff < distance:
                distance = diff
                index = i
        if index is Ellipsis:
            raise IndexError('Index is Ellipsis')
        for v in self.sequences[0][:self.sequences[0].index(pairs[index][0])]:
            if v in self.points:
                self.points.remove(v)
        for v in self.sequences[-1][self.sequences[-1].index(pairs[index][1])+1:]:
            if v in self.points:
                self.points.remove(v)

    def shorter(self, sequence: list[TourPoint]):
        # Optimiert eine Teilsequenz, indem nicht notwendige Tourpunkte entfernt werden
        size = len(sequence)
        for i in range(0, size, 1):
            if sequence[i] in self.points:
                for j in range(i + 1, size, 1):
                    if sequence[j] in self.points and self.are_connected(sequence[i], sequence[j]):
                        for e in sequence[i+1:j]:
                            if e in self.points:
                                self.points.remove(e)

    def are_connected(self, left: TourPoint, right: TourPoint) -> bool:
        # Überprüft, ob zwei Tourpunkte direkt miteinander verbunden sind
        if left.is_local_equ(right):
            return True
        return left.name in self.distances[right.name].keys()

    def get_distance(self, left: TourPoint, right: TourPoint) -> int:
        # Gibt die Distanz zwischen zwei Tourpunkten zurück
        if left.is_local_equ(right):
            return 0  # Annahme, das Abstand zwischen demselben Ort 0 ist
        try:
            return self.distances[left.name][right.name]
        except KeyError:
            raise ValueError(f'Can not connect {left} and {right}')

    def reset_distances(self):
        # Setzt die Distanzen zwischen den Tourpunkten zurück, um die chronologische Reihenfolge zu gewährleisten
        self.points[0].distance = 0
        for i in range(1, len(self.points)):
            self.points[i].distance = self.points[i-1].distance + self.get_distance(self.points[i-1], self.points[i])


tour = Tour(input('Please enter a file: '))
tour.optimise()
print(tour)
