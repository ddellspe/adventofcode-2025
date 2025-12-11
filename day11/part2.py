from __future__ import annotations

import argparse
import math
import os.path
from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def count_paths(paths: dict[str, list[str]], start: str, end: str) -> int:
    @lru_cache(None)
    def dfs(node: str) -> int:
        if node == end:
            return 1
        return sum(dfs(next) for next in paths[node])
    return (dfs(start))


def compute(s: str) -> int:
    paths: dict[str, list[str]] = {}
    for line in s.splitlines():
        source, destinations = line.split(': ')
        paths[source] = destinations.split(' ')

    paths['out'] = []

    return max(
        [
            math.prod(
                count_paths(paths, start, end)
                for start, end in zip(path, path[1:])
            )
            for path in [
                ['svr', 'dac', 'fft', 'out'],
                ['svr', 'fft', 'dac', 'out'],
            ]
        ],
    )


INPUT_S = '''\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''
EXPECTED = 2


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
