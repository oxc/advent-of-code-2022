import math
import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

ROCKS = ((
    '####',
), (
    '.#.',
    '###',
    '.#.',
), (
    '..#',
    '..#',
    '###',
), (
    '#',
    '#',
    '#',
    '#',
), (
    '##',
    '##',
))

class Point(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __str__(self):
        return self.type

jetstream = input.strip()
jetindex = -1
def next_jet():
    global jetindex
    jetindex = (jetindex + 1) % len(jetstream)
    return jetstream[jetindex]

rockindex = -1
def next_rock():
    global rockindex
    rockindex = (rockindex + 1) % len(ROCKS)
    return ROCKS[rockindex]

chamber = [(Point(0, 0, '+'), *(Point(x, 0, '-') for x in range(1, 8)), Point(8, 0, '+'))]

rock = None

def highest_point():
    for row in reversed(chamber):
        if any(point for point in row[1:-1] if point.type != '.'):
            return row[0].y
    return 0

def chamber_offset():
    return chamber[0][0].y

def cut_off_chamber():
    def highest(x):
        for row in reversed(chamber):
            if row[x].type != '.':
                return row[x].y
    cut_off_point = min(highest(x) for x in range(1, 8))-1
    cut_off_point -= chamber_offset()
    if cut_off_point > 0:
        del chamber[0:cut_off_point]

def ensure_height(h):
    for y in range(chamber[-1][0].y + 1, h):
        row = (Point(0, y, '|'), *(Point(x, y, '.') for x in range(1, 8)), Point(8, y, '|'))
        chamber.append(row)

def can_move(dx, dy):
    y0 = chamber_offset()
    for point in rock:
        x, y = point.x + dx, point.y + dy
        if chamber[y-y0][x].type != '.':
            return False
    return True

def move(dx, dy):
    for point in rock:
        point.x += dx
        point.y += dy

def settle():
    y0 = chamber_offset()
    for point in rock:
        chamber[point.y-y0][point.x].type = '#'

def print_chamber():
    print(draw_chamber())

def draw_chamber():
    return '\n' + '\n'.join(reversed([
        ''.join('@' if rock and point in rock else point.type for point in row)
        for row in chamber
    ]))

def run_rocks(target_count):
    global rock
    rock_count = 0
    while rock_count < target_count:
        if rock is None:
            # new rock appears
            shape = next_rock()
            height = len(shape)
            # increase chamber height
            start_y = highest_point() + height + 3
            ensure_height(start_y + 1)
            rock = tuple(Point(x+3, start_y-y, c) for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#')

        dx = 1 if next_jet() == '>' else -1
        if can_move(dx, 0):
            move(dx, 0)

        dy = -1
        if can_move(0, dy):
            move(0, dy)
        else:
            settle()
            rock_count += 1
            rock = None
            cut_off_chamber()

chunk_size = math.lcm(len(ROCKS), len(jetstream))
print(f"chunk_size = {chunk_size}")
run_rocks(chunk_size)
first_chunk_height = highest_point()

test_chunks_height = first_chunk_height
test_chunk_heights = []
while True:
    run_rocks(chunk_size)
    previous_height = test_chunks_height
    test_chunks_height = highest_point()
    test_chunk_height = test_chunks_height - previous_height
    test_chunk_heights.append(test_chunk_height)
    print(f"test_chunk_heights[{len(test_chunk_heights)}] = {test_chunk_heights[-1]}")
    if len(test_chunk_heights) > 2 and len(test_chunk_heights) % 2 == 0:
        cycle_len = len(test_chunk_heights) // 2
        if test_chunk_heights[:cycle_len] == test_chunk_heights[cycle_len:]:
            cycle_height = sum(test_chunk_heights[:cycle_len])
            print(f"cycle_len = {cycle_len}")
            break
target = 1000000000000
cycle_rocks = cycle_len*chunk_size
remaining_rocks = target - 2*cycle_rocks - chunk_size
run_rocks(remaining_rocks % cycle_rocks)
rest_height = highest_point()-(2*cycle_height)-first_chunk_height

print(first_chunk_height, cycle_len, cycle_rocks, test_chunk_heights, rest_height)

solution = highest_point() + (remaining_rocks // cycle_rocks) * cycle_height

print(solution)
