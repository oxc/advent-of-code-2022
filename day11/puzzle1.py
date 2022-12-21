import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

import re

re_monkey = re.compile(r'''Monkey (?P<monkey>\d+):
\s*Starting items: (?P<items>[\d, ]+)
\s*Operation: new = old (?P<op_operator>[*+/-]) (?P<op_operand>\d+|old)
\s*Test: divisible by (?P<test_operand>\d+)
\s*If true: throw to monkey (?P<target_true>\d+)
\s*If false: throw to monkey (?P<target_false>\d+)''')

class Monkey(object):
    def __init__(self, monkey, items, op_operator, op_operand, test_operand, target_true, target_false):
        self.id = monkey
        self.items = [int(it.strip()) for it in items.split(',')]
        self.op_operator = op_operator
        self.op_operand = 'old' if op_operand == 'old' else int(op_operand)
        self.test_operand = int(test_operand)
        self.target_true = int(target_true)
        self.target_false = int(target_false)

        self.inspected_items = 0

    def turn(self):
        while self.items:
            item = self.items.pop(0)
            self.item(item)

    def item(self, item):
        self.inspected_items += 1
        operand = item if self.op_operand == 'old' else self.op_operand
        if self.op_operator == '*':
            item = item * operand
        elif self.op_operator == '+':
            item = item + operand
        item = item // 3
        if item % self.test_operand == 0:
            target = self.target_true
        else:
            target = self.target_false
        monkeys[target].items.append(item)

monkeys = [Monkey(**re_monkey.match(monkey).groupdict()) for monkey in input.split('\n\n')]

def round(i):
    print('Round', i)
    for monkey in monkeys:
        print(f'Monkey {monkey.id}: {monkey.items}')
        monkey.turn()
    for monkey in monkeys:
        print(f'Monkey {monkey.id} inspected {monkey.inspected_items} items')
        print(f'Monkey {monkey.id}: {monkey.items}')

for i in range(1, 21):
    round(i)

active = sorted((monkey.inspected_items for monkey in monkeys), reverse=True)

solution = active[0] * active[1]

print(solution)