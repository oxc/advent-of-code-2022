import sys

input = open('input' if len(sys.argv) == 1 else sys.argv[1]).read()

def snafu_to_number(snafu):
    digits = [-2 if c == '=' else -1 if c == '-' else int(c) for c in snafu]
    return sum(d * 5 ** i for i, d in enumerate(reversed(digits)))

def number_to_snafu(number):
    if number == 0:
        return '0'
    inverse_digits = []
    while number:
        inverse_digits.append(number % 5)
        number //= 5
    snagits = []
    acc = 0
    for digit in inverse_digits:
        digit += acc
        acc = 0
        if digit in (0, 1, 2):
            snagits.append(digit)
        else:
            snagits.append(digit - 5)
            acc = 1
    if acc:
        snagits.append(acc)
    snagits.reverse()
    return ''.join('=' if d == -2 else '-' if d == -1 else str(d) for d in snagits)

numbers = [snafu_to_number(snafu) for snafu in input.splitlines()]

needed_fuel = sum(numbers)

solution = number_to_snafu(needed_fuel)

print(solution)