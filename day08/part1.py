from __future__ import annotations

import argparse
import itertools
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def calculate_distance(
        box1: tuple[int, int, int],
        box2: tuple[int, int, int],
) -> float:
    return sum([(box2[i] - box1[i])**2 for i in range(3)])


def compute(s: str, num_connections: int = 10) -> int:
    boxes = set()
    for line in s.splitlines():
        x, y, z = line.split(',')
        boxes.add((int(x), int(y), int(z)))
    connections = list(itertools.combinations(boxes, 2))
    connections.sort(key=lambda x: calculate_distance(x[0], x[1]))

    groupings: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {
        box: [] for box in boxes
    }
    for box1, box2 in connections[:num_connections]:
        groupings[box1].append(box2)
        groupings[box2].append(box1)
    visited = set()
    circuits = []
    for box in boxes:
        if box in visited:
            continue
        circuit = set()
        queue = deque([box])
        visited.add(box)

        while queue:
            current = queue.popleft()
            circuit.add(current)
            for neighbor in groupings[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        circuits.append(circuit)
    circuits.sort(key=len, reverse=True)
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])


INPUT_S = '''\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
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
        print(compute(f.read(), num_connections=1000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
