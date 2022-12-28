import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Item(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def set_next(self, item):
        self.next = item
        item.prev = self

    def move_forward(self):
        a, b, c, d = self.prev, self, self.next, self.next.next
        a.set_next(c)
        c.set_next(b)
        b.set_next(d)

    def move_backward(self):
        self.prev.move_forward()


    def find_value(self, value):
        it = self
        while it.value != value:
            it = it.next
        return it

    def find_next(self, i):
        i %= len(items)
        # python does not optimize tail recursion ¯\_(ツ)_/¯
        it = self
        while i > 0:
            it = it.next
            i -= 1
        return it

    def to_list(self):
        it = self
        result = []
        while True:
            result.append(it.value)
            it = it.next
            if it is self:
                break
        return result

items = [Item(int(line)) for line in input.splitlines()]
for i, item in enumerate(items):
    item.set_next(items[(i + 1) % len(items)])

def mix():
    mod = len(items)-1
    for item in items:
        for _ in range(item.value % mod):
            item.move_forward()

for item in items:
    item.value *= 811589153

zero = items[0].find_value(0)

for _ in range(10):
    mix()

results = [zero.find_next(i).value for i in (1000, 2000, 3000)]

print(results)

solution = sum(results)

print(solution)
