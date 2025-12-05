from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    (rngs, ingredients) = s.split('\n\n')
    ranges = [
        tuple(int(val) for val in rng.split('-'))
        for rng in rngs.splitlines()
    ]
    count = 0
    for ingredient in ingredients.splitlines():
        if len([
            True for rng in ranges
            if rng[0] <= int(ingredient) and int(ingredient) <= rng[1]
        ]) > 0:
            count += 1
    return count


INPUT_S = '''\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''
EXPECTED = 3


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
