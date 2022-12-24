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

    def __str__(self):
        return self.type

jetstream = input.strip()
jetindex = -1
def next_jet():
    global jetindex
    jetindex = (jetindex + 1) % len(jetstream)
    return jetstream[jetindex]

chamber = [(Point(0, 0, '+'), *(Point(0, x, '-') for x in range(1, 8)), Point(0, 8, '+'))]

rock = None

def highest_point():
    for row in reversed(chamber):
        if any(point for point in row[1:-1] if point.type != '.'):
            return row[0].y
    return 0

def ensure_height(h):
    while len(chamber) < h:
        y = len(chamber)
        row = (Point(0, y, '|'), *(Point(x, y, '.') for x in range(1, 8)), Point(8, y, '+'))
        chamber.append(row)

def can_move(dx, dy):
    for point in rock:
        x, y = point.x + dx, point.y + dy
        if chamber[y][x].type != '.':
            return False
    return True

def move(dx, dy):
    for point in rock:
        point.x += dx
        point.y += dy

def settle():
    for point in rock:
        chamber[point.y][point.x].type = '#'

def print_chamber():
    return
    print('\n'.join(reversed([
        ''.join('@' if rock and point in rock else point.type for point in row)
        for row in chamber
    ])))

rock_count = 0
while rock_count < 2022:
    if rock is None:
        # new rock appears
        shape = ROCKS[rock_count % len(ROCKS)]
        height = len(shape)
        # increase chamber height
        start_y = highest_point() + height + 3
        ensure_height(start_y + 1)
        rock = tuple(Point(x+3, start_y-y, c) for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#')
        print_chamber()

    dx = 1 if next_jet() == '>' else -1
    if can_move(dx, 0):
        move(dx, 0)
        print_chamber()

    dy = -1
    if can_move(0, dy):
        move(0, dy)
    else:
        settle()
        rock_count += 1
        rock = None
    print_chamber()


solution = highest_point()
print(solution)
