from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = [list(line) for line in s.splitlines()]
    equation_pieces: zip[tuple[str]] = zip(*lines)
    equation: list[tuple[str]] = []
    equations: list[list[tuple[str]]] = []
    for piece in equation_pieces:
        if all([True if p == ' ' else False for p in piece]):
            equations.append(equation)
            equation = []
            continue
        equation.append(piece)
    equations.append(equation)
    for equation in equations:
        numbers = [
            int(''.join(num[0]))
            for num in zip([digit[:-1] for digit in equation])
        ]
        operation = [
            op for op in [
                last[-1]
                for last in equation
            ] if op != ' '
        ][0]
        if operation == '+':
            total += sum(numbers)
        elif operation == '*':
            total += math.prod(numbers)
    return total


INPUT_S = '''\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
'''
EXPECTED = 3263827


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
