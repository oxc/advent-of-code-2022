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

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        if self.op in ('-', '+'):
            return f'({self.lop} {self.op} {self.rop})'
        return f'{self.lop} {self.op} {self.rop}'

class Value(object):
    def __init__(self, value):
        self.value = value
        self.prev = None

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Var(object):
    def __init__(self):
        self.prev = None
        self.value = None

    def __str__(self):
        return 'H'

class Equals(object):
    def __init__(self, lhs, _, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f'{self.lhs} = {self.rhs}'

    def resolve(self):
        if self.rhs.value is None:
            self.lhs, self.rhs = self.rhs, self.lhs
        if isinstance(self.lhs, Var):
            return True

        exp = self.lhs
        if exp.rop.value is None:
            if exp.op in ('*', '+'):
                exp.lop, exp.rop = exp.rop, exp.lop
        if exp.lop.value is None:
            reverse_op = {'*': '/', '/': '*', '+': '-', '-': '+'}[exp.op]
            self.rhs = Operation(self.rhs, reverse_op, exp.rop)
            self.lhs = exp.lop
            int(self.rhs)
        else:
            if exp.op in ('-', '/'):
                self.rhs = Operation(exp.lop, exp.op, self.rhs)
                self.lhs = exp.rop
                int(self.rhs)

expressions = {
    lhs: Equals(*rhs.split()) if lhs == 'root' else Var() if lhs == 'humn' else Value(int(rhs)) if rhs.isdigit() else Operation(*rhs.split()) for lhs, rhs in
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
    elif isinstance(expr, Value):
        values.append(expr)
root = expressions['root']
root.lhs = expressions[root.lhs]
root.rhs = expressions[root.rhs]

# resolve values without triggering (too much) recursion
while values:
    prev = values.pop(0).prev
    if prev is None:
        continue
    if isinstance(prev, Operation):
        # this is part of the tree that needs to be resolved
        if prev.lop.value is None or prev.rop.value is None:
            continue
    int(prev)
    values.append(prev)

print(str(root))
while not root.resolve():
    print(str(root))

solution = int(root.rhs)

print(solution)