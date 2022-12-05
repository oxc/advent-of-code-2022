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
