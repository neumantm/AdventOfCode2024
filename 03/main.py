from re import compile

DO="do()"
DONT="don't()"

instruction_pattern = compile(r"mul\((?P<X>[0-9]{1,3}),(?P<Y>[0-9]{1,3})\)")


def read_input() -> str:
    with open("input.txt") as f:
        return f.read()


def find_valid_instructions(input: str) -> list[tuple[str, str]]:
    """
    Returns Tuples like (X,Y) for valid multiplication instructions like mul(X,Y)
    """
    return instruction_pattern.findall(input)


def find_valid_instructions_considering_donts(input: str) -> list[tuple[str, str]]:
    """
    Returns Tuples like (X,Y) for valid multiplication instructions like mul(X,Y)
    """
    instructions: list[tuple[str, str]] = []
    is_on = True

    i = 0
    while i < len(input):
        remaining_input = input[i:]
        if remaining_input.startswith(DO):
            is_on = True
            i += len(DO)
        elif remaining_input.startswith(DONT):
            is_on = False
            i += len(DONT)
        elif is_on:
            # match only looks at the beginning of the string
            found = instruction_pattern.match(remaining_input)
            if found:
                instructions.append((found.group("X"), found.group("Y")))
                i += found.end()
            else:
                i += 1
        else:
            i += 1

    return instructions

def calculate_sum_of_products(instructions: list[tuple[str, str]]) -> int:
    return sum([int(x) * int(y) for x, y in instructions])


def main():
    input = read_input()
    instructions = find_valid_instructions(input)
    sum = calculate_sum_of_products(instructions)

    print(f"{sum=}")

    instructions_with_donts = find_valid_instructions_considering_donts(input)
    sum_with_donts = calculate_sum_of_products(instructions_with_donts)

    print(f"{sum_with_donts=}")


if __name__ == "__main__":
    main()
