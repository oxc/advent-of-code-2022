import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Point(object):
    def __init__(self, x, y, type = ' '):
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

class Blizzard(Point):
    def __init__(self, x, y, dir):
        super().__init__(x, y, dir)
        self.dir = dir

    def next_position(self):
        if self.dir in ('>', '<'):
            next_x = self.x + (1 if self.dir == '>' else -1)
            return (next_x % width), self.y
        if self.dir in ('^', 'v'):
            next_y = self.y + (1 if self.dir == 'v' else -1)
            return self.x, (next_y % height)
        raise Exception(f'Invalid direction {self.dir}')

    def move(self):
        self.x, self.y = self.next_position()

class Path(object):
    def __init__(self, head, tail = None):
        self.head = head
        self.tail = tail

    def __len__(self):
        return 1 if self.tail is None else 1 + len(self.tail)

    def __str__(self):
        if self.tail is None:
            return str(self.head)
        return f"{self.tail} -> {self.head}"

lines = [line for line in input.splitlines() if line]
width = len(lines[0])-2
height = len(lines)-2
blizzards = [Blizzard(x, y, c)
         for y, line in enumerate(lines[1:-1])
         for x, c in enumerate(line[1:-1])
         if c in ('>', '<', '^', 'v')]
start = lines[0].index('.')-1, -1
end = lines[-1].index('.')-1, height

def count_blizzards(blizzard_positions=None):
    if blizzard_positions is None:
        blizzard_positions = [(b.x, b.y) for b in blizzards]
    blizz = {}
    for blizzard,p in zip(blizzards, blizzard_positions):
        if p in blizz: blizz[p].append(blizzard)
        else: blizz[p] = [blizzard]
    return blizz

def print_map(paths):
    expeditions = set(path.head for path in paths)
    minute = len(paths[0])-1
    if minute == 0:
        print('Initial state:')
    else:
        print(f'Minute {minute}:')
    blizz = count_blizzards()
    def print_blizzard(x, y):
        b = blizz.get((x, y))
        if b is None: return '.'
        if len(b) == 1: return b[0].dir
        return str(len(b))
    print('\n'.join(
        ''.join(
            '\u001B[47mE\033[0m' if (x, y) in expeditions else
            '.' if (x, y) in (start, end) else
            '#' if x == -1 or y == -1 or x == width or y == height else
            print_blizzard(x, y)
            for x in range(-1, width+1)
        )
        for y in range(-1, height+1)
    ))


def find_first_shortest_path(start, end):
    paths = [Path(start)]

    if start[1] < end[1]:
        moves = ((1, 0), (0, 1), (0,0), (-1, 0), (0, -1))
    else:
        moves = ((-1, 0), (0, -1), (0,0), (1, 0), (0, 1))


    def next_steps(path, next_blizzard_positions):
        cx, cy = path.head
        for (x, y) in moves:
            target = (cx + x, cy + y)
            if not 0 <= target[0] < width or not 0 <= target[1] < height:
                if target not in (start, end):
                    continue
            if target not in next_blizzard_positions:
                yield target

    def distance_to_end(path):
        c = path.head
        return abs(c[0] - end[0]) + abs(c[1] - end[1])

    while True:
        next_blizzard_positions = [blizzard.next_position() for blizzard in blizzards]
        blizz = count_blizzards(next_blizzard_positions)
        current_paths = paths
        current_paths.sort(key=distance_to_end)
        print_map(current_paths)
        paths = []
        heads = set()
        for path in current_paths:
            for step in next_steps(path, blizz):
                if step in heads: continue
                heads.add(step)
                new_path = Path(step, path)
                if step == end:
                    return new_path
                paths.append(new_path)
        for blizzard, next_pos in zip(blizzards, next_blizzard_positions):
            blizzard.x, blizzard.y = next_pos

path_a = find_first_shortest_path(start, end)
path_b = find_first_shortest_path(end, start)
path_c = find_first_shortest_path(start, end)

print(path_a)
print(path_b)
print(path_c)


a = len(path_a)-1
b = len(path_b)-2
c = len(path_c)-2

print(a, b, c)

solution = a + b + c

print(solution)