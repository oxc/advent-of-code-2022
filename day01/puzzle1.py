input = open('input').read()
solution = max(sum((int(cal) for cal in elf.strip().splitlines())) for elf in input.split('\n\n'))
print(solution)
