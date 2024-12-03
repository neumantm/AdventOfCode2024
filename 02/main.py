
def read_input() -> list[list[int]]:
    reports: list[list[int]] = []

    with open("input.txt") as f:
        for line in f:
            cells = line.split()
            reports.append([int(cell) for cell in cells])

    return reports


def is_report_safe(report: list[int]) -> tuple[bool, int]:
    is_decreasing = report[0] > report[1]
    for i in range(0, len(report) - 1):
        difference = report[i] - report[i + 1]
        if is_decreasing:
            if difference not in [1, 2, 3]:
                return False, i
        else:
            if difference not in [-1, -2, -3]:
                return False, i
    return True, -1


def count_safe_reports(reports: list[list[int]]):
    directly_safe = 0
    made_safe_by_problem_dampener = 0
    for report in reports:
        is_directly_safe, failed_at = is_report_safe(report)
        if is_directly_safe:
            directly_safe += 1
            continue
        # Try 1: Remove i
        fix_try_1 = report[:failed_at] + report[failed_at + 1:]
        is_safed, _ = is_report_safe(fix_try_1)
        if is_safed:
            made_safe_by_problem_dampener += 1
            continue
        # Try 2: Remove i+1
        fix_try_2 = report[:failed_at + 1] + report[failed_at + 2:]
        is_safed, _ = is_report_safe(fix_try_2)
        if is_safed:
            made_safe_by_problem_dampener += 1
            continue
        # Try 3: Remove 0 (could influence the direction)
        fix_try_3 = report[1:]
        is_safed, _ = is_report_safe(fix_try_3)
        if is_safed:
            made_safe_by_problem_dampener += 1
            continue

    print(f"There are {directly_safe} safe reports")
    print(f"When considering the problem dampener {directly_safe + made_safe_by_problem_dampener} reports are safe")


def main():
    reports = read_input()
    count_safe_reports(reports)



if __name__ == "__main__":
    main()
