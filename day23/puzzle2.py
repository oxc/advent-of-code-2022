import sys
from collections import Counter

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Elf(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def move(self, x, y):
        #print(f"Elf {self} moves to {x},{y}")
        self.x = x
        self.y = y

    def propose_move(self, round, elf_positions):
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
        ''.join('#' if (x, y) in elf_positions else '.'
                for x in range(minx, maxx+1)
                ) for y in range(miny, maxy+1)
    )+'\n')

elf_positions = None
round = 0
while True:
    round += 1
    print(f"Round {round}")
    elf_positions = {(elf.x, elf.y): elf for elf in elves}
    #print_map(round, elf_positions)
    proposed_positions = [elf.propose_move(round-1, elf_positions) for elf in elves]
    if not any(proposed_positions):
        break
    position_count = Counter(proposed_positions)
    for elf, position in zip(elves, proposed_positions):
        if position and position_count[position] == 1:
            elf.move(*position)
print_map(round, elf_positions)

solution = round

print(solution)