
def read_input() -> tuple[list[int], list[int]]:
    left_list: list[int] = []
    right_list: list[int] = []

    with open("input.txt") as f:
        for line in f:
            left_cell, right_cell = line.split()
            left_list.append(int(left_cell))
            right_list.append(int(right_cell))

    return left_list, right_list


def calc_differences(left_list: list[int], right_list: list[int]) -> int:
    assert len(left_list) == len(right_list)
    diff_sum = 0
    for i in range(0, len(left_list)):
        diff = abs(left_list[i] - right_list[i])
        diff_sum += diff

    return diff_sum


def distance(left_list: list[int], right_list: list[int]):
    left_list.sort()
    right_list.sort()

    diff_sum = calc_differences(left_list, right_list)
    print(f"The distance is {diff_sum}")


def calc_value_for_entry(left_entry: int, right_list: list[int]) -> int:
    count = right_list.count(left_entry)
    return count * left_entry


def similarity(left_list: list[int], right_list: list[int]):
    sum = 0
    for left_entry in left_list:
        sum += calc_value_for_entry(left_entry, right_list)

    print(f"The similarity is {sum}")


def main():
    left_list, right_list = read_input()

    distance(left_list.copy(), right_list.copy())
    similarity(left_list.copy(), right_list.copy())


if __name__ == "__main__":
    main()
