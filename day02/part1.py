from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_valid(val: int) -> bool:
    value = str(val)
    size = len(value)
    if size % 2 == 0:
        if value[0:size//2] == value[size//2:]:
            return False
    return True


def compute(s: str) -> int:
    invalid_ids = 0
    ranges = [(int(range.split('-')[0]), int(range.split('-')[1]))
              for range in s.split(',')]
    for (start, end) in ranges:
        for id in range(start, end + 1):
            if not is_valid(id):
                invalid_ids += id

    return invalid_ids


INPUT_S = '''\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
'''
EXPECTED = 1227775554


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
