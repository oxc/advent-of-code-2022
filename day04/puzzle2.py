input = open('input').read()

def elf_range(r):
     return range(*(int(i) for i in r.split('-')))

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
print(solution)
