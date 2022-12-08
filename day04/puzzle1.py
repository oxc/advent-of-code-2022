input = open('input').read()

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
print(solution)
