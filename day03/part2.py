from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def calc_max_joltage(batt: str, num: int) -> int:
    batteries = [int(b) for b in batt]
    num_batteries = len(batteries)
    joltage = 0
    start_index = 0
    for i in range(-num + 1, 1, 1):
        joltage *= 10
        max_jolts = max(batteries[start_index:num_batteries + i])
        start_index = (
            batteries.index(
                max_jolts, start_index, num_batteries + i,
            ) + 1
        )
        joltage += max_jolts
    return joltage


def compute(s: str) -> int:
    max_joltage = 0
    for line in s.splitlines():
        max_joltage += calc_max_joltage(line, 12)
    return max_joltage


INPUT_S = '''\
987654321111111
811111111111119
234234234234278
818181911112111
'''
EXPECTED = 3121910778619


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
