def read_input() -> list[list[str]]:
    result: list[list[str]] = []
    with open("input.txt") as f:
        for line in f:
            result.append(list(line.strip()))
    return result


def get_all_sequences(input: list[list[str]]) -> list[str]:
    result: list[str] = []
    # Rows
    for row in input:
        result.append("".join(row))
    # Columns
    for column_number in range(len(input[0])):
        column = [row[column_number] for row in input]
        result.append("".join(column))
    # Right Diagnoals starting at the top
    for column_number in range(len(input[0])):
        diag = [input[row_number][row_number + column_number] for row_number in range(len(input)) if column_number + row_number < len(input[0])]
        result.append("".join(diag))
    # Right Diagnoals starting at the left
    for row_number in range(1, len(input)):
        diag = [input[row_number + column_number][column_number] for column_number in range(len(input[0])) if column_number + row_number < len(input)]
        result.append("".join(diag))
    # Left Diagnoals starting at the top
    for column_number in range(len(input[0])):
        diag = [input[row_number][len(input[0]) - (row_number + column_number + 1)] for row_number in range(len(input)) if len(input[0]) - (row_number + column_number) > 0]
        result.append("".join(diag))
    # Left Diagnoals starting at the right
    for row_number in range(1, len(input)):
        diag = [input[row_number + column_number][len(input[0]) - (column_number + 1)] for column_number in range(len(input[0])) if column_number + row_number < len(input)]
        result.append("".join(diag))
    return result


def count_xmas(sequences: list[str]) -> int:
    result = 0
    for sequence in sequences:
        for i in range(len(sequence)):
            reamining_squence = sequence[i:]
            if reamining_squence.startswith("XMAS") or reamining_squence.startswith("SAMX"):
                result += 1
    return result


def find_xmas(input: list[list[str]]):
    for row in input:
        assert len(row) == len(input[0])
    sequences = get_all_sequences(input)
    print(f"{count_xmas(sequences)}")


def check_x_mas(input: list[list[str]], rownum: int, columnnum: int) -> bool:
    if input[rownum][columnnum] != "A":
        return False
    if input[rownum - 1][columnnum - 1] == "M":
        if input[rownum + 1][columnnum + 1] != "S":
            return False
    elif input[rownum - 1][columnnum - 1] == "S":
        if input[rownum + 1][columnnum + 1] != "M":
            return False
    else:
        return False
    if input[rownum + 1][columnnum - 1] == "M":
        if input[rownum - 1][columnnum + 1] != "S":
            return False
    elif input[rownum + 1][columnnum - 1] == "S":
        if input[rownum - 1][columnnum + 1] != "M":
            return False
    else:
        return False
    return True


def find_canditates(input: list[list[str]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for rownnum in range(1, len(input) - 1):
        for columnnum in range(1, len(input[0]) - 1):
            if input[rownnum][columnnum] == "A":
                result.append((rownnum, columnnum))
    return result


def find_x_mas(input: list[list[str]]):
    candidates = find_canditates(input)
    found = [canditdate for canditdate in candidates if check_x_mas(input, canditdate[0], canditdate[1])]
    print(f"Found {len(found)} x-mas")


def main():
    input = read_input()
    find_xmas(input)
    find_x_mas(input)


if __name__ == "__main__":
    main()
