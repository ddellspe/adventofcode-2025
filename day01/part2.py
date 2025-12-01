from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    dial = 50
    zeroes = 0
    for line in s.splitlines():
        initial_dial = dial
        dir = line[0]
        val = int(line[1:])
        if dir == 'R':
            dial += val
        else:
            initial_dial = (100-initial_dial) % 100
            dial -= val

        overspin = val % 100

        zeroes += (initial_dial + overspin) // 100 + val // 100

        dial %= 100

    return zeroes


INPUT_S = '''\
L68
L30
R48
L5
R60
L55
L1
L99
R300
R14
L300
L82
'''
EXPECTED = 12


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
