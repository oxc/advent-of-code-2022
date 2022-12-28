import itertools
import re
import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Facing(object):
    def __init__(self, value):
        self.value = value
        self.name = ['RIGHT', 'DOWN', 'LEFT', 'UP'][self.value]
        self.short = ['→', '↓', '←', '↑'][self.value]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        if isinstance(other, Facing):
            other = other.value
        return FACINGS[(self.value + other) % 4]

    def __sub__(self, other):
        if isinstance(other, Facing):
            other = other.value
        return FACINGS[(self.value - other) % 4]

    def opposite(self):
        return self + 2

FACINGS = tuple(Facing(i) for i in range(4))
FACING_RIGHT, FACING_DOWN, FACING_LEFT, FACING_UP = FACINGS

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

    def __repr__(self):
        return f"({self.x},{self.y})"

    def neighbour(self, facing):
        if self.type == ' ': return None
        x, y = self.x, self.y

        if facing in (FACING_UP, FACING_DOWN):
            y = (y + (1 if facing == FACING_DOWN else -1))
        else:
            x = (x + (1 if facing == FACING_RIGHT else -1))
        point = board.get((x, y))
        if point and point.type != ' ':
            return point, facing
        # we stepped of the board, find the right edge
        this_side = sides[self.x // edgelen, self.y // edgelen]
        new_side, new_facing = this_side[facing]
        print(f'Stepped off the board at {this_side} facing {facing}, landing at side {new_side} facing {new_facing}')

        origin = new_side.origin
        rx, ry = self.x % edgelen, self.y % edgelen

        while facing != new_facing:
            facing += 1
            if facing == FACING_RIGHT:
                rx, ry = 0, rx
            elif facing == FACING_DOWN:
                rx, ry = edgelen-1-ry, 0
            elif facing == FACING_LEFT:
                rx, ry = edgelen-1, rx
            elif facing == FACING_UP:
                rx, ry = edgelen-1-ry, edgelen-1
        return board[origin.x + rx, origin.y + ry], new_facing

side_id = 0
class Side(object):
    def __init__(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin
        if origin.type != ' ':
            global side_id
            side_id += 1
            self.id = side_id
        else:
            self.id = None
        self.neighbors = [None, None, None, None]

    def __getitem__(self, item):
        return self.neighbors[item.value]

    def __setitem__(self, key, value):
        side, direction = value
        if self[key] is not None:
            eside, edir = self[key]
            if eside is not side or edir is not direction:
                raise Exception(f'Edge {key} of {self.id} already set to {eside.id} in direction {edir}, got new {side.id} in direction {direction}')
        self.neighbors[key.value] = value
        side.neighbors[direction.opposite().value] = self, key.opposite()

    def __str__(self):
        return str(self.id)

    def print(self):
        def id(s):
            if s is None: return ' ? '
            return f'{s[1].short}{s[0].id}{s[1].short}'
        return (f'{id(self[FACING_UP]):^9}',
            f'{id(self[FACING_LEFT])}({self.id}){id(self[FACING_RIGHT])}',
            f'{id(self[FACING_DOWN]):^9}')


input_map, input_steps = input.split('\n\n')

lines = input_map.splitlines()
w = max(len(line) for line in lines)
h = len(lines)
points = [Point(x   , y, c) for y, line in enumerate(lines) for x, c in enumerate(line.ljust(w)) if c != ' ']
board = {(p.x,p.y): p for p in points}
instructions = [step for step in re.split(r'(\d+)', input_steps) if step.strip()]

edgelen = 50 if len(sys.argv) == 1 else 4

sides = {(x,y): Side(x, y, c) for (x, y, c) in
         ((x, y, board.get((x*edgelen, y*edgelen)))
            for y in range(h // edgelen)
            for x in range(w // edgelen)
          ) if c}

# fold the cube
while any(s is None for side in sides.values() for s in side.neighbors):
    for c in sides.values():
        if c[FACING_RIGHT] is None:
            right = sides.get((c.x+1, c.y))
            if right:
                c[FACING_RIGHT] = right, FACING_RIGHT
        if c[FACING_DOWN] is None:
            bottom = sides.get((c.x, c.y+1))
            if bottom:
                c[FACING_DOWN] = bottom, FACING_DOWN
        if c[FACING_LEFT] and c[FACING_DOWN]:
            left, left_dir = c[FACING_LEFT]
            down, down_dir = c[FACING_DOWN]
            down[down_dir+1] = left, left_dir+1
        if c[FACING_RIGHT] and c[FACING_DOWN]:
            right, right_dir = c[FACING_RIGHT]
            down, down_dir = c[FACING_DOWN]
            right[right_dir+1] = down, down_dir+1
        if c[FACING_RIGHT] and c[FACING_UP]:
            right, right_dir = c[FACING_RIGHT]
            up, up_dir = c[FACING_UP]
            right[right_dir-1] = up, up_dir-1
        if c[FACING_LEFT] and c[FACING_UP]:
            left, left_dir = c[FACING_LEFT]
            up, up_dir = c[FACING_UP]
            up[up_dir-1] = left, left_dir-1

slines = [
    [sides.get((x,y)) for x in range(w // edgelen)]
    for y in range(h // edgelen)
]
print('\n\n'.join(
    '\n'.join(' '.join(side.print()[i] if side else ' '*9 for side in row) for i in range(3))
for row in slines))

facing = FACING_RIGHT
position = next(point for point in points if point.type == '.')

for step in instructions:
    print(step)
    if step == 'R':
        facing += 1
    elif step == 'L':
        facing -= 1
    else:
        step = int(step)
        for i in range(step):
            new_position, new_facing = position.neighbour(facing)
            if new_position.type == '#':
                print('Bumped into a wall')
                break
            position = new_position
            facing = new_facing
            print(repr(position), facing)

print(repr(position), facing)
solution = (position.y+1) * 1000 + (position.x+1) * 4 + facing.value

print(solution)
