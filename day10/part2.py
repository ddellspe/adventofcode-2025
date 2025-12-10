from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest
from z3 import Int
from z3 import Optimize

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    for input_data in s.splitlines():
        splits = input_data.split(' ')
        buttons = [
            [int(ind) for ind in button[1:-1].split(',')]
            for button in splits[1:-1]
        ]
        final_joltage = [int(v) for v in splits[-1][1:-1].split(',')]
        counters_button_lookup = defaultdict(list)
        for i, button in enumerate(buttons):
            for index in button:
                counters_button_lookup[index].append(i)

        presses = Int('presses')
        button_vars = [Int(f'button{i}') for i in range(len(buttons))]

        equations = []
        for counter, counter_buttons in counters_button_lookup.items():
            equations.append(
                final_joltage[counter] == sum(
                    [button_vars[i] for i in counter_buttons],
                ),
            )

        for button_var in button_vars:
            equations.append(button_var >= 0)

        equations.append(presses == sum(button_vars))

        opt = Optimize()
        opt.add(equations)
        opt.minimize(presses)
        opt.check()

        output = opt.model()[presses]

        total += int(str(output))
    return total


INPUT_S = '''\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''
EXPECTED = 33


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
