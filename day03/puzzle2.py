from functools import reduce

input = open('input').read()

def priority(item):
    o = ord(item)
    if o >= ord('a'):
        return o - ord('a') + 1
    return o - ord('A') + 27


rucksacks = list(set(line) for line in input.splitlines())
items = list(
    reduce(lambda acc, rucksack: acc.intersection(rucksack), group).pop()
    for group in (
        rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)
    )
)
solution = sum(priority(item) for item in items)
print(solution)
