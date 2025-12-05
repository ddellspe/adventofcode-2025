from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    rngs = s.split('\n\n')[0]
    ranges = [
        [int(val) for val in rng.split('-')]
        for rng in rngs.splitlines()
    ]
    ranges.sort(key=lambda x: x[0])
    fresh_ingredients = [ranges[0]]

    for current_start, current_end in ranges[1:]:

        _, last_merged_end = fresh_ingredients[-1]

        if current_start <= last_merged_end:
            fresh_ingredients[-1][1] = max(last_merged_end, current_end)
        else:
            fresh_ingredients.append([current_start, current_end])

    return sum([
        ingredient_range[1] - ingredient_range[0] + 1
        for ingredient_range in fresh_ingredients
    ])


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
EXPECTED = 14


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
