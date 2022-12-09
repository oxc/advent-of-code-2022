input = open('input').read()

grid = [list(s) for s in input.splitlines()]

def check_score(tree_x, tree_y):
    height = grid[tree_y][tree_x]
    left = reversed(grid[tree_y][0:tree_x])
    right = grid[tree_y][tree_x+1:]
    top = (grid[y][tree_x] for y in range(tree_y-1, -1, -1))
    bottom = (grid[y][tree_x] for y in range(tree_y+1, len(grid)))
    score = 1
    for path in (left, right, top, bottom):
        factor = 0
        for tree in path:
            factor += 1
            if tree >= height:
                break
        score *= factor
    return score

solution = max(max(check_score(x,y) for x in range(len(grid[y]))) for y in range(len(grid)))

print(solution)
