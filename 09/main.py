import re


def read_input() -> list[tuple[int, bool, int]]:
    """
    Returns a list of tuples: (length, is_space, file_id)
    """
    file_id = 0
    is_space = False
    result: list[tuple[int, bool, int]] = []
    with open("input.txt") as f:
        for char in f.read():
            if not char.isdigit():
                continue
            result.append((int(char), is_space, file_id if not is_space else -1))
            if not is_space:
                file_id += 1
            is_space = not is_space
    return result


def build_disk_map(input: list[tuple[int, bool, int]]) -> list[str]:
    result: list[str] = []
    for section in input:
        for _ in range(section[0]):
            if section[1]:
                result.append(".")
            else:
                result.append(str(section[2]))
    return result


def compact_disk(input: list[tuple[int, bool, int]]) -> list[tuple[int, bool, int]]:
    result: list[tuple[int, bool, int]] = []
    last_index_completely_moved = len(input)
    currently_moving: tuple[int, bool, int] = input[last_index_completely_moved - 1]
    moved_of_current_section = 0

    for i, section in enumerate(input):
        if i >= last_index_completely_moved:
            result.append((section[0], True, -1))
        elif i == last_index_completely_moved - 1:
            remaining_blocks = section[0] - moved_of_current_section
            result.append((remaining_blocks, section[1], section[2]))
            result.append((moved_of_current_section, True, -1))
            last_index_completely_moved -= 1
            currently_moving = (0, True, -2)
            moved_of_current_section = 0
        elif section[1]:
            available_space = section[0]

            while available_space > 0:
                if currently_moving[1]:
                    last_index_completely_moved -= 1
                    currently_moving = input[last_index_completely_moved - 1]
                    moved_of_current_section = 0
                    if last_index_completely_moved == i:
                        result.append((available_space, True, -1))
                        break
                available_blocks = currently_moving[0] - moved_of_current_section

                if available_space == available_blocks:
                    result.append((available_space, currently_moving[1], currently_moving[2]))
                    last_index_completely_moved -= 1
                    currently_moving = input[last_index_completely_moved - 1]
                    moved_of_current_section = 0
                    available_space = 0
                elif available_space < available_blocks:
                    result.append((available_space, False, currently_moving[2]))
                    moved_of_current_section += available_space
                    available_space = 0
                else:
                    result.append((available_blocks, False, currently_moving[2]))
                    available_space -= available_blocks
                    last_index_completely_moved -= 1
                    currently_moving = input[last_index_completely_moved - 1]
                    moved_of_current_section = 0
        else:
            result.append(section)

    return result


def compact_disk_without_fragment(input: list[tuple[int, bool, int]]) -> list[tuple[int, bool, int]]:
    remaining_space_in_sections: list[int] = [] # (length)

    for section in input:
        if section[1]:
            remaining_space_in_sections.append(section[0])
        else:
            remaining_space_in_sections.append(0)

    move_sources: dict[int, list[int]] = {} # for each space section a list of indices of sections that are to be moved to it
    moved_sections: list[int] = []

    for i in range(len(input) - 1, -1, -1):
        section = input[i]
        if section[1]:
            continue
        section_length = section[0]
        for j in range(i):
            if remaining_space_in_sections[j] >= section_length:
                if j not in move_sources:
                    move_sources[j] = []
                move_sources[j].append(i)
                remaining_space_in_sections[j] -= section_length
                moved_sections.append(i)
                break

    result: list[tuple[int, bool, int]] = []

    for i in range(len(input)):
        orig_section = input[i]
        if i in moved_sections:
            result.append((orig_section[0], True, -1))
        elif not orig_section[1]:
            result.append(orig_section)
        else:
            remaining_blocks = orig_section[0]
            for move_src in move_sources.get(i, []):
                move_src_section = input[move_src]
                result.append((move_src_section[0], False, move_src_section[2]))
                remaining_blocks -= move_src_section[0]
            if remaining_blocks > 0:
                result.append((remaining_blocks, True, -1))

    return result


def calc_checksum(map: list[tuple[int, bool, int]]) -> int:
    checksum = 0
    offset = 0
    for section in map:
        for i in range(section[0]):
            if not section[1]:
                checksum += offset * section[2]
            offset += 1
    return checksum


def check(input: list[tuple[int, bool, int]], compacted: list[tuple[int, bool, int]], non_fragmented: bool = False):
    input_map = build_disk_map(input)
    compacted_map = build_disk_map(compacted)
    if len(input_map) != len(compacted_map):
        raise Exception(f"Lengths do not match: {len(input_map)} != {len(compacted_map)}")

    input_block_count: dict[int, int] = {}

    for section in input:
        if section[1]:
            continue
        if section[2] not in input_block_count:
            input_block_count[section[2]] = 0
        input_block_count[section[2]] += section[0]

    compacted_block_count: dict[int, int] = {}

    for section in compacted:
        if section[1]:
            continue
        if section[2] not in compacted_block_count:
            compacted_block_count[section[2]] = 0
        compacted_block_count[section[2]] += section[0]

    for file_id in input_block_count:
        if file_id not in compacted_block_count:
            raise Exception(f"File id {file_id} not found in compacted disk")
        if input_block_count[file_id] != compacted_block_count[file_id]:
            raise Exception(f"File id {file_id} block count does not match: {input_block_count[file_id]} != {compacted_block_count[file_id]}")

    if non_fragmented:
        return

    found_empty = False
    for section in compacted:
        if section[1]:
            found_empty = True
        else:
            if found_empty:
                raise Exception("Found non-empty section after empty section")

def main():
    input = read_input()
    disk_map = build_disk_map(input)

    # print(f"DM       : {''.join(disk_map)}")

    compacted_disk = compact_disk(input)

    check(input, compacted_disk)

    # print(f"Compacted: {''.join(build_disk_map(compacted_disk))}")

    print(f"{calc_checksum(compacted_disk)=}")

    non_fragmented_compacted_disk = compact_disk_without_fragment(input)

    check(input, non_fragmented_compacted_disk, True)

    # print(f"Non-fragm: {''.join(build_disk_map(non_fragmented_compacted_disk))}")

    print(f"{calc_checksum(non_fragmented_compacted_disk)=}")


if __name__ == "__main__":
    main()
