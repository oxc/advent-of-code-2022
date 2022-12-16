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

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

re_line = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

pairs = [
    (Point(m[0], m[1]), Point(m[2], m[3])) for m in (
        tuple(int(c) for c in g) for g in (re_line.match(line).groups() for line in input.splitlines())
    )
]
pairs_with_distance = [(p1, p2, p1.distance(p2)) for p1, p2 in pairs]
min_x = min(p1.x - distance for p1, p2, distance in pairs_with_distance)
max_x = max(p1.x + distance for p1, p2, distance in pairs_with_distance)


def impossible_sensor_spots_in_row(y):
    spots = dict()

    for sensor, beacon in pairs:
        distance = sensor.distance(beacon)
        if not (sensor.y - distance <= y <= sensor.y + distance):
            continue

        for x in range(sensor.x - distance, sensor.x + distance + 1):
            p = Point(x, y)
            if p in spots:
                p = spots[p]
            if sensor.x == x and sensor.y == y:
                p.type = 'S'
            elif beacon.x == x and beacon.y == y:
                p.type = 'B'
            elif sensor.distance(p) <= distance and p.type == '.':
                p.type = '#'
            else:
                continue
            spots[p] = p

    return sum(1 if p.type == '#' else 0 for p in spots.values())


#solution = possible_sensors_in_row(10)
solution = impossible_sensor_spots_in_row(2000000)

print(solution)