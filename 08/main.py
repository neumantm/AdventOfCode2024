import itertools


def read_input() -> list[list[str]]:
    result: list[list[str]] = []
    with open("input.txt") as f:
        for line in f:
            if len(line.strip()) > 0:
                result.append(list(line.strip()))
    return result


def find_antennas(input: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    result: dict[str, list[tuple[int, int]]] = {}
    for y, row in enumerate(input):
        for x, cell in enumerate(row):
            if cell.isalnum():
                if cell not in result:
                    result[cell] = []
                result[cell].append((x, y))
    return result


def vec_sub(vec1: tuple[int, int], vec2: tuple[int, int]) -> tuple[int, int]:
    return vec1[0] - vec2[0], vec1[1] - vec2[1]


def vec_add(vec1: tuple[int, int], vec2: tuple[int, int]) -> tuple[int, int]:
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def get_antinodes(antenna1: tuple[int, int], antenna2: tuple[int, int]) -> set[tuple[int, int]]:
    difference_vec = vec_sub(antenna1, antenna2)
    inverted_difference_vec = vec_sub((0, 0), difference_vec)

    antinode1 = vec_add(antenna1, difference_vec)
    antinode2 = vec_add(antenna2, inverted_difference_vec)
    return {antinode1, antinode2}


def get_antinodes_with_harmonics(antenna1: tuple[int, int],
                                 antenna2: tuple[int, int],
                                 width: int,
                                 height: int) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()

    difference_vec = vec_sub(antenna1, antenna2)

    working_vec = antenna1

    while True:
        if working_vec[0] < 0 or working_vec[0] >= width or working_vec[1] < 0 or working_vec[1] >= height:
            break
        result.add(working_vec)
        working_vec = vec_add(working_vec, difference_vec)

    working_vec = antenna2

    while True:
        if working_vec[0] < 0 or working_vec[0] >= width or working_vec[1] < 0 or working_vec[1] >= height:
            break
        result.add(working_vec)
        working_vec = vec_sub(working_vec, difference_vec)

    return result


def filter_positions(positions: set[tuple[int, int]], width: int, height: int) -> set[tuple[int, int]]:
    return {pos for pos in positions if pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height}


def find_antinodes(input: list[list[str]], with_harmonics=False):
    for row in input:
        assert len(row) == len(input[0])

    width = len(input[0])
    height = len(input)
    antennas = find_antennas(input)

    all_antinodes: set[tuple[int, int]] = set()

    for frequency, freq_antennas in antennas.items():
        for antennaA, antennaB in itertools.combinations(freq_antennas, 2):
            if with_harmonics:
                antinodes = get_antinodes_with_harmonics(antennaA, antennaB, width, height)
            else:
                antinodes = get_antinodes(antennaA, antennaB)
            all_antinodes.update(antinodes)

    antinodes_in_bounds = filter_positions(all_antinodes, width, height)

    print(f"{len(antinodes_in_bounds)=}")


def main():
    input = read_input()
    find_antinodes(input)
    print("with harmonics:")
    find_antinodes(input, True)


if __name__ == "__main__":
    main()
