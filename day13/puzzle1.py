import sys
input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

from ast import literal_eval

pairs = [[literal_eval(line) for line in pair.splitlines()] for pair in input.split('\n\n')]

def in_order(a, b):
    if isinstance(a, list):
        if isinstance(b, list):
            for i, j in zip(a,b):
                res = in_order(i,j)
                if res is not None:
                    return res
            return in_order(len(a), len(b))
        return in_order(a, [b])
    if isinstance(b, list):
        return in_order([a], b)
    if a == b:
        return None
    return a < b

solution = sum(i+1 for i, pair in enumerate(pairs) if in_order(*pair))

print(solution)
