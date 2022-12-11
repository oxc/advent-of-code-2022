input = open('input').read()

class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0

grid = [[True]]
H = Point()
T = Point()
s = Point()

def grid_width():
    return len(grid[0])

def grid_height():
    return len(grid)

def grow_grid_top():
    grid.insert(0, [False] * grid_width())
    for point in (H, T, s):
        point.y += 1

def grow_grid_left():
    for row in grid:
        row.insert(0, False)
    for point in (H, T, s):
        point.x += 1

def grow_grid_right():
    for row in grid:
        row.append(False)

def grow_grid_bottom():
    grid.append([False] * grid_width())

def print_grid():
    for y, row in enumerate(grid):
        for x, visited in enumerate(grid[y]):
            if H.x == x and H.y == y:
                print('H', end = '')
            elif T.x == x and T.y == y:
                print('T', end = '')
            elif s.x == x and s.y == y:
                print('s', end = '')
            elif visited:
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

        xdiff = abs(H.x - T.x)
        ydiff = abs(H.y - T.y)
        if xdiff > 1 or ydiff > 1:
            if xdiff > 1 or (xdiff > 0 and ydiff > 1):
                T.x += 1 if H.x > T.x else -1
            if ydiff > 1 or (ydiff > 0 and xdiff > 1):
                T.y += 1 if H.y > T.y else -1
        grid[T.y][T.x] = True

           
print_grid()
print()
 
solution = sum(sum(1 if grid[y][x] else 0 for x in range(len(grid[y]))) for y in range(len(grid)))

print(solution)
