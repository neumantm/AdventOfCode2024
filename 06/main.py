from typing import Optional

from dataclasses import dataclass, field, replace
from enum import Enum
from functools import partial


def apply_direction(direction: tuple[int, int], position: tuple[int, int]) -> tuple[int, int]:
    return position[0] + direction[0], position[1] + direction[1]


class Direction(Enum):
    NORTH = partial(apply_direction, (0, -1))
    EAST = partial(apply_direction, (1, 0))
    SOUTH = partial(apply_direction, (0, 1))
    WEST = partial(apply_direction, (-1, 0))


@dataclass(frozen=True)
class Area():
    """
        Rows: y
        Columns: x
        Obstructions: list(tuple(x,y))
        x=0, y=0 is at top left
        x=1, y=0 is right (east) of that
        x=0, y=1 is below (south) of it
    """
    rows: int
    columns: int
    obstructions: list[tuple[int, int]]

    def contains_point(self, point: tuple[int, int]) -> bool:
        x = point[0]
        x_ok = x >= 0 and x < self.columns
        y = point[1]
        y_ok = y >= 0 and y < self.rows
        return x_ok and y_ok


@dataclass
class Guard():
    """
        Position: tuple(x, y)
        Number of positions: count
        Direction: direction
    """
    position: tuple[int, int]
    direction: Direction
    patrol_path: set[tuple[int, int, Direction]] = field(init=False)

    def patrol_path_entry(self) -> tuple[int, int, Direction]:
        return self.position[0], self.position[1], self.direction

    def __post_init__(self):
        self.patrol_path = set([self.patrol_path_entry()])

    def would_be_pos_after_step(self) -> tuple[int, int]:
        return self.direction.value(self.position)

    def step(self) -> bool:
        """
        Returns whether we have been at the same position in the same orientation
        """
        self.position = self.would_be_pos_after_step()
        patrol_path_entry = self.patrol_path_entry()
        if patrol_path_entry in self.patrol_path:
            return True
        self.patrol_path.add(patrol_path_entry)
        return False

    def turn_right(self):
        if self.direction == Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.NORTH

    def count_patrol_positions(self) -> int:
        positions = {(entry[0], entry[1]) for entry in self.patrol_path}
        return len(positions)


def find_all(haystack: str, needle: str) -> list[int]:
    result: list[int] = []
    pos = 0
    while (found_at := haystack.find(needle, pos)) != -1:
        result.append(found_at)
        pos = found_at + 1
    return result


def read_input() -> tuple[Area, Guard]:
    columns = 0
    rows = 0
    obstructions: list[tuple[int, int]] = []
    guard: Optional[Guard] = None

    with open("input.txt") as f:
        for line in f:
            if columns == 0:
                columns = len(line)
            else:
                assert len(line) == columns

            for obstruction_x in find_all(line, "#"):
                obstructions.append((obstruction_x, rows))

            if "^" in line:
                assert guard is None
                guard_x = line.find("^")
                guard = Guard((guard_x, rows), Direction.NORTH)
            if "v" in line:
                assert guard is None
                guard_x = line.find("v")
                guard = Guard((guard_x, rows), Direction.SOUTH)
            if ">" in line:
                assert guard is None
                guard_x = line.find(">")
                guard = Guard((guard_x, rows), Direction.EAST)
            if "<" in line:
                assert guard is None
                guard_x = line.find("<")
                guard = Guard((guard_x, rows), Direction.WEST)

            rows += 1

    area = Area(rows, columns, obstructions)

    assert guard is not None

    return area, guard


def simulate_guard(area: Area, guard: Guard) -> tuple[int, bool]:
    """
    Returns length of patrol path and whether it is a loop
    """
    turn_counter = 0

    while True:
        next_pos = guard.would_be_pos_after_step()
        if not area.contains_point(next_pos):
            break
        if next_pos in area.obstructions:
            guard.turn_right()
            # Need to re-check next_pos, therefore just continue with next iteration
            turn_counter += 1
            assert turn_counter < 4
        else:
            turn_counter = 0
            is_on_loop = guard.step()
            if is_on_loop:
                return guard.count_patrol_positions(), True

    return guard.count_patrol_positions(), False


def find_obstructions_that_make_loop(area: Area, guard: Guard):
    all_positions = [(x, y) for x in range(area.columns) for y in range(area.rows)]

    loops_found = 0

    iterations_since_last_fraction_report = 0

    for i, position in enumerate(all_positions):
        iterations_since_last_fraction_report += 1
        if iterations_since_last_fraction_report > len(all_positions) / 20:
            iterations_since_last_fraction_report = 0
            fraction = i / len(all_positions)
            print(f"{round(fraction * 100, 0)}%")

        if position == guard.position:
            continue
        if position in area.obstructions:
            continue
        new_area = replace(area, obstructions=(area.obstructions + [position]))
        patrol_path_length, was_a_loop = simulate_guard(new_area, replace(guard))
        if was_a_loop:
            print(f"Found a loop, when placing obstruction at {position}. The patrol path covers {patrol_path_length} spaces")
            loops_found += 1

    print(f"Found {loops_found} loops.")


def main():
    area, guard = read_input()

    patrol_path_length, was_a_loop = simulate_guard(area, replace(guard))
    assert not was_a_loop
    print(f"{patrol_path_length=}")

    find_obstructions_that_make_loop(area, guard)


if __name__ == "__main__":
    main()
