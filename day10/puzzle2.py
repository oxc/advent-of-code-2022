import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

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
