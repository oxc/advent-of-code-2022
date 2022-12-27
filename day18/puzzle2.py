import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

cubes = { (x, y, z) for x, y, z in (map(int, line.split(',')) for line in input.splitlines()) }

minx = min(x for x, y, z in cubes)-1
maxx = max(x for x, y, z in cubes)+1
miny = min(y for x, y, z in cubes)-1
maxy = max(y for x, y, z in cubes)+1
minz = min(z for x, y, z in cubes)-1
maxz = max(z for x, y, z in cubes)+1

cubes_reach_outside = set()

def neighbors(cube):
    x, y, z = cube
    result = set()
    for dx, dy, dz in (-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1):
        rx, ry, rz = x + dx, y + dy, z + dz
        if minx <= rx <= maxx and miny <= ry <= maxy and minz <= rz <= maxz:
            result.add((rx, ry, rz))
    return result

# find cubes from the outside
cubes_to_check = set().union(
    { (x, z, y) for x in range(minx, maxx+1) for y in (miny, maxy) for z in (minz, maxz) }).union(
    { (x, z, y) for x in (minx, maxx) for y in range(miny, maxy+1) for z in (minz, maxz) }).union(
    { (x, z, y) for x in (minx, maxx) for y in (miny, maxy) for z in range(minz, maxz+1) })

while cubes_to_check:
    cube = cubes_to_check.pop()
    if cube not in cubes:
        cubes_reach_outside.add(cube)
        cubes_to_check.update(neighbors(cube).difference(cubes_reach_outside))

for z in range(minz, maxz+1):
    print('z =', z)
    print('\n'.join(''.join(
        '#' if (x, y, z) in cubes else '.' if (x, y, z) in cubes_reach_outside else ' ' for x in range(minx, maxx+1)
    ) for y in range(miny, maxy+1)))

solution = sum(len(neighbors(cube).intersection(cubes_reach_outside)) for cube in cubes)

print(solution)