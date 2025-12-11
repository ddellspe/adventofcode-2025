from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    paths: dict[str, list[str]] = {}
    for line in s.splitlines():
        source, destinations = line.split(': ')
        paths[source] = destinations.split(' ')
    found_paths = set()
    queue: collections.deque[tuple[str, ...]]
    queue = collections.deque([tuple(['you'])])

    while queue:
        path = queue.popleft()

        if path[-1] == 'out':
            found_paths.add(path)
            continue

        for next in paths[path[-1]]:
            if next in path:
                continue
            queue.append(tuple(list(path) + [next]))
    return len(found_paths)


INPUT_S = '''\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''
EXPECTED = 5


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
