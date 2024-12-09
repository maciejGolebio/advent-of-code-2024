LOG_LEVEL = 1


def log_info(*args):
    global LOG_LEVEL
    if LOG_LEVEL >= 0:
        print(*args)


def log_debug(*args):
    global LOG_LEVEL
    if LOG_LEVEL >= 1:
        print(*args)


def pprinrt_info(lst):
    log_info("".join(str(i) for i in lst))


def pprint_debug(lst):
    log_debug("".join(str(i) for i in lst))

def append_n_times(n, char, decompressed):
    for _ in range(n):
        decompressed.append(char)

def decompress(disk):
    decompressed = []
    counter = 0

    for i in range(0, len(disk), 2):
        file_size = disk[i]
        append_n_times(file_size, str(counter), decompressed)
        counter += 1
        if i + 1 < len(disk):
            free_size = disk[i + 1]
            append_n_times(free_size, ".", decompressed)
    return decompressed, counter

def find_leftmost_gap_with_size(decompressed, size, limit):
    #log_debug(f"Finding gap of size {size} and limit {limit}")
    for i in range(0, limit - size + 1):
        if all(block == '.' for block in decompressed[i:i+size]):
            return i
    return None

def checksum(decompressed):
    checksum = 0
    for i, block in enumerate(decompressed):
        if block == '.':
            continue
        checksum += i * int(block)
    return checksum

if __name__ == "__main__":

    with open("input.txt") as f:
        lines = f.read().splitlines()
        disk = []
        for line in lines:
            for char in line:
                disk.append(int(char))

    decompressed, file_count = decompress(disk)
    
    pprinrt_info(decompressed)
    print(decompressed)

    for file_id in range(file_count - 1, -1, -1):
        file_id_str = str(file_id)
        # log_debug(f"Moving file {file_id_str}")
        file_positions = [i for i, block in enumerate(decompressed) if block == file_id_str]
        log_debug(f"File {file_id_str} positions: {file_positions}")
        if not file_positions:
            continue
        file_start = file_positions[0]
        file_end = file_positions[-1]
        file_size = file_end - file_start + 1
        log_debug(f"File {file_id_str} start: {file_start}, end: {file_end}, size: {file_size}")

        leftmost_gap = find_leftmost_gap_with_size(decompressed, file_size, file_start)
        if leftmost_gap is not None:
            for i in range(file_size):
                decompressed[leftmost_gap + i] = file_id_str
                decompressed[file_start + i] = '.'

    # Compute and print the checksum after all moves
    print(checksum(decompressed))