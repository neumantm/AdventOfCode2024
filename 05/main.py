import functools

def read_input() -> tuple[dict[int, list[int]], list[list[int]]]:
    page_ordering_rules: dict[int, list[int]] = dict()
    updates: list[list[int]] = []
    reached_updates = False
    with open("input.txt") as f:
        for line in f:
            if len(line.strip()) == 0:
                reached_updates = True
            elif reached_updates:
                updates.append([int(page) for page in line.split(",")])
            else:
                parts = line.split("|")
                assert len(parts) == 2
                earlier_page = int(parts[0])
                later_page = int(parts[1])
                if earlier_page not in page_ordering_rules:
                    page_ordering_rules[earlier_page] = []
                page_ordering_rules[earlier_page].append(later_page)

    return page_ordering_rules, updates


def is_update_valid(page_ordering_rules: dict[int, list[int]], update: list[int]) -> bool:
    seen_pages: set[int] = set()
    for page in update:
        if page in page_ordering_rules:
            for must_be_later in page_ordering_rules[page]:
                if must_be_later in seen_pages:
                    return False
        seen_pages.add(page)
    return True


def get_middle_page(update: list[int]) -> int:
    quotient, remainder = divmod(len(update), 2)
    assert remainder == 1
    return update[quotient]


def sorted_by_rules(page_ordering_rules: dict[int, list[int]], update: list[int]) -> list[int]:
    def compare(x: int, y: int):
        if x in page_ordering_rules:
            if y in page_ordering_rules[x]:
                return -1
        if y in page_ordering_rules:
            if x in page_ordering_rules[y]:
                return 1
        # not sure of this actually works as we declare to objects equal even though we just do not know anyting about them
        # It could happen that they are actually transitievely dependent
        return 0
    return sorted(update, key=functools.cmp_to_key(compare))


def main():
    page_ordering_rules, updates = read_input()
    correct_mp_sum = 0
    sorted_mp_sum = 0
    for update in updates:
        if is_update_valid(page_ordering_rules, update):
            mp = get_middle_page(update)
            correct_mp_sum += mp
        else:
            sorted_update = sorted_by_rules(page_ordering_rules, update)
            mp = get_middle_page(sorted_update)
            sorted_mp_sum += mp

    print(f"Sum of middle page for correctly sorted updates: {correct_mp_sum}")
    print(f"Sum of middle page for initially incorrectly sorted updates after sorting: {sorted_mp_sum}")


if __name__ == "__main__":
    main()
