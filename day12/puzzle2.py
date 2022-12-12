import sys
input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Point(object):
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.visited = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def can_step_up(self, other):
        return other.h <= self.h + 1

    def __repr__(self):
        return f"({self.x},{self.y})"

E = None

offset = ord('a')
def point(h, x, y):
    global E
    if h == 'E':
        E = Point(x, y, ord('z')-offset)
        return E
    return Point(x, y, ord(h)-offset)

grid = [[point(c, x, y) for x, c in enumerate(line)] for y, line in enumerate(input.splitlines())]
assert E is not None

def grid_width():
    return len(grid[0])

def grid_height():
    return len(grid)

def lower_neighbors(p):
    if p.x > 0:
        l = grid[p.y][p.x-1]
        if l.can_step_up(p): yield l
    if p.y > 0:
        u = grid[p.y-1][p.x]
        if u.can_step_up(p): yield u
    if p.x < grid_width()-1:
        r = grid[p.y][p.x+1]
        if r.can_step_up(p): yield r
    if p.y < grid_height()-1:
        d = grid[p.y+1][p.x]
        if d.can_step_up(p): yield d

def find_shortest_path():
    paths = [[E]]
    while True:
        for path in paths:
            for n in lower_neighbors(path[-1]):
                if n.h == 0:
                    path.reverse()
                    return path
                elif not n.visited:
                    n.visited = True
                    paths.append([*path, n])

path = find_shortest_path()

solution = len(path)

print(solution)
