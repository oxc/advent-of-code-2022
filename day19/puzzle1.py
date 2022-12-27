import sys
import re
import copy

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

re_blueprint = re.compile(r'''Blueprint\ (?P<id>\d+):
\ Each\ ore\ robot\ costs\ (?P<ore_robot_ore_price>\d+)\ ore.
\ Each\ clay\ robot\ costs\ (?P<clay_robot_ore_price>\d+)\ ore.
\ Each\ obsidian\ robot\ costs\ (?P<obsidian_robot_ore_price>\d+)\ ore\ and\ (?P<obsidian_robot_clay_price>\d+)\ clay.
\ Each\ geode\ robot\ costs\ (?P<geode_robot_ore_price>\d+)\ ore\ and\ (?P<geode_robot_obsidian_price>\d+)\ obsidian.
''', re.VERBOSE)

class Blueprint(object):
    def __init__(self, id, ore_robot_ore_price, clay_robot_ore_price, obsidian_robot_ore_price, obsidian_robot_clay_price, geode_robot_ore_price, geode_robot_obsidian_price):
        self.id = id
        self.ore_robot_ore_price = ore_robot_ore_price
        self.clay_robot_ore_price = clay_robot_ore_price
        self.obsidian_robot_ore_price = obsidian_robot_ore_price
        self.obsidian_robot_clay_price = obsidian_robot_clay_price
        self.geode_robot_ore_price = geode_robot_ore_price
        self.geode_robot_obsidian_price = geode_robot_obsidian_price

    def __repr__(self):
        return f'Blueprint({self.id}, {self.ore_robot_ore_price}, {self.clay_robot_ore_price}, {self.obsidian_robot_ore_price}+{self.obsidian_robot_clay_price}, {self.geode_robot_ore_price}+{self.geode_robot_obsidian_price})'

blueprints = [
    Blueprint(**{k: int(v) for k, v in re_blueprint.match(line).groupdict().items()}) for
    line in input.splitlines()
]

class Build(object):
    def __init__(self, blueprint):
        self.blueprint = blueprint

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.next_robot = None

    def __hash__(self):
        return hash((self.blueprint, self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots, self.ore, self.clay, self.obsidian, self.geodes, self.next_robot))

    def __eq__(self, other):
        return self.blueprint.id == other.blueprint.id and self.ore_robots == other.ore_robots and self.clay_robots == other.clay_robots and self.obsidian_robots == other.obsidian_robots and self.geode_robots == other.geode_robots and self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geodes == other.geodes and self.next_robot == other.next_robot

    def possible_next_builds(self):
        yield 'ore'
        yield 'clay'
        if self.clay_robots:
            yield 'obsidian'
        if self.obsidian_robots:
            yield 'geode'

    def current_projected_geodes(self, minutes_left):
        return self.geodes + self.geode_robots * minutes_left

    def max_possible_geodes(self, minutes_left):
        return self.current_projected_geodes(minutes_left) + (minutes_left * (minutes_left + 1) // 2)


    def next_build_cost(self):
        if self.next_robot == 'ore':
            return self.blueprint.ore_robot_ore_price, 0, 0
        elif self.next_robot == 'clay':
            return self.blueprint.clay_robot_ore_price, 0, 0
        elif self.next_robot == 'obsidian':
            return self.blueprint.obsidian_robot_ore_price, self.blueprint.obsidian_robot_clay_price, 0
        elif self.next_robot == 'geode':
            return self.blueprint.geode_robot_ore_price, 0, self.blueprint.geode_robot_obsidian_price

    def build(self):
        ore_price, clay_price, obsidian_price = self.next_build_cost()
        if self.ore < ore_price or self.clay < clay_price or self.obsidian < obsidian_price:
            return False
        self.ore -= ore_price
        self.clay -= clay_price
        self.obsidian -= obsidian_price
        return True

    def tick(self, minute, debug=True):
        if self.next_robot is None: raise Exception('No next robot')
        robot_built = self.build()
        if debug: print(f'== Minute {minute} ==')

        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

        if debug: print(f'{self.ore_robots} ore-collecting collect {self.ore_robots} ore. You now have {self.ore} ore.')
        if debug: print(f'{self.clay_robots} clay-collecting collect {self.clay_robots} clay. You now have {self.clay} clay.')
        if debug: print(f'{self.obsidian_robots} obsidian-collecting collect {self.obsidian_robots} obsidian. You now have {self.obsidian} obsidian.')
        if debug: print(f'{self.geode_robots} geode-cracking crack {self.geode_robots} geodes. You now have {self.geodes} geodes.')

        if robot_built:
            if self.next_robot == 'ore':
                self.ore_robots += 1
                if debug: print(f'The new ore-collecting robot is ready; You now have {self.ore_robots} of them.')
            elif self.next_robot == 'clay':
                self.clay_robots += 1
                if debug: print(f'The new clay-collecting robot is ready; You now have {self.clay_robots} of them.')
            elif self.next_robot == 'obsidian':
                self.obsidian_robots += 1
                if debug: print(f'The new obsidian-collecting robot is ready; You now have {self.obsidian_robots} of them.')
            elif self.next_robot == 'geode':
                self.geode_robots += 1
                if debug: print(f'The new geode-cracking robot is ready; You now have {self.geode_robots} of them.')
            self.next_robot = None


def find_best_build(blueprint):
    builds = [Build(blueprint)]
    max_seen = 0
    for minute in range(1, 25):
        minutes_left = 25 - minute
        debug = True
        this_minute_builds = set(builds)
        builds = set()
        print(f'== {len(this_minute_builds)} possible builds ==')
        while this_minute_builds:
            build = this_minute_builds.pop()
            projection = build.current_projected_geodes(minutes_left)
            if projection > max_seen:
                max_seen = projection
                print(f'New max: {max_seen}')
            elif build.max_possible_geodes(minutes_left) < max_seen:
                continue
            if build.next_robot:
                build.tick(minute, debug=debug)
                builds.add(build)
                debug = False
                continue
            else:
                for next_robot in build.possible_next_builds():
                    b = copy.copy(build)
                    b.next_robot = next_robot
                    b.tick(minute, debug=debug)
                    builds.add(b)
                    debug = False
    return max(builds, key=lambda build: build.geodes)


solution = sum(blueprint.id * find_best_build(blueprint).geodes for blueprint in blueprints)
print(solution)
