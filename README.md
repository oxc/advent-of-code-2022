# Advent of Code

My solutions for [Advent of Code 2022](https://adventofcode.com/2022/).


## Day 1 "Calorie Counting"

[[Description]](https://adventofcode.com/2022/day/1) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day01)

<details>
<summary>Puzzle 1</summary>

```python
solution = max(sum((int(cal) for cal in elf.strip().splitlines())) for elf in input.split('\n\n'))
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
cals = list(sum((int(cal) for cal in elf.strip().splitlines())) for elf in input.split('\n\n'))
cals.sort()
solution = sum(cals[-3:])
```
</details>

## Day 2 "Rock Paper Scissors"

[[Description]](https://adventofcode.com/2022/day/2) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day02)

<details>
<summary>Puzzle 1</summary>

```python
scores = {
    "A X": 1+3,
    "B X": 1+0,
    "C X": 1+6,
    "A Y": 2+6,
    "B Y": 2+3,
    "C Y": 2+0,
    "A Z": 3+0,
    "B Z": 3+6,
    "C Z": 3+3,
}

solution = sum(scores[line] for line in input.splitlines() if line)
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
scores = {
    "A X": 3+0,
    "B X": 1+0,
    "C X": 2+0,
    "A Y": 1+3,
    "B Y": 2+3,
    "C Y": 3+3,
    "A Z": 2+6,
    "B Z": 3+6,
    "C Z": 1+6,
}

solution = sum(scores[line] for line in input.splitlines() if line)
```
</details>

## Day 3 "Rucksack Reorganization"

[[Description]](https://adventofcode.com/2022/day/3) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day03)

<details>
<summary>Puzzle 1</summary>

```python
def priority(item):
  ...

items = list(
    set(line[0:int(len(line)/2)])
        .intersection(set(line[int(len(line)/2):]))
        .pop()
    for line in input.splitlines()
)
solution = sum(priority(item) for item in items)
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
rucksacks = list(set(line) for line in input.splitlines())
items = list(
    reduce(lambda acc, rucksack: acc.intersection(rucksack), group).pop()
    for group in (
        rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)
    )
)
solution = sum(priority(item) for item in items)
```
</details>


## Day 4 "Camp Cleanup"

[[Description]](https://adventofcode.com/2022/day/4) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day04)

<details>
<summary>Puzzle 1</summary>

```python
def elf_range(r):
     return range(*(int(i) for i in r.split('-')))

def contains_assignment(a, b):
     return a.start <= b.start and a.stop >= b.stop

pairs = list(
        list(map(elf_range, r.split(',')))
        for r in input.splitlines()
)

solution = len(list(
        pair for pair in pairs
        if contains_assignment(*pair) or contains_assignment(*reversed(pair))
))
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
def assignments_overlap(a, b):
     return a.start <= b.start and a.stop >= b.start

pairs = list(
        list(map(elf_range, r.split(',')))
        for r in input.splitlines()
)

solution = len(list(
        pair for pair in pairs
        if assignments_overlap(*pair) or assignments_overlap(*reversed(pair))
))
```
</details>


## Day 5 "Supply Stacks"

[[Description]](https://adventofcode.com/2022/day/5) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day05)

<details>
<summary>Puzzle 1</summary>

```python
lines = input.splitlines()

stacks = [[] for i in range(0, len(lines[0]), 4)]
while True:
    line = lines.pop(0)
    crates = [line[i:i+3].strip() for i in range(0, len(line), 4)]
    if crates[0] == '1':
        break
    for i, crate in enumerate(crates):
        if crate:
            stacks[i].append(crate.strip('[]'))
lines.pop(0)

for line in lines:
    (amount, src, dst) = map(int, re.match('move (\d+) from (\d+) to (\d+)', line).groups())
    stacks[dst-1][0:0] = reversed(stacks[src-1][0:amount])
    stacks[src-1][0:amount] = []

solution = ''.join((stack[0] for stack in stacks))
```
</details>

<details>
<summary>Puzzle 2</summary>

Remove the `reversed` from puzzle1
</details>

## Day 6 "Tuning Trouble"

[[Description]](https://adventofcode.com/2022/day/6) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day06)

<details>
<summary>Puzzle 1</summary>


```python
def find_marker(input, size):
    for i in range(size, len(input)):
        chars = set(input[i-size:i])
        if len(chars) == size:
            return i

solution = find_marker(input, 4)
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
solution = find_marker(input, 14)
```

(First solution was actually hardcoded to 4 ;)
</details>


## Day 7 "No Space Left On Device"

[[Description]](https://adventofcode.com/2022/day/7) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day07)

<details>
<summary>Puzzle 1</summary>


```python
class Directory(object):
    def __init__(self, name):
        self.name = name
        self.directories = {}
        self.files = {}

    def size(self):
        return sum(
                size for size in self.files.values()
            ) + sum(
                dir.size() for dir in self.directories.values()
            )

    def cd(self, dirName):
        return self.directories.setdefault(dirName, Directory(dirName))

    def collect_dirs(self, acc = []):
        acc.append(self)
        for dir in self.directories.values():
            dir.collect_dirs(acc)
        return acc

def build_filesystem(input):
    root = Directory('/')
    cwd = [root]
    for line in input.splitlines():
        if line.startswith('$'):
            (cmd, arg) = (line.split() + [''])[1:3]
            if cmd == 'cd':
                if arg == '/':
                    cwd = [root]
                elif arg == '..':
                    cwd.pop()
                    if len(cwd) == 0:
                        cwd = [root]
                else:
                    cwd.append(cwd[-1].cd(arg))
            # ignore ls
        else:
            (size, name) = line.split()
            if size == 'dir':
                cwd[-1].cd(name)
            else:
                cwd[-1].files[name] = int(size)
    return root

root = build_filesystem(input)
dirs = root.collect_dirs()
```

```python
solution = sum(size for size in (dir.size() for dir in dirs) if size <= 100000)
```
</details>

<details>
<summary>Puzzle 2</summary>

```python
max_size = 70000000
req_size = 30000000

used_size = root.size()
unused_size = max_size - used_size

diff = req_size - unused_size

sizes = [dir.size() for dir in dirs]
sizes.sort()

solution = next(size for size in sizes if size >= diff)
```
</details>


## Day 8 "Treetop Tree House"

[[Description]](https://adventofcode.com/2022/day/8) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day08)

<details>
<summary>Puzzle 1</summary>


```python
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
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
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

```
</details>


## Day 9 "Rope Bridge"

[[Description]](https://adventofcode.com/2022/day/9) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day09)

<details>
<summary>Puzzle 1</summary>


```python
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

commands = ((direction, int(steps)) for (direction, steps) in (line.split() for line in input.splitlines()))

for (direction, steps) in commands:
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

solution = sum(sum(1 if grid[y][x] else 0 for x in range(len(grid[y]))) for y in range(len(grid)))
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
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

commands = ((direction, int(steps)) for (direction, steps) in (line.split() for line in input.splitlines()))

for (direction, steps) in commands:
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

solution = sum(sum(1 if grid[y][x] else 0 for x in range(len(grid[y]))) for y in range(len(grid)))
```
</details>


## Day 10 "Cathode-Ray Tube"

[[Description]](https://adventofcode.com/2022/day/10) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day10)

<details>
<summary>Puzzle 1</summary>

```python
instructions = [line.split() for line in input.splitlines()]

cycle = 0
x = 1
readings = []

def next_cycle():
    global cycle, x
    cycle += 1
    if cycle % 40 == 20:
        readings.append(cycle * x)


for instruction in instructions:
    command = instruction.pop(0)
    if command == 'noop':
        next_cycle()
        continue
    if command == 'addx':
        arg = int(instruction.pop(0))
        next_cycle()
        next_cycle()
        x += arg
        continue
    raise ValueError("Unknown command: " + command)

solution = sum(readings)
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
instructions = [line.split() for line in input.splitlines()]

cycle = 0
x = 1
lines = [['.' for x in range(40)] for y in range(6)]

def next_cycle():
    global cycle

    pixel = cycle % 40 
    if pixel in range(x-1, x+2):
        line = cycle // 40
        lines[line][pixel] = '#'
    
    cycle += 1

for instruction in instructions:
    command = instruction.pop(0)
    if command == 'noop':
        next_cycle()
        continue
    if command == 'addx':
        arg = int(instruction.pop(0))
        next_cycle()
        next_cycle()
        x += arg
        continue
    raise ValueError("Unknown command: " + command)

solution = '\n'.join(''.join(line) for line in lines)

print(solution)
```
</details>

## Day 11 "Monkey in the Middle"

[[Description]](https://adventofcode.com/2022/day/11) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day11)

<details>
<summary>Puzzle 1</summary>

```python
re_monkey = re.compile(r'''Monkey (?P<monkey>\d+):
\s*Starting items: (?P<items>[\d, ]+)
\s*Operation: new = old (?P<op_operator>[*+/-]) (?P<op_operand>\d+|old)
\s*Test: divisible by (?P<test_operand>\d+)
\s*If true: throw to monkey (?P<target_true>\d+)
\s*If false: throw to monkey (?P<target_false>\d+)''')

class Monkey(object):
    def __init__(self, monkey, items, op_operator, op_operand, test_operand, target_true, target_false):
        self.id = monkey
        self.items = [int(it.strip()) for it in items.split(',')]
        self.op_operator = op_operator
        self.op_operand = 'old' if op_operand == 'old' else int(op_operand)
        self.test_operand = int(test_operand)
        self.target_true = int(target_true)
        self.target_false = int(target_false)

        self.inspected_items = 0

    def turn(self):
        while self.items:
            item = self.items.pop(0)
            self.item(item)

    def item(self, item):
        self.inspected_items += 1
        operand = item if self.op_operand == 'old' else self.op_operand
        if self.op_operator == '*':
            item = item * operand
        elif self.op_operator == '+':
            item = item + operand
        item = item // 3
        if item % self.test_operand == 0:
            target = self.target_true
        else:
            target = self.target_false
        monkeys[target].items.append(item)

monkeys = [Monkey(**re_monkey.match(monkey).groupdict()) for monkey in input.split('\n\n')]

def round(i):
    print('Round', i)
    for monkey in monkeys:
        print(f'Monkey {monkey.id}: {monkey.items}')
        monkey.turn()
    for monkey in monkeys:
        print(f'Monkey {monkey.id} inspected {monkey.inspected_items} items')
        print(f'Monkey {monkey.id}: {monkey.items}')

for i in range(1, 21):
    round(i)

active = sorted((monkey.inspected_items for monkey in monkeys), reverse=True)

solution = active[0] * active[1]
```

</details>

<details>
<summary>Puzzle 2</summary>

Mod % lcm(all possible test operands)

```python
re_monkey = re.compile(r'''Monkey (?P<monkey>\d+):
\s*Starting items: (?P<items>[\d, ]+)
\s*Operation: new = old (?P<op_operator>[*+/-]) (?P<op_operand>\d+|old)
\s*Test: divisible by (?P<test_operand>\d+)
\s*If true: throw to monkey (?P<target_true>\d+)
\s*If false: throw to monkey (?P<target_false>\d+)''')

class Monkey(object):
    def __init__(self, monkey, items, op_operator, op_operand, test_operand, target_true, target_false):
        self.id = monkey
        self.items = [int(it.strip()) for it in items.split(',')]
        self.op_operator = op_operator
        self.op_operand = 'old' if op_operand == 'old' else int(op_operand)
        self.test_operand = int(test_operand)
        self.target_true = int(target_true)
        self.target_false = int(target_false)

        self.inspected_items = 0

    def turn(self):
        while self.items:
            item = self.items.pop(0)
            self.item(item)

    def item(self, item):
        self.inspected_items += 1
        operand = item if self.op_operand == 'old' else self.op_operand
        if self.op_operator == '*':
            item *= operand
        elif self.op_operator == '+':
            item += operand
        item %= lcm
        if item % self.test_operand == 0:
            target = self.target_true
        else:
            target = self.target_false
        monkeys[target].items.append(item)

monkeys = [Monkey(**re_monkey.match(monkey).groupdict()) for monkey in input.split('\n\n')]

lcm = math.lcm(*[monkey.test_operand for monkey in monkeys])

def round(i):
    print('Round', i)
    for monkey in monkeys:
        monkey.turn()
    for monkey in monkeys:
        print(f'Monkey {monkey.id} inspected {monkey.inspected_items} items')

for i in range(1, 10001):
    round(i)

active = sorted((monkey.inspected_items for monkey in monkeys), reverse=True)

solution = active[0] * active[1]
```
</details>



## Day 12 "Hill Climbing Algorithm"

[[Description]](https://adventofcode.com/2022/day/12) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day12)

<details>
<summary>Puzzle 1</summary>

```python
class Point(object):
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.visited = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def can_step_up(self, other):
        return other.h <= self.h + 1

S = None
E = None

offset = ord('a')
def point(h, x, y):
    global S, E
    if h == 'S':
        S = Point(x, y, ord('a')-offset)
        return S
    if h == 'E':
        E = Point(x, y, ord('z')-offset)
        return E
    return Point(x, y, ord(h)-offset)

grid = [[point(c, x, y) for x, c in enumerate(line)] for y, line in enumerate(input.splitlines())]
assert S is not None
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
                if n == S:
                    path.reverse()
                    return path
                elif not n.visited:
                    n.visited = True
                    paths.append([*path, n])

path = find_shortest_path()

solution = len(path)
 ```

</details>

<details>
<summary>Puzzle 2</summary>

```python
class Point(object):
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.visited = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def can_step_up(self, other):
        return other.h <= self.h + 1

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
```
</details>


## Day 13 "Distress Signal"

[[Description]](https://adventofcode.com/2022/day/13) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day13)

<details>
<summary>Puzzle 1</summary>

```python
pairs = [[literal_eval(line) for line in pair.splitlines()] for pair in input.split('\n\n')]

def in_order(a, b):
    if isinstance(a, list):
        if isinstance(b, list):
            for i, j in zip(a,b):
                res = in_order(i,j)
                if res is not None:
                    return res
            return in_order(len(a), len(b))
        return in_order(a, [b])
    if isinstance(b, list):
        return in_order([a], b)
    if a == b:
        return None
    return a < b

solution = sum(i+1 for i, pair in enumerate(pairs) if in_order(*pair))
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
divider1 = [[2]]
divider2 = [[6]]

packets = [literal_eval(line) for line in input.splitlines() if line.strip()] + [divider1, divider2]

def compare(a, b):
    if isinstance(a, list):
        if isinstance(b, list):
            for i, j in zip(a,b):
                res = compare(i,j)
                if res != 0:
                    return res
            return compare(len(a), len(b))
        return compare(a, [b])
    if isinstance(b, list):
        return compare([a], b)
    if a == b:
        return 0
    return -1 if a < b else 1

packet_key = cmp_to_key(compare)

packets.sort(key=packet_key)

decoder1 = packets.index(divider1)+1
decoder2 = packets.index(divider2)+1

solution = decoder1 * decoder2
```
</details>


## Day 14 "Regolith Reservoir"

[[Description]](https://adventofcode.com/2022/day/14) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day14)

<details>
<summary>Puzzle 1</summary>

```python
AIR = '.'
ROCK = '#'
MOVING_SAND = '+'
RESTING_SAND = 'o'

WILL_FLOW = '~'


class Point(object):
    def __init__(self, x, y, type=AIR):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"({self.x},{self.y})"


streams = [[Point(int(x), int(y)) for x, y in (xy.strip().split(',') for xy in line.split(' -> '))] for line in
           input.splitlines()]

min_x = min(min(p.x for p in stream) for stream in streams) - 1
max_x = max(max(p.x for p in stream) for stream in streams) + 1
max_y = max(max(p.y for p in stream) for stream in streams) + 4

grid = [[Point(x, y) for x in range(min_x, max_x + 1)] for y in range(max_y + 1)]


def point(x, y):
    return grid[y][x - min_x]


for stream in streams:
    for start, end in zip(stream, stream[1:]):
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                point(x, y).type = ROCK

sand = Point(500, 0, MOVING_SAND)


def produce_sand(mark=False):
    global sand
    sand.x = 500
    sand.y = 0

    while sand.y < max_y:
        if mark:
            point(sand.x, sand.y).type = WILL_FLOW
        if point(sand.x, sand.y + 1).type == AIR:
            sand.y += 1
            continue
        if point(sand.x - 1, sand.y + 1).type == AIR:
            sand.x -= 1
            sand.y += 1
            continue
        if point(sand.x + 1, sand.y + 1).type == AIR:
            sand.x += 1
            sand.y += 1
            continue
        point(sand.x, sand.y).type = RESTING_SAND
        return False
    return True

resting_sand = 0
while not produce_sand():
    resting_sand += 1
produce_sand(True)

solution = resting_sand
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
AIR = '.'
ROCK = '#'
MOVING_SAND = '+'
RESTING_SAND = 'o'


class Point(object):
    def __init__(self, x, y, type=AIR):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"({self.x},{self.y})"


streams = [[Point(int(x), int(y)) for x, y in (xy.strip().split(',') for xy in line.split(' -> '))] for line in
           input.splitlines()]

max_y = max(max(p.y for p in stream) for stream in streams) + 2

min_x = min(500 - (max_y), min(min(p.x for p in stream) for stream in streams) - 1)
max_x = max(500 + (max_y), max(max(p.x for p in stream) for stream in streams) + 1)

grid = [[Point(x, y) for x in range(min_x, max_x + 1)] for y in range(max_y + 1)]


def point(x, y):
    return grid[y][x - min_x]


streams.append([Point(min_x, max_y), Point(max_x, max_y)])
for stream in streams:
    for start, end in zip(stream, stream[1:]):
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                point(x, y).type = ROCK

sand = Point(500, 0, MOVING_SAND)

def produce_sand(mark=False):
    global sand
    sand.x = 500
    sand.y = 0

    while not point(500, 0).type == RESTING_SAND:
        if point(sand.x, sand.y + 1).type == AIR:
            sand.y += 1
            continue
        if point(sand.x - 1, sand.y + 1).type == AIR:
            sand.x -= 1
            sand.y += 1
            continue
        if point(sand.x + 1, sand.y + 1).type == AIR:
            sand.x += 1
            sand.y += 1
            continue
        point(sand.x, sand.y).type = RESTING_SAND
        return False
    return True


resting_sand = 0
while not produce_sand():
    resting_sand += 1
sand.type = RESTING_SAND

solution = resting_sand
```
</details>

## Day 15 "Beacon Exclusion Zone"

[[Description]](https://adventofcode.com/2022/day/15) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day15)

<details>
<summary>Puzzle 1</summary>

This one is not very efficient :(

```python
class Point(object):
    def __init__(self, x, y, type = '.'):
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

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

re_line = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

pairs = [
    (Point(m[0], m[1]), Point(m[2], m[3])) for m in (
        tuple(int(c) for c in g) for g in (re_line.match(line).groups() for line in input.splitlines())
    )
]
pairs_with_distance = [(p1, p2, p1.distance(p2)) for p1, p2 in pairs]
min_x = min(p1.x - distance for p1, p2, distance in pairs_with_distance)
max_x = max(p1.x + distance for p1, p2, distance in pairs_with_distance)


def impossible_sensor_spots_in_row(y):
    spots = dict()

    for sensor, beacon in pairs:
        distance = sensor.distance(beacon)
        if not (sensor.y - distance <= y <= sensor.y + distance):
            continue

        for x in range(sensor.x - distance, sensor.x + distance + 1):
            p = Point(x, y)
            if p in spots:
                p = spots[p]
            if sensor.x == x and sensor.y == y:
                p.type = 'S'
            elif beacon.x == x and beacon.y == y:
                p.type = 'B'
            elif sensor.distance(p) <= distance and p.type == '.':
                p.type = '#'
            else:
                continue
            spots[p] = p

    return sum(1 if p.type == '#' else 0 for p in spots.values())

solution = impossible_sensor_spots_in_row(2000000)
```

</details>

<details>
<summary>Puzzle 2</summary>

This one is not very efficient :(

```python
class Point(object):
    def __init__(self, x, y, type = '.'):
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

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

re_line = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

pairs = [
    (Point(m[0], m[1]), Point(m[2], m[3])) for m in (
        tuple(int(c) for c in g) for g in (re_line.match(line).groups() for line in input.splitlines())
    )
]
pairs_with_distance = [(p1, p2, p1.distance(p2.x, p2.y)) for p1, p2 in pairs]


def find_free(searchArea = 4000000):
    for y in range(searchArea):
        x = 0
        while x < searchArea:
            for sensor, beacon, distance in pairs_with_distance:
                if sensor.x == x and sensor.y == y:
                    break
                elif beacon.x == x and beacon.y == y:
                    break
                if not (sensor.y - distance <= y <= sensor.y + distance):
                    continue
                y_distance = abs(sensor.y - y)
                x_distance = distance - y_distance
                if sensor.x - x_distance <= x <= sensor.x + x_distance:
                    x = sensor.x + x_distance
                    break
            else:
                return Point(x, y)

            x += 1


free = find_free()
solution = free.x * 4000000 + free.y
```
</details>


## Day 16 "Proboscidea Volcanium"

[[Description]](https://adventofcode.com/2022/day/16) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day16)

<details>
<summary>Puzzle 1</summary>

```python
re_valve = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')


valves = { m[0]: (int(m[1]), set(v.strip() for v in m[2].split(','))) for m in
           (re_valve.match(line).groups() for line in input.splitlines()) }


def find_paths(path, pressure_released, seen_valves_while_moving, open_valves, current_valve):
    minutes_remaining = 30 - len(path)

    if minutes_remaining == 0:
        yield pressure_released
        return

    flow_rate, next_valves = valves[current_valve]
    if flow_rate > 0 and current_valve not in open_valves:
        yield from find_paths(
            [*path, f'open {current_valve}'],
            pressure_released + flow_rate*(minutes_remaining-1),
            set(),
            open_valves.union({current_valve}),
            current_valve
        )

    if minutes_remaining == 1:
        yield pressure_released
        return

    for next_valve in next_valves:
        if next_valve in seen_valves_while_moving:
            continue
        yield from find_paths(
            [*path, f'move to {next_valve}'],
            pressure_released,
            seen_valves_while_moving.union({current_valve}),
            open_valves,
            next_valve
        )

paths = list(set(find_paths([], 0, set(), set(), 'AA')))

paths.sort(reverse=True)

solution = paths[0]
```

</details>

<details>
<summary>Puzzle 2</summary>

This one runs for ages, but at least it should terminate with my resources
(as opposed to previous solution attempts) :D

```python
re_valve = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')


valves = { m[0]: (int(m[1]), set(v.strip() for v in m[2].split(','))) for m in
           (re_valve.match(line).groups() for line in input.splitlines()) }

flow_valves = frozenset({ k for k, v in valves.items() if v[0] > 0 })

def dijkstra(source):
    dist = {}
    prev = {}
    Q = set()
    for vertex in valves.keys():
        dist[vertex] = float('inf')
        prev[vertex] = None
        Q.add(vertex)
    dist[source] = 0

    while Q:
        u = min(Q, key=dist.get)
        Q.remove(u)
        for v in valves[u][1]:
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev

def find_shortest_paths():
    result = {}
    for source in valves.keys():
        dist, prev = dijkstra(source)
        result[source] = { k: None for k in dist.keys() }
        for target in dist.keys():
            u = target
            path = []
            while prev[u] is not None:
                path.insert(0, u)
                u = prev[u]
            result[source][target] = tuple(path)

    return result

shortest_paths = find_shortest_paths()

valve_count = len(flow_valves)

NUM_ACTORS = 2

def find_max_pressure(steps, open_valves, actors_states):
    if steps % len(actors_states) == 0:
        actors_states = tuple(sorted(actors_states, key=lambda s: s[0]))
    pressure, path_id = _find_max_pressure(steps, open_valves, actors_states)
    return pressure, path_id

@functools.lru_cache(maxsize=15000000)
def _find_max_pressure(steps, open_valves, actors_states):
    minutes_elapsed = (steps // len(actors_states))+1
    minutes_remaining = 27 - minutes_elapsed
    actor_id = steps % len(actors_states)

    if minutes_remaining == 0:
        return 0, ''

    pressure_this_step = 0
    if actor_id == 0:
        pressure_this_step = sum(valves[v][0] for v in open_valves)

    if len(open_valves) == valve_count:
        pressure, path_id, path = _find_max_pressure(steps+1, open_valves, actors_states)
        return pressure + pressure_this_step, path_id

    current_valve, next_steps = actors_states[actor_id]
    if next_steps is None:
        results = []

        possible_targets = flow_valves - \
                           open_valves - \
                           { t[-1] for c, t in actors_states if t is not None and len(t) > 0 } - \
                           { c for c, t in actors_states if t is not None and len(t) == 0 }

        for target in sorted(possible_targets, key=lambda v: valves[v][0], reverse=True):
            next_path = shortest_paths[current_valve][target]
            if len(next_path) + 1 > minutes_remaining:
                continue
            new_state = (current_valve, next_path)
            new_states = actors_states[:actor_id] + (new_state,) + actors_states[actor_id + 1:]
            pressure, path_id = find_max_pressure(
                steps,
                open_valves,
                new_states,
            )
            results.append((pressure, path_id))

        if not results:
            pressure, path_id = find_max_pressure(
                steps+1,
                open_valves,
                actors_states,
            )
            return pressure + pressure_this_step, path_id

        return max(results, key=lambda x: x[0])

    if len(next_steps) == 0:
        # open valve and set to None to select next
        new_state = (current_valve, None)
        new_states = actors_states[:actor_id] + (new_state,) + actors_states[actor_id + 1:]

        pressure, path_id = find_max_pressure(
            steps + 1,
            open_valves.union({current_valve}),
            new_states,
        )
        return pressure + pressure_this_step, f':{actor_id}{current_valve}' + path_id

    else:
        next_valve = next_steps[0]
        new_state = (next_valve, next_steps[1:])
        new_states = actors_states[:actor_id] + (new_state,) + actors_states[actor_id + 1:]
        pressure, path_id = find_max_pressure(
            steps + 1,
            open_valves,
            new_states,
        )
        return pressure + pressure_this_step, path_id

solution, solution_path_id = find_max_pressure(0, frozenset(), tuple(('AA', None) for i in range(NUM_ACTORS)))
print(solution_path_id)
print(solution)
```
</details>



## Day 17 "Pyroclastic Flow"

[[Description]](https://adventofcode.com/2022/day/17) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day17)

<details>
<summary>Puzzle 1</summary>

```python
ROCKS = ((
    '####',
), (
    '.#.',
    '###',
    '.#.',
), (
    '..#',
    '..#',
    '###',
), (
    '#',
    '#',
    '#',
    '#',
), (
    '##',
    '##',
))

class Point(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __str__(self):
        return self.type

jetstream = input.strip()
jetindex = -1
def next_jet():
    global jetindex
    jetindex = (jetindex + 1) % len(jetstream)
    return jetstream[jetindex]

chamber = [(Point(0, 0, '+'), *(Point(0, x, '-') for x in range(1, 8)), Point(0, 8, '+'))]

rock = None

def highest_point():
    for row in reversed(chamber):
        if any(point for point in row[1:-1] if point.type != '.'):
            return row[0].y
    return 0

def ensure_height(h):
    while len(chamber) < h:
        y = len(chamber)
        row = (Point(0, y, '|'), *(Point(x, y, '.') for x in range(1, 8)), Point(8, y, '+'))
        chamber.append(row)

def can_move(dx, dy):
    for point in rock:
        x, y = point.x + dx, point.y + dy
        if chamber[y][x].type != '.':
            return False
    return True

def move(dx, dy):
    for point in rock:
        point.x += dx
        point.y += dy

def settle():
    for point in rock:
        chamber[point.y][point.x].type = '#'

def print_chamber():
    return
    print('\n'.join(reversed([
        ''.join('@' if rock and point in rock else point.type for point in row)
        for row in chamber
    ])))

rock_count = 0
while rock_count < 2022:
    if rock is None:
        # new rock appears
        shape = ROCKS[rock_count % len(ROCKS)]
        height = len(shape)
        # increase chamber height
        start_y = highest_point() + height + 3
        ensure_height(start_y + 1)
        rock = tuple(Point(x+3, start_y-y, c) for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#')
        print_chamber()

    dx = 1 if next_jet() == '>' else -1
    if can_move(dx, 0):
        move(dx, 0)
        print_chamber()

    dy = -1
    if can_move(0, dy):
        move(0, dy)
    else:
        settle()
        rock_count += 1
        rock = None
    print_chamber()


solution = highest_point()
p```

</details>

<details>
<summary>Puzzle 2</summary>

Not so happy about this one. Seems like a 350 cycle is too long, and there must be a better way. But maybe there isn't :)

```python
ROCKS = ((
    '####',
), (
    '.#.',
    '###',
    '.#.',
), (
    '..#',
    '..#',
    '###',
), (
    '#',
    '#',
    '#',
    '#',
), (
    '##',
    '##',
))

class Point(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __str__(self):
        return self.type

jetstream = input.strip()
jetindex = -1
def next_jet():
    global jetindex
    jetindex = (jetindex + 1) % len(jetstream)
    return jetstream[jetindex]

rockindex = -1
def next_rock():
    global rockindex
    rockindex = (rockindex + 1) % len(ROCKS)
    return ROCKS[rockindex]

chamber = [(Point(0, 0, '+'), *(Point(x, 0, '-') for x in range(1, 8)), Point(8, 0, '+'))]

rock = None

def highest_point():
    for row in reversed(chamber):
        if any(point for point in row[1:-1] if point.type != '.'):
            return row[0].y
    return 0

def chamber_offset():
    return chamber[0][0].y

def cut_off_chamber():
    def highest(x):
        for row in reversed(chamber):
            if row[x].type != '.':
                return row[x].y
    cut_off_point = min(highest(x) for x in range(1, 8))-1
    cut_off_point -= chamber_offset()
    if cut_off_point > 0:
        del chamber[0:cut_off_point]

def ensure_height(h):
    for y in range(chamber[-1][0].y + 1, h):
        row = (Point(0, y, '|'), *(Point(x, y, '.') for x in range(1, 8)), Point(8, y, '|'))
        chamber.append(row)

def can_move(dx, dy):
    y0 = chamber_offset()
    for point in rock:
        x, y = point.x + dx, point.y + dy
        if chamber[y-y0][x].type != '.':
            return False
    return True

def move(dx, dy):
    for point in rock:
        point.x += dx
        point.y += dy

def settle():
    y0 = chamber_offset()
    for point in rock:
        chamber[point.y-y0][point.x].type = '#'

def run_rocks(target_count):
    global rock
    rock_count = 0
    while rock_count < target_count:
        if rock is None:
            # new rock appears
            shape = next_rock()
            height = len(shape)
            # increase chamber height
            start_y = highest_point() + height + 3
            ensure_height(start_y + 1)
            rock = tuple(Point(x+3, start_y-y, c) for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#')

        dx = 1 if next_jet() == '>' else -1
        if can_move(dx, 0):
            move(dx, 0)

        dy = -1
        if can_move(0, dy):
            move(0, dy)
        else:
            settle()
            rock_count += 1
            rock = None
            cut_off_chamber()

chunk_size = math.lcm(len(ROCKS), len(jetstream))
run_rocks(chunk_size)
first_chunk_height = highest_point()

test_chunks_height = first_chunk_height
test_chunk_heights = []
while True:
    run_rocks(chunk_size)
    previous_height = test_chunks_height
    test_chunks_height = highest_point()
    test_chunk_height = test_chunks_height - previous_height
    test_chunk_heights.append(test_chunk_height)
    if len(test_chunk_heights) > 2 and len(test_chunk_heights) % 2 == 0:
        cycle_len = len(test_chunk_heights) // 2
        if test_chunk_heights[:cycle_len] == test_chunk_heights[cycle_len:]:
            cycle_height = sum(test_chunk_heights[:cycle_len])
            break
target = 1000000000000
cycle_rocks = cycle_len*chunk_size
remaining_rocks = target - 2*cycle_rocks - chunk_size
run_rocks(remaining_rocks % cycle_rocks)
rest_height = highest_point()-(2*cycle_height)-first_chunk_height

solution = highest_point() + (remaining_rocks // cycle_rocks) * cycle_height
```
</details>




## Day 18 ""

[[Description]](https://adventofcode.com/2022/day/18) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day18)

<details>
<summary>Puzzle 1</summary>

```python
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
```
</details>




## Day 19 ""

[[Description]](https://adventofcode.com/2022/day/19) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day19)

<details>
<summary>Puzzle 1</summary>

```python
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
```
</details>




## Day 20 ""

[[Description]](https://adventofcode.com/2022/day/20) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day20)

<details>
<summary>Puzzle 1</summary>

```python
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
```
</details>




## Day 21 "Monkey Math"

[[Description]](https://adventofcode.com/2022/day/21) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day21)

<details>
<summary>Puzzle 1</summary>

```python
class Operation(object):
    def __init__(self, lop, op, rop):
        self.lop = lop
        self.op = op
        self.rop = rop
        self.prev = None
        self.value = None

    def __int__(self):
        if self.value is None:
            if self.op == '+':
                self.value = int(self.lop) + int(self.rop)
            elif self.op == '*':
                self.value = int(self.lop) * int(self.rop)
            elif self.op == '-':
                self.value = int(self.lop) - int(self.rop)
            elif self.op == '/':
                self.value = int(self.lop) // int(self.rop)
        return self.value


class Value(object):
    def __init__(self, value):
        self.value = value
        self.prev = None

    def __int__(self):
        return self.value

expressions = {
    lhs: Value(int(rhs)) if rhs.isdigit() else Operation(*rhs.split()) for lhs, rhs in
    (line.split(': ') for line in input.splitlines())
 }

# build graph
values = []
for expr in expressions.values():
    if isinstance(expr, Operation):
        expr.lop = expressions[expr.lop]
        assert(expr.lop.prev is None)
        expr.lop.prev = expr
        expr.rop = expressions[expr.rop]
        assert(expr.rop.prev is None)
        expr.rop.prev = expr
    else:
        values.append(expr)

# resolve values without triggering (too much) recursion
while values:
    prev = values.pop(0).prev
    if prev is None:
        continue
    int(prev)
    values.append(prev)

root = expressions['root']

solution = int(root)
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
class Operation(object):
    def __init__(self, lop, op, rop):
        self.lop = lop
        self.op = op
        self.rop = rop
        self.prev = None
        self.value = None

    def __int__(self):
        if self.value is None:
            if self.op == '+':
                self.value = int(self.lop) + int(self.rop)
            elif self.op == '*':
                self.value = int(self.lop) * int(self.rop)
            elif self.op == '-':
                self.value = int(self.lop) - int(self.rop)
            elif self.op == '/':
                self.value = int(self.lop) // int(self.rop)
        return self.value

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        if self.op in ('-', '+'):
            return f'({self.lop} {self.op} {self.rop})'
        return f'{self.lop} {self.op} {self.rop}'

class Value(object):
    def __init__(self, value):
        self.value = value
        self.prev = None

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Var(object):
    def __init__(self):
        self.prev = None
        self.value = None

    def __str__(self):
        return 'H'

class Equals(object):
    def __init__(self, lhs, _, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f'{self.lhs} = {self.rhs}'

    def resolve(self):
        if self.rhs.value is None:
            self.lhs, self.rhs = self.rhs, self.lhs
        if isinstance(self.lhs, Var):
            return True

        exp = self.lhs
        if exp.rop.value is None:
            if exp.op in ('*', '+'):
                exp.lop, exp.rop = exp.rop, exp.lop
        if exp.lop.value is None:
            reverse_op = {'*': '/', '/': '*', '+': '-', '-': '+'}[exp.op]
            self.rhs = Operation(self.rhs, reverse_op, exp.rop)
            self.lhs = exp.lop
            int(self.rhs)
        else:
            if exp.op in ('-', '/'):
                self.rhs = Operation(exp.lop, exp.op, self.rhs)
                self.lhs = exp.rop
                int(self.rhs)

expressions = {
    lhs: Equals(*rhs.split()) if lhs == 'root' else Var() if lhs == 'humn' else Value(int(rhs)) if rhs.isdigit() else Operation(*rhs.split()) for lhs, rhs in
    (line.split(': ') for line in input.splitlines())
 }

# build graph
values = []
for expr in expressions.values():
    if isinstance(expr, Operation):
        expr.lop = expressions[expr.lop]
        assert(expr.lop.prev is None)
        expr.lop.prev = expr
        expr.rop = expressions[expr.rop]
        assert(expr.rop.prev is None)
        expr.rop.prev = expr
    elif isinstance(expr, Value):
        values.append(expr)
root = expressions['root']
root.lhs = expressions[root.lhs]
root.rhs = expressions[root.rhs]

# resolve values without triggering (too much) recursion
while values:
    prev = values.pop(0).prev
    if prev is None:
        continue
    if isinstance(prev, Operation):
        # this is part of the tree that needs to be resolved
        if prev.lop.value is None or prev.rop.value is None:
            continue
    int(prev)
    values.append(prev)

print(str(root))
while not root.resolve():
    print(str(root))

solution = int(root.rhs)

```
</details>



