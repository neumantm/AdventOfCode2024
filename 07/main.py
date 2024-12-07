def read_input() -> list[tuple[int, list[int]]]:
    result: list[tuple[int, list[int]]] = []
    with open("input.txt") as f:
        for line in f:
            parts = line.split(":")
            result.append((int(parts[0].strip()), [int(operand) for operand in parts[1].split()]))
    return result


def check_equation(required_result: int, operands: list[int], operator_possibility_num: int) -> bool:
    intermediate_result = operands[0]
    num_operators = len(operands) - 1
    for i in range(1, len(operands)):
        bit_mask = 1 << (num_operators - i)
        is_mult = operator_possibility_num & bit_mask > 0
        if is_mult:
            intermediate_result *= operands[i]
        else:
            intermediate_result += operands[i]
        if intermediate_result > required_result:
            return False
    return intermediate_result == required_result


def check_if_equation_can_be_fulfilled(equation: tuple[int, list[int]]) -> bool:
    result = equation[0]
    operands = equation[1]
    num_operators = len(operands) - 1
    possibilities = 2**num_operators

    for i in range(possibilities):
        if check_equation(result, operands, i):
            return True
    return False


def main():
    input = read_input()

    total = 0

    for i, equation in enumerate(input):
        if check_if_equation_can_be_fulfilled(equation):
            print(f"Can fullfill equation {i}")
            total += equation[0]

    print(f"{total=}")


if __name__ == "__main__":
    main()
