import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

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

print(solution)
