import sys
from collections import Counter

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Elf(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = '#'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def move(self, x, y):
        print(f"Elf {self} moves to {x},{y}")
        if x > self.x:
            self.dir = '→'
        elif x < self.x:
            self.dir = '←'
        elif y > self.y:
            self.dir = '↓'
        elif y < self.y:
            self.dir = '↑'
        else:
            self.dir = '#'
        self.x = x
        self.y = y

    def propose_move(self, round, elf_positions):
        self.dir = '#'
        neighbours = [
            elf_positions.get((self.x + x, self.y + y)) for x, y in (
                (-1, -1), (0, -1), (1, -1),
                (-1, 0), (1, 0),
                (-1, 1), (0, 1), (1, 1)
            )
        ]
        if not any(neighbours):
            return None
        NW, N, NE, W, E, SW, S, SE = neighbours
        checks = [
            ((NW, N, NE), (0, -1)),
            ((S, SE, SW), (0, 1)),
            ((W, NW, SW), (-1, 0)),
            ((E, NE, SE), (1, 0)),
        ]
        start = round % 4
        for check in range(start, start+4):
            points, (dx, dy) = checks[check % 4]
            if not any(points):
                return self.x + dx, self.y + dy
        return None

elves = [Elf(x, y)
         for y, line in enumerate(input.splitlines())
         for x, c in enumerate(line)
         if c == '#']

def map_extents():
    return (
        min(elf.x for elf in elves), max(elf.x for elf in elves),
        min(elf.y for elf in elves), max(elf.y for elf in elves)
    )

def print_map(round, elf_positions):
    print(f"== End of Round {round} ==")
    minx, maxx, miny, maxy = map_extents()
    print('\n'.join(
        ''.join(elf.dir if elf else '.'
                for elf in (elf_positions.get((x, y))
                for x in range(minx, maxx+1)
                )) for y in range(miny, maxy+1)
    )+'\n')

elf_positions = None
for round in range(11):
    elf_positions = {(elf.x, elf.y): elf for elf in elves}
    print_map(round, elf_positions)
    proposed_positions = [elf.propose_move(round, elf_positions) for elf in elves]
    if not any(proposed_positions):
        break
    position_count = Counter(proposed_positions)
    print(f"Proposed positions: {[f'{p}x{position_count[p]}' for p in proposed_positions]}")
    for elf, position in zip(elves, proposed_positions):
        if position and position_count[position] == 1:
            elf.move(*position)
else:
    for elf in elves:
        elf.dir = '#'
    print_map(round, elf_positions)

x1, x2, y1, y2 = map_extents()
solution = ((x2 - x1 + 1) * (y2 - y1 + 1)) - len(elves)

print(solution)