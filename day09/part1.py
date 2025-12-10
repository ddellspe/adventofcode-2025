from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    red_tiles: list[tuple[int, int]] = []
    for line in s.splitlines():
        red_tiles.append((int(line.split(',')[0]), int(line.split(',')[1])))
    combinations = itertools.combinations(red_tiles, 2)
    max_size = 0
    for pt1, pt2 in combinations:
        size = (abs(pt1[0] - pt2[0]) + 1) * (abs(pt1[1] - pt2[1]) + 1)
        if size > max_size:
            max_size = size
    return max_size


INPUT_S = '''\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''
EXPECTED = 50


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
