import sys
input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Point(object):
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

grid = [[True]]
H = Point('H')
Ts = [Point(str(knot+1)) for knot in range(9)]
s = Point('s')
rope = [H, *Ts]
points = [*rope, s]

def grid_width():
    return len(grid[0])

def grid_height():
    return len(grid)

def grow_grid_top():
    grid.insert(0, [False] * grid_width())
    for point in points:
        point.y += 1

def grow_grid_left():
    for row in grid:
        row.insert(0, False)
    for point in points:
        point.x += 1

def grow_grid_right():
    for row in grid:
        row.append(False)

def grow_grid_bottom():
    grid.append([False] * grid_width())

def print_grid():
    for y, row in enumerate(grid):
        for x, visited in enumerate(grid[y]):
            for p in points:
                if p.x == x and p.y == y:
                    print(p.name, end = '')
                    break
            else:
                if visited:
                    print('#', end = '')
                else:
                    print('.', end = '')
        print()

commands = ((direction, int(steps)) for (direction, steps) in (line.split() for line in input.splitlines()))

for (direction, steps) in commands:
    print("===", direction, steps, "===")
    for i in range(steps):
        if direction == 'L':
            if H.x == 0:
                grow_grid_left()
            H.x -= 1
        elif direction == 'U':
            if H.y == 0:
                grow_grid_top()
            H.y -= 1
        elif direction == 'R':
            if H.x == grid_width()-1:
                grow_grid_right()
            H.x += 1
        elif direction == 'D':
            if H.y == grid_height()-1:
                grow_grid_bottom()
            H.y += 1

        for (h, t) in zip(rope, Ts):
            xdiff = abs(h.x - t.x)
            ydiff = abs(h.y - t.y)
            if xdiff > 1 or ydiff > 1:
                if xdiff > 1 or (xdiff > 0 and ydiff > 1):
                    t.x += 1 if h.x > t.x else -1
                if ydiff > 1 or (ydiff > 0 and xdiff > 1):
                    t.y += 1 if h.y > t.y else -1
        grid[Ts[-1].y][Ts[-1].x] = True

print_grid()
print()
 
solution = sum(sum(1 if grid[y][x] else 0 for x in range(len(grid[y]))) for y in range(len(grid)))

print(solution)
