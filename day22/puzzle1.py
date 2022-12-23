import re
import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

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

    def neighbour(self, f):
        if self.type == ' ': return None
        x, y = self.x, self.y
        while True:
            if f in (FACING_UP, FACING_DOWN):
                y = (y + (1 if f == FACING_DOWN else -1)) % h
            else:
                x = (x + (1 if f == FACING_RIGHT else -1)) % w
            point = board[y][x]
            if point.type != ' ':
                return point

FACING_RIGHT, FACING_DOWN, FACING_LEFT, FACING_UP = range(4)

input_map, input_steps = input.split('\n\n')

lines = input_map.splitlines()
w = max(len(line) for line in lines)
h = len(lines)
board = [[Point(x, y, c) for x, c in enumerate(line.ljust(w))] for y, line in enumerate(lines)]
instructions = [step for step in re.split(r'(\d+)', input_steps) if step.strip()]

facing = FACING_RIGHT
position = next(point for point in board[0] if point.type == '.')

for step in instructions:
    print(step)
    if step == 'R':
        facing = (facing + 1) % 4
    elif step == 'L':
        facing = (facing - 1) % 4
    else:
        step = int(step)
        for i in range(step):
            neighbour = position.neighbour(facing)
            if neighbour.type == '#':
                print('Bumped into a wall')
                break
            position = neighbour
            print(repr(position))

print(repr(position), facing)
solution = (position.y+1) * 1000 + (position.x+1) * 4 + facing

print(solution)