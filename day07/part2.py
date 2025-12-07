from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    grid: list[str] = [line for line in s.splitlines()]
    beams: dict[int, int] = {grid[0].index('S'): 1}
    for row in range(1, len(grid)):
        next: dict[int, int] = {}
        for col, count in beams.items():
            if grid[row][col] == '^':
                next.setdefault(col-1, 0)
                next.setdefault(col+1, 0)
                next[col-1] += count
                next[col+1] += count
            else:
                next.setdefault(col, 0)
                next[col] += count
        beams = next
    return sum(beams.values())


INPUT_S = '''\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''
EXPECTED = 40


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
