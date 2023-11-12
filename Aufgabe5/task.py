
class Tour:
    def __init__(self, path: str):
        with open(path, 'r') as reader:
            self.m = int(reader.readline())
            self.points = []
            self.buildings = {}
            for _ in range(self.m):
                args = reader.readline()
                name, year, distance = args[0], int(args[1]), int(args[3])
                associated = self.buildings.get(name)
                if associated is None:
                    associated = TourBuilding(name)
                    self.buildings[name] = associated
                associated.years.append(year)
                
                self.points.append(TourPoint(name, year, args[2] == 'X', distance))


class TourPoint:
    def __init__(self, name: str, year: int, essential: bool, distance: int):
        self.name = name
        self.year = year
        self.essential = essential
        self.distance = distance


class TourBuilding:
    def __init__(self, name: str):
        self.name = name
        self.years = []
        self.neighbors = {}
    ...  # FIXME
