from __future__ import annotations

import argparse
import itertools
import os.path

import pytest
from shapely.geometry import Polygon

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    red_tiles: list[tuple[int, int]] = []
    for line in s.splitlines():
        red_tiles.append((int(line.split(',')[0]), int(line.split(',')[1])))
    pattern = Polygon(red_tiles)
    combinations = itertools.combinations(red_tiles, 2)
    max_size = 0
    for pt1, pt2 in combinations:
        min_x = min(pt1[0], pt2[0])
        min_y = min(pt1[1], pt2[1])
        max_x = max(pt1[0], pt2[0])
        max_y = max(pt1[1], pt2[1])
        if pattern.contains(
            Polygon((
                (min_x, min_y), (max_x, min_y),
                (max_x, max_y), (min_x, max_y),
            )),
        ):
            size = (max_x - min_x + 1) * (max_y - min_y + 1)
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
EXPECTED = 24


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
