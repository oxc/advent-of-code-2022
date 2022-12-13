import sys
input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

from ast import literal_eval
from functools import cmp_to_key

divider1 = [[2]]
divider2 = [[6]]

packets = [literal_eval(line) for line in input.splitlines() if line.strip()] + [divider1, divider2]

def compare(a, b):
    if isinstance(a, list):
        if isinstance(b, list):
            for i, j in zip(a,b):
                res = compare(i,j)
                if res != 0:
                    return res
            return compare(len(a), len(b))
        return compare(a, [b])
    if isinstance(b, list):
        return compare([a], b)
    if a == b:
        return 0
    return -1 if a < b else 1

packet_key = cmp_to_key(compare)

packets.sort(key=packet_key)

decoder1 = packets.index(divider1)+1
decoder2 = packets.index(divider2)+1

solution = decoder1 * decoder2

print(solution)
