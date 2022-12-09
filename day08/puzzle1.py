input = open('input').read()

grid = [list(s) for s in input.splitlines()]

def check_visible(tree_x, tree_y):
    height = grid[tree_y][tree_x]
    left = grid[tree_y][0:tree_x]
    right = grid[tree_y][tree_x+1:]
    top = (grid[y][tree_x] for y in range(0, tree_y))
    bottom = (grid[y][tree_x] for y in range(tree_y+1, len(grid)))
    for path in (left, right, top, bottom):
        if all(otherHeight < height for otherHeight in path):
            return True
    return False

solution = sum(sum(1 if check_visible(x,y) else 0 for x in range(len(grid[y]))) for y in range(len(grid)))

print(solution)
