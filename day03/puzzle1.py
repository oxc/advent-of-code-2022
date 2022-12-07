input = open('input').read()

def priority(item):
    o = ord(item)
    if o >= ord('a'):
        return o - ord('a') + 1
    return o - ord('A') + 27


items = list(
    set(line[0:int(len(line)/2)])
        .intersection(set(line[int(len(line)/2):]))
        .pop() 
    for line in input.splitlines()
)
solution = sum(priority(item) for item in items)
print(solution)
