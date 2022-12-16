import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

import re


class Point(object):
    def __init__(self, x, y, type = '.'):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"({self.x},{self.y})"

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

re_line = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

pairs = [
    (Point(m[0], m[1]), Point(m[2], m[3])) for m in (
        tuple(int(c) for c in g) for g in (re_line.match(line).groups() for line in input.splitlines())
    )
]
pairs_with_distance = [(p1, p2, p1.distance(p2.x, p2.y)) for p1, p2 in pairs]


def find_free(searchArea = 4000000):
    for y in range(searchArea):
        x = 0
        while x < searchArea:
            for sensor, beacon, distance in pairs_with_distance:
                if sensor.x == x and sensor.y == y:
                    break
                elif beacon.x == x and beacon.y == y:
                    break
                if not (sensor.y - distance <= y <= sensor.y + distance):
                    continue
                y_distance = abs(sensor.y - y)
                x_distance = distance - y_distance
                if sensor.x - x_distance <= x <= sensor.x + x_distance:
                    x = sensor.x + x_distance
                    break
            else:
                return Point(x, y)

            if x % 40000 == 0:
                print('.', end = '', flush = True)

            x += 1
        if y % 40000 == 0:
            print("Row", y)


free = find_free()
print(repr(free))
solution = free.x * 4000000 + free.y

print(solution)
