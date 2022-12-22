import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

class Operation(object):
    def __init__(self, lop, op, rop):
        self.lop = lop
        self.op = op
        self.rop = rop
        self.prev = None
        self.value = None

    def __int__(self):
        if self.value is None:
            if self.op == '+':
                self.value = int(self.lop) + int(self.rop)
            elif self.op == '*':
                self.value = int(self.lop) * int(self.rop)
            elif self.op == '-':
                self.value = int(self.lop) - int(self.rop)
            elif self.op == '/':
                self.value = int(self.lop) // int(self.rop)
        return self.value


class Value(object):
    def __init__(self, value):
        self.value = value
        self.prev = None

    def __int__(self):
        return self.value

expressions = {
    lhs: Value(int(rhs)) if rhs.isdigit() else Operation(*rhs.split()) for lhs, rhs in
    (line.split(': ') for line in input.splitlines())
 }

# build graph
values = []
for expr in expressions.values():
    if isinstance(expr, Operation):
        expr.lop = expressions[expr.lop]
        assert(expr.lop.prev is None)
        expr.lop.prev = expr
        expr.rop = expressions[expr.rop]
        assert(expr.rop.prev is None)
        expr.rop.prev = expr
    else:
        values.append(expr)

# resolve values without triggering (too much) recursion
while values:
    prev = values.pop(0).prev
    if prev is None:
        continue
    int(prev)
    values.append(prev)

root = expressions['root']

solution = int(root)

print(solution)