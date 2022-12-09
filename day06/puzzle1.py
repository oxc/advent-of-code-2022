input = open('input').read()

def find_marker(input):
    for i in range(4, len(input)):
        chars = set(input[i-4:i])
        if len(chars) == 4:
            return i

solution = find_marker(input)
print(solution)
