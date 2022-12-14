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




## Day 18 "Boiling Boulders"

[[Description]](https://adventofcode.com/2022/day/18) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day18)

<details>
<summary>Puzzle 1</summary>

```python
cubes = { (x, y, z) for x, y, z in (map(int, line.split(',')) for line in input.splitlines()) }

def neighbors(cube):
    x, y, z = cube
    result = set()
    for dx, dy, dz in (-1, 0, 0), (0, -1, 0), (0, 0, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1):
        result.add((x + dx, y + dy, z + dz))
    return result

solution = sum(6 - len(cubes.intersection(neighbors(cube))) for cube in cubes)

```

</details>

<details>
<summary>Puzzle 2</summary>

```python
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

solution = sum(len(neighbors(cube).intersection(cubes_reach_outside)) for cube in cubes)
```
</details>




## Day 19 "Not Enough Minerals"

[[Description]](https://adventofcode.com/2022/day/19) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day19)

<details>
<summary>Puzzle 1</summary>

```python
re_blueprint = re.compile(r'''Blueprint\ (?P<id>\d+):
\ Each\ ore\ robot\ costs\ (?P<ore_robot_ore_price>\d+)\ ore.
\ Each\ clay\ robot\ costs\ (?P<clay_robot_ore_price>\d+)\ ore.
\ Each\ obsidian\ robot\ costs\ (?P<obsidian_robot_ore_price>\d+)\ ore\ and\ (?P<obsidian_robot_clay_price>\d+)\ clay.
\ Each\ geode\ robot\ costs\ (?P<geode_robot_ore_price>\d+)\ ore\ and\ (?P<geode_robot_obsidian_price>\d+)\ obsidian.
''', re.VERBOSE)

class Blueprint(object):
    def __init__(self, id, ore_robot_ore_price, clay_robot_ore_price, obsidian_robot_ore_price, obsidian_robot_clay_price, geode_robot_ore_price, geode_robot_obsidian_price):
        self.id = id
        self.ore_robot_ore_price = ore_robot_ore_price
        self.clay_robot_ore_price = clay_robot_ore_price
        self.obsidian_robot_ore_price = obsidian_robot_ore_price
        self.obsidian_robot_clay_price = obsidian_robot_clay_price
        self.geode_robot_ore_price = geode_robot_ore_price
        self.geode_robot_obsidian_price = geode_robot_obsidian_price

    def __repr__(self):
        return f'Blueprint({self.id}, {self.ore_robot_ore_price}, {self.clay_robot_ore_price}, {self.obsidian_robot_ore_price}+{self.obsidian_robot_clay_price}, {self.geode_robot_ore_price}+{self.geode_robot_obsidian_price})'

blueprints = [
    Blueprint(**{k: int(v) for k, v in re_blueprint.match(line).groupdict().items()}) for
    line in input.splitlines()
]

class Build(object):
    def __init__(self, blueprint):
        self.blueprint = blueprint

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.next_robot = None

    def __hash__(self):
        return hash((self.blueprint, self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots, self.ore, self.clay, self.obsidian, self.geodes, self.next_robot))

    def __eq__(self, other):
        return self.blueprint.id == other.blueprint.id and self.ore_robots == other.ore_robots and self.clay_robots == other.clay_robots and self.obsidian_robots == other.obsidian_robots and self.geode_robots == other.geode_robots and self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geodes == other.geodes and self.next_robot == other.next_robot

    def possible_next_builds(self):
        yield 'ore'
        yield 'clay'
        if self.clay_robots:
            yield 'obsidian'
        if self.obsidian_robots:
            yield 'geode'

    def current_projected_geodes(self, minutes_left):
        return self.geodes + self.geode_robots * minutes_left

    def max_possible_geodes(self, minutes_left):
        return self.current_projected_geodes(minutes_left) + (minutes_left * (minutes_left + 1) // 2)


    def next_build_cost(self):
        if self.next_robot == 'ore':
            return self.blueprint.ore_robot_ore_price, 0, 0
        elif self.next_robot == 'clay':
            return self.blueprint.clay_robot_ore_price, 0, 0
        elif self.next_robot == 'obsidian':
            return self.blueprint.obsidian_robot_ore_price, self.blueprint.obsidian_robot_clay_price, 0
        elif self.next_robot == 'geode':
            return self.blueprint.geode_robot_ore_price, 0, self.blueprint.geode_robot_obsidian_price

    def build(self):
        ore_price, clay_price, obsidian_price = self.next_build_cost()
        if self.ore < ore_price or self.clay < clay_price or self.obsidian < obsidian_price:
            return False
        self.ore -= ore_price
        self.clay -= clay_price
        self.obsidian -= obsidian_price
        return True

    def tick(self, minute):
        if self.next_robot is None: raise Exception('No next robot')
        robot_built = self.build()

        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

        if robot_built:
            if self.next_robot == 'ore':
                self.ore_robots += 1
            elif self.next_robot == 'clay':
                self.clay_robots += 1
            elif self.next_robot == 'obsidian':
                self.obsidian_robots += 1
            elif self.next_robot == 'geode':
                self.geode_robots += 1
            self.next_robot = None


def find_best_build(blueprint):
    builds = [Build(blueprint)]
    max_seen = 0
    for minute in range(1, 25):
        minutes_left = 25 - minute
        this_minute_builds = set(builds)
        builds = set()
        while this_minute_builds:
            build = this_minute_builds.pop()
            projection = build.current_projected_geodes(minutes_left)
            if projection > max_seen:
                max_seen = projection
            elif build.max_possible_geodes(minutes_left) < max_seen:
                continue
            if build.next_robot:
                build.tick(minute)
                builds.add(build)
                continue
            else:
                for next_robot in build.possible_next_builds():
                    b = copy.copy(build)
                    b.next_robot = next_robot
                    b.tick(minute)
                    builds.add(b)
                    debug = False
    return max(builds, key=lambda build: build.geodes)


solution = sum(blueprint.id * find_best_build(blueprint).geodes for blueprint in blueprints)
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
re_blueprint = re.compile(r'''Blueprint\ (?P<id>\d+):
\ Each\ ore\ robot\ costs\ (?P<ore_robot_ore_price>\d+)\ ore.
\ Each\ clay\ robot\ costs\ (?P<clay_robot_ore_price>\d+)\ ore.
\ Each\ obsidian\ robot\ costs\ (?P<obsidian_robot_ore_price>\d+)\ ore\ and\ (?P<obsidian_robot_clay_price>\d+)\ clay.
\ Each\ geode\ robot\ costs\ (?P<geode_robot_ore_price>\d+)\ ore\ and\ (?P<geode_robot_obsidian_price>\d+)\ obsidian.
''', re.VERBOSE)

class Blueprint(object):
    def __init__(self, id, ore_robot_ore_price, clay_robot_ore_price, obsidian_robot_ore_price, obsidian_robot_clay_price, geode_robot_ore_price, geode_robot_obsidian_price):
        self.id = id
        self.ore_robot_ore_price = ore_robot_ore_price
        self.clay_robot_ore_price = clay_robot_ore_price
        self.obsidian_robot_ore_price = obsidian_robot_ore_price
        self.obsidian_robot_clay_price = obsidian_robot_clay_price
        self.geode_robot_ore_price = geode_robot_ore_price
        self.geode_robot_obsidian_price = geode_robot_obsidian_price

    def __repr__(self):
        return f'Blueprint({self.id}, {self.ore_robot_ore_price}, {self.clay_robot_ore_price}, {self.obsidian_robot_ore_price}+{self.obsidian_robot_clay_price}, {self.geode_robot_ore_price}+{self.geode_robot_obsidian_price})'

blueprints = [
    Blueprint(**{k: int(v) for k, v in re_blueprint.match(line).groupdict().items()}) for
    line in input.splitlines()[0:3]
]

class Build(object):
    def __init__(self, blueprint):
        self.blueprint = blueprint

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.next_robot = None

    def __hash__(self):
        return hash((self.blueprint, self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots, self.ore, self.clay, self.obsidian, self.geodes, self.next_robot))

    def __eq__(self, other):
        return self.blueprint.id == other.blueprint.id and self.ore_robots == other.ore_robots and self.clay_robots == other.clay_robots and self.obsidian_robots == other.obsidian_robots and self.geode_robots == other.geode_robots and self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geodes == other.geodes and self.next_robot == other.next_robot

    def possible_next_builds(self):
        yield 'ore'
        yield 'clay'
        if self.clay_robots:
            yield 'obsidian'
        if self.obsidian_robots:
            yield 'geode'

    def current_projected_geodes(self, minutes_left):
        return self.geodes + self.geode_robots * minutes_left

    def max_possible_geodes(self, minutes_left):
        return self.current_projected_geodes(minutes_left) + (minutes_left * (minutes_left + 1) // 2)


    def next_build_cost(self):
        if self.next_robot == 'ore':
            return self.blueprint.ore_robot_ore_price, 0, 0
        elif self.next_robot == 'clay':
            return self.blueprint.clay_robot_ore_price, 0, 0
        elif self.next_robot == 'obsidian':
            return self.blueprint.obsidian_robot_ore_price, self.blueprint.obsidian_robot_clay_price, 0
        elif self.next_robot == 'geode':
            return self.blueprint.geode_robot_ore_price, 0, self.blueprint.geode_robot_obsidian_price

    def build(self):
        ore_price, clay_price, obsidian_price = self.next_build_cost()
        if self.ore < ore_price or self.clay < clay_price or self.obsidian < obsidian_price:
            return False
        self.ore -= ore_price
        self.clay -= clay_price
        self.obsidian -= obsidian_price
        return True

    def tick(self, minute):
        if self.next_robot is None: raise Exception('No next robot')
        robot_built = self.build()

        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

        if robot_built:
            if self.next_robot == 'ore':
                self.ore_robots += 1
            elif self.next_robot == 'clay':
                self.clay_robots += 1
            elif self.next_robot == 'obsidian':
                self.obsidian_robots += 1
            elif self.next_robot == 'geode':
                self.geode_robots += 1
            self.next_robot = None


def find_best_build(blueprint, minutes=32):
    builds = [Build(blueprint)]
    max_seen = 0
    for minute in range(1, minutes+1):
        minutes_left = minutes - minute
        this_minute_builds = set(builds)
        builds = set()
        while this_minute_builds:
            build = this_minute_builds.pop()
            projection = build.current_projected_geodes(minutes_left)
            if projection > max_seen:
                max_seen = projection
            elif build.max_possible_geodes(minutes_left) < max_seen:
                continue
            if build.next_robot:
                build.tick(minute)
                builds.add(build)
                continue
            else:
                for next_robot in build.possible_next_builds():
                    b = copy.copy(build)
                    b.next_robot = next_robot
                    b.tick(minute)
                    builds.add(b)
    return max(builds, key=lambda build: build.geodes)


num_geodes = [find_best_build(blueprint).geodes for blueprint in blueprints]

result = 1
for num in num_geodes: result *= num

solution = result
```
</details>




## Day 20 "Grove Positioning System"

[[Description]](https://adventofcode.com/2022/day/20) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day20)

<details>
<summary>Puzzle 1</summary>

```python
class Item(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def set_next(self, item):
        self.next = item
        item.prev = self

    def move_forward(self):
        a, b, c, d = self.prev, self, self.next, self.next.next
        a.set_next(c)
        c.set_next(b)
        b.set_next(d)

    def move_backward(self):
        self.prev.move_forward()


    def find_value(self, value):
        it = self
        while it.value != value:
            it = it.next
        return it

    def find_next(self, i):
        i %= len(items)
        # python does not optimize tail recursion ??\_(???)_/??
        it = self
        while i > 0:
            it = it.next
            i -= 1
        return it

    def to_list(self):
        it = self
        result = []
        while True:
            result.append(it.value)
            it = it.next
            if it is self:
                break
        return result

items = [Item(int(line)) for line in input.splitlines()]
for i in range(len(items)):
    items[i].prev = items[(i - 1) % len(items)]
    items[i].next = items[(i + 1) % len(items)]

def mix():
    for item in items:
        if item.value > 0:
            for _ in range(item.value):
                item.move_forward()
        elif item.value < 0:
            for _ in range(-item.value):
                item.move_backward()


mix()

zero = items[0].find_value(0)

results = [zero.find_next(i).value for i in (1000, 2000, 3000)]

solution = sum(results)
```

</details>

<details>
<summary>Puzzle 2</summary>

Lots of moving. Should've probably jumped directly to the target position, but got it wrong on first try after already having the correct numbers, so ??\_(???)_/??

```python
class Item(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def set_next(self, item):
        self.next = item
        item.prev = self

    def move_forward(self):
        a, b, c, d = self.prev, self, self.next, self.next.next
        a.set_next(c)
        c.set_next(b)
        b.set_next(d)

    def move_backward(self):
        self.prev.move_forward()


    def find_value(self, value):
        it = self
        while it.value != value:
            it = it.next
        return it

    def find_next(self, i):
        i %= len(items)
        # python does not optimize tail recursion ??\_(???)_/??
        it = self
        while i > 0:
            it = it.next
            i -= 1
        return it

    def to_list(self):
        it = self
        result = []
        while True:
            result.append(it.value)
            it = it.next
            if it is self:
                break
        return result

items = [Item(int(line)) for line in input.splitlines()]
for i, item in enumerate(items):
    item.set_next(items[(i + 1) % len(items)])

def mix():
    mod = len(items)-1
    for item in items:
        for _ in range(item.value % mod):
            item.move_forward()

for item in items:
    item.value *= 811589153

zero = items[0].find_value(0)

for _ in range(10):
    mix()

results = [zero.find_next(i).value for i in (1000, 2000, 3000)]

solution = sum(results)
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



## Day 22 "Monkey Map"

[[Description]](https://adventofcode.com/2022/day/22) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day22)

<details>
<summary>Puzzle 1</summary>

```python
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

    def __repr__(self):
        return f"({self.x},{self.y})"

    def neighbour(self, f):
        if self.type == ' ': return None
        x, y = self.x, self.y
        while True:
            if f in (FACING_UP, FACING_DOWN):
                y = (y + (1 if f == FACING_DOWN else -1)) % h
            else:
                x = (x + (1 if f == FACING_RIGHT else -1)) % w
            point = board[y][x]
            if point.type != ' ':
                return point

FACING_RIGHT, FACING_DOWN, FACING_LEFT, FACING_UP = range(4)

input_map, input_steps = input.split('\n\n')

lines = input_map.splitlines()
w = max(len(line) for line in lines)
h = len(lines)
board = [[Point(x, y, c) for x, c in enumerate(line.ljust(w))] for y, line in enumerate(lines)]
instructions = [step for step in re.split(r'(\d+)', input_steps) if step.strip()]

facing = FACING_RIGHT
position = next(point for point in board[0] if point.type == '.')

for step in instructions:
    if step == 'R':
        facing = (facing + 1) % 4
    elif step == 'L':
        facing = (facing - 1) % 4
    else:
        step = int(step)
        for i in range(step):
            neighbour = position.neighbour(facing)
            if neighbour.type == '#':
                print('Bumped into a wall')
                break
            position = neighbour

solution = (position.y+1) * 1000 + (position.x+1) * 4 + facing
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
class Facing(object):
    def __init__(self, value):
        self.value = value
        self.name = ['RIGHT', 'DOWN', 'LEFT', 'UP'][self.value]
        self.short = ['???', '???', '???', '???'][self.value]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        if isinstance(other, Facing):
            other = other.value
        return FACINGS[(self.value + other) % 4]

    def __sub__(self, other):
        if isinstance(other, Facing):
            other = other.value
        return FACINGS[(self.value - other) % 4]

    def opposite(self):
        return self + 2

FACINGS = tuple(Facing(i) for i in range(4))
FACING_RIGHT, FACING_DOWN, FACING_LEFT, FACING_UP = FACINGS

class Point(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)

    def neighbour(self, facing):
        if self.type == ' ': return None
        x, y = self.x, self.y

        if facing in (FACING_UP, FACING_DOWN):
            y = (y + (1 if facing == FACING_DOWN else -1))
        else:
            x = (x + (1 if facing == FACING_RIGHT else -1))
        point = board.get((x, y))
        if point and point.type != ' ':
            return point, facing
        # we stepped of the board, find the right edge
        this_side = sides[self.x // edgelen, self.y // edgelen]
        new_side, new_facing = this_side[facing]

        origin = new_side.origin
        rx, ry = self.x % edgelen, self.y % edgelen

        while facing != new_facing:
            facing += 1
            if facing == FACING_RIGHT:
                rx, ry = 0, rx
            elif facing == FACING_DOWN:
                rx, ry = edgelen-1-ry, 0
            elif facing == FACING_LEFT:
                rx, ry = edgelen-1, rx
            elif facing == FACING_UP:
                rx, ry = edgelen-1-ry, edgelen-1
        return board[origin.x + rx, origin.y + ry], new_facing

side_id = 0
class Side(object):
    def __init__(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin
        if origin.type != ' ':
            global side_id
            side_id += 1
            self.id = side_id
        else:
            self.id = None
        self.neighbors = [None, None, None, None]

    def __getitem__(self, item):
        return self.neighbors[item.value]

    def __setitem__(self, key, value):
        side, direction = value
        if self[key] is not None:
            eside, edir = self[key]
        self.neighbors[key.value] = value
        side.neighbors[direction.opposite().value] = self, key.opposite()

input_map, input_steps = input.split('\n\n')

lines = input_map.splitlines()
w = max(len(line) for line in lines)
h = len(lines)
points = [Point(x   , y, c) for y, line in enumerate(lines) for x, c in enumerate(line.ljust(w)) if c != ' ']
board = {(p.x,p.y): p for p in points}
instructions = [step for step in re.split(r'(\d+)', input_steps) if step.strip()]

edgelen = 50 if len(sys.argv) == 1 else 4

sides = {(x,y): Side(x, y, c) for (x, y, c) in
         ((x, y, board.get((x*edgelen, y*edgelen)))
            for y in range(h // edgelen)
            for x in range(w // edgelen)
          ) if c}

# fold the cube
while any(s is None for side in sides.values() for s in side.neighbors):
    for c in sides.values():
        if c[FACING_RIGHT] is None:
            right = sides.get((c.x+1, c.y))
            if right:
                c[FACING_RIGHT] = right, FACING_RIGHT
        if c[FACING_DOWN] is None:
            bottom = sides.get((c.x, c.y+1))
            if bottom:
                c[FACING_DOWN] = bottom, FACING_DOWN
        if c[FACING_LEFT] and c[FACING_DOWN]:
            left, left_dir = c[FACING_LEFT]
            down, down_dir = c[FACING_DOWN]
            down[down_dir+1] = left, left_dir+1
        if c[FACING_RIGHT] and c[FACING_DOWN]:
            right, right_dir = c[FACING_RIGHT]
            down, down_dir = c[FACING_DOWN]
            right[right_dir+1] = down, down_dir+1
        if c[FACING_RIGHT] and c[FACING_UP]:
            right, right_dir = c[FACING_RIGHT]
            up, up_dir = c[FACING_UP]
            right[right_dir-1] = up, up_dir-1
        if c[FACING_LEFT] and c[FACING_UP]:
            left, left_dir = c[FACING_LEFT]
            up, up_dir = c[FACING_UP]
            up[up_dir-1] = left, left_dir-1

facing = FACING_RIGHT
position = next(point for point in points if point.type == '.')

for step in instructions:
    if step == 'R':
        facing += 1
    elif step == 'L':
        facing -= 1
    else:
        step = int(step)
        for i in range(step):
            new_position, new_facing = position.neighbour(facing)
            if new_position.type == '#':
                break
            position = new_position
            facing = new_facing

solution = (position.y+1) * 1000 + (position.x+1) * 4 + facing.value
```
</details>



## Day 23 "Unstable Diffusion"

[[Description]](https://adventofcode.com/2022/day/23) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day23)

<details>
<summary>Puzzle 1</summary>

```python
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

elf_positions = None
for round in range(11):
    elf_positions = {(elf.x, elf.y): elf for elf in elves}
    proposed_positions = [elf.propose_move(round, elf_positions) for elf in elves]
    if not any(proposed_positions):
        break
    position_count = Counter(proposed_positions)
    for elf, position in zip(elves, proposed_positions):
        if position and position_count[position] == 1:
            elf.move(*position)

x1, x2, y1, y2 = map_extents()
solution = ((x2 - x1 + 1) * (y2 - y1 + 1)) - len(elves)
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
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

elf_positions = None
round = 0
while True:
    round += 1
    elf_positions = {(elf.x, elf.y): elf for elf in elves}
    proposed_positions = [elf.propose_move(round-1, elf_positions) for elf in elves]
    if not any(proposed_positions):
        break
    position_count = Counter(proposed_positions)
    for elf, position in zip(elves, proposed_positions):
        if position and position_count[position] == 1:
            elf.move(*position)

solution = round
```
</details>


## Day 24 "Blizzard Basin"

[[Description]](https://adventofcode.com/2022/day/24) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day24)

<details>
<summary>Puzzle 1</summary>

```python
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

def next_steps(path, next_blizzard_positions):
    cx, cy = path.head
    for (x, y) in ((1, 0), (0, 1), (0,0), (-1, 0), (0, -1)):
        target = (cx + x, cy + y)
        if not 0 <= target[0] < width or not 0 <= target[1] < height:
            if target not in (start, end):
                continue
        if target not in next_blizzard_positions:
            yield target

def distance_to_end(path):
    c = path.head
    return abs(c[0] - end[0]) + abs(c[1] - end[1])
def find_first_shortest_path():
    paths = [Path(start)]
    while True:
        next_blizzard_positions = [blizzard.next_position() for blizzard in blizzards]
        blizz = count_blizzards(next_blizzard_positions)
        current_paths = paths
        current_paths.sort(key=distance_to_end)
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

shortest_path = find_first_shortest_path()

solution = len(shortest_path)-1
```

</details>

<details>
<summary>Puzzle 2</summary>

```python
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

a = len(path_a)-1
b = len(path_b)-2
c = len(path_c)-2

print(a, b, c)

solution = a + b + c
```
</details>


## Day 25 "Full of Hot Air"

[[Description]](https://adventofcode.com/2022/day/24) |
[[Solutions]](https://github.com/oxc/advent-of-code-2022/tree/main/day24)

<details>
<summary>Puzzle 1</summary>

```python
def snafu_to_number(snafu):
    digits = [-2 if c == '=' else -1 if c == '-' else int(c) for c in snafu]
    return sum(d * 5 ** i for i, d in enumerate(reversed(digits)))

def number_to_snafu(number):
    if number == 0:
        return '0'
    inverse_digits = []
    while number:
        inverse_digits.append(number % 5)
        number //= 5
    snagits = []
    acc = 0
    for digit in inverse_digits:
        digit += acc
        acc = 0
        if digit in (0, 1, 2):
            snagits.append(digit)
        else:
            snagits.append(digit - 5)
            acc = 1
    if acc:
        snagits.append(acc)
    snagits.reverse()
    return ''.join('=' if d == -2 else '-' if d == -1 else str(d) for d in snagits)

numbers = [snafu_to_number(snafu) for snafu in input.splitlines()]

needed_fuel = sum(numbers)

solution = number_to_snafu(needed_fuel)
```
</details>


