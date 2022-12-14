import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

AIR = '.'
ROCK = '#'
MOVING_SAND = '+'
RESTING_SAND = 'o'

WILL_FLOW = '~'


class Point(object):
    def __init__(self, x, y, type=AIR):
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


streams = [[Point(int(x), int(y)) for x, y in (xy.strip().split(',') for xy in line.split(' -> '))] for line in
           input.splitlines()]

min_x = min(min(p.x for p in stream) for stream in streams) - 1
max_x = max(max(p.x for p in stream) for stream in streams) + 1
max_y = max(max(p.y for p in stream) for stream in streams) + 4

grid = [[Point(x, y) for x in range(min_x, max_x + 1)] for y in range(max_y + 1)]


def point(x, y):
    return grid[y][x - min_x]


for stream in streams:
    for start, end in zip(stream, stream[1:]):
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                point(x, y).type = ROCK

sand = Point(500, 0, MOVING_SAND)


def print_grid():
    header_len = len(str(max_x))
    header = [str(p.x).rjust(header_len) for p in grid[0]]
    print('\n'.join(''.join(h[i] for h in header) for i in range(header_len)))
    print('\n'.join(''.join(str(sand if sand == p else p) for p in row) for row in grid))


def produce_sand(mark=False):
    global sand
    sand.x = 500
    sand.y = 0

    while sand.y < max_y:
        if mark:
            point(sand.x, sand.y).type = WILL_FLOW
        if point(sand.x, sand.y + 1).type == AIR:
            sand.y += 1
            continue
        if point(sand.x - 1, sand.y + 1).type == AIR:
            sand.x -= 1
            sand.y += 1
            continue
        if point(sand.x + 1, sand.y + 1).type == AIR:
            sand.x += 1
            sand.y += 1
            continue
        point(sand.x, sand.y).type = RESTING_SAND
        return False
    return True

resting_sand = 0
while not produce_sand():
    resting_sand += 1
produce_sand(True)
print_grid()

solution = resting_sand
print(solution)