from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    for input_data in s.splitlines():
        splits = input_data.split(' ')
        machine = [1 if v == '#' else 0 for v in splits[0][1:-1]]
        machine_int = int(''.join([str(v) for v in machine]), 2)
        buttons = [
            tuple(int(ind) for ind in button[1:-1].split(','))
            for button in splits[1:-1]
        ]
        button_movements = [
            int(
                ''.join([
                    '1' if ind in button else '0'
                    for ind in range(len(machine))
                ]), 2,
            ) for button in buttons
        ]
        size = 0
        for comb_size in range(1, len(button_movements) + 1):
            for combination in itertools.combinations(
                button_movements, comb_size,
            ):
                start = 0
                for item in combination:
                    start ^= item
                if start == machine_int:
                    size = comb_size
                    break
            if size > 0:
                break
        total += size
    return total


INPUT_S = '''\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''
EXPECTED = 7


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
