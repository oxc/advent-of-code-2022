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


