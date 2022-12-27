import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

cubes = { (x, y, z) for x, y, z in (map(int, line.split(',')) for line in input.splitlines()) }

def neighbors(cube):
    x, y, z = cube
    result = set()
    for dx, dy, dz in (-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1):
        result.add((x + dx, y + dy, z + dz))
    return result

solution = sum(6 - len(cubes.intersection(neighbors(cube))) for cube in cubes)

print(solution)