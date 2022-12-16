import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

import re

re_valve = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')


valves = { m[0]: (int(m[1]), set(v.strip() for v in m[2].split(','))) for m in
           (re_valve.match(line).groups() for line in input.splitlines()) }

print(valves)


def find_paths(path, pressure_released, seen_valves_while_moving, open_valves, current_valve):
    minutes_remaining = 30 - len(path)

    if minutes_remaining == 0:
        #print(minutes_remaining, path, pressure_released)
        #yield path, pressure_released, open_valves
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
print(solution)
