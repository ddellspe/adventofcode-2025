from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    rolls = support.parse_coords_hash(s, item='@')
    removed = 0
    to_be_removed = set()
    keep_processing = True
    while keep_processing:
        for (x, y) in rolls:
            if len([
                True for point in support.adjacent_8(x, y)
                if point in rolls
            ]) < 4:
                to_be_removed.add((x, y))
                removed += 1
        if len(to_be_removed) > 0:
            for roll in to_be_removed:
                rolls.discard(roll)
            to_be_removed = set()
        else:
            keep_processing = False

    return removed


INPUT_S = '''\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''
EXPECTED = 43


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
