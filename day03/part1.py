from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    max_joltage = 0
    for line in s.splitlines():
        batteries = [int(b) for b in line]
        num_batteries = len(batteries)
        max_power = max(batteries)
        first_max_index = batteries.index(max_power)
        if num_batteries - 1 == first_max_index:
            second_max_power = max_power
            max_power = max(batteries[:first_max_index])
        else:
            second_max_power = max(batteries[first_max_index+1:])
        max_joltage += (max_power * 10 + second_max_power)
    return max_joltage


INPUT_S = '''\
987654321111111
811111111111119
234234234234278
818181911112111
'''
EXPECTED = 357


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
