from enum import Enum
import itertools


class Operator(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    CONCATINATION = 3


def read_input() -> list[tuple[int, list[int]]]:
    result: list[tuple[int, list[int]]] = []
    with open("input.txt") as f:
        for line in f:
            parts = line.split(":")
            result.append((int(parts[0].strip()), [int(operand) for operand in parts[1].split()]))
    return result


def check_equation(required_result: int, operands: list[int], operators: tuple[Operator, ...]) -> bool:
    assert len(operands) == len(operators) + 1

    intermediate_result = operands[0]
    for i in range(1, len(operands)):
        if operators[i - 1] == Operator.MULTIPLICATION:
            intermediate_result *= operands[i]
        elif operators[i - 1] == Operator.ADDITION:
            intermediate_result += operands[i]
        elif operators[i - 1] == Operator.CONCATINATION:
            intermediate_result = int(str(intermediate_result) + str(operands[i]))
        else:
            assert False
        if intermediate_result > required_result:
            return False
    return intermediate_result == required_result


def check_if_equation_can_be_fulfilled(equation: tuple[int, list[int]]) -> bool:
    result = equation[0]
    operands = equation[1]
    num_operators = len(operands) - 1

    for operator_sequence in itertools.product(list(Operator), repeat=num_operators):
        if check_equation(result, operands, operator_sequence):
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
