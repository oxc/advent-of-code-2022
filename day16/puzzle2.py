import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

import re
import functools

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

highest_value = 0

def find_max_pressure(steps, open_valves, actors_states):
    if steps % len(actors_states) == 0:
        actors_states = tuple(sorted(actors_states, key=lambda s: s[0]))
    pressure, path_id = _find_max_pressure(steps, open_valves, actors_states)
    global highest_value
    if pressure > highest_value:
        highest_value = pressure
    if steps == 0:
        print(highest_value, pressure, path_id)
    elif steps < 10:
        print('...', steps, highest_value, pressure, path_id, _find_max_pressure.cache_info())
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
        flow_rate = valves[current_valve][0]
        if flow_rate == 0:
            raise Exception('Should not have selected this valve (flow rate is 0)')
        if current_valve in open_valves:
            raise Exception(f'Should not have selected this valve {current_valve} (already open: {open_valves})')

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
