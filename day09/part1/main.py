def pretty_print(disk):
    print(''.join([str(x) for x in disk]))

def append_n_times(n, char, decompressed):
    for _ in range(n):
        decompressed.append(char)

def decompress(disk):
    decompressed = []
    counter = 0
    for i in range(len(disk)):
        
        if i % 2 == 1:
            append_n_times(disk[i], '.', decompressed)

        if i % 2 == 0:
            append_n_times(disk[i], counter, decompressed)
            counter += 1
    
    return decompressed

def is_gap_in_decompressed(decompressed):
    for i in range(len(decompressed)-1):
        if decompressed[i] == '.' and decompressed[i+1] != '.':
            return True
    return False


def get_last_number_index_with_limit(decompressed, limit):
    for i in range(len(decompressed)-1, limit, -1):
        if decompressed[i] != '.':
            return i
    return None

def swap_first_gap_and_last_number(decompressed):
    for i in range(len(decompressed)):
        if decompressed[i] == '.' and is_gap_in_decompressed(decompressed[i:]):
            last = get_last_number_index_with_limit(decompressed, i)
            decompressed[i], decompressed[last] = decompressed[last], decompressed[i]

    return decompressed

def checksum(decompressed):
    checksum = 0
    for i in range(len(decompressed)):
        if decompressed[i] == '.':
            break
        
        checksum += i * int(decompressed[i])
    return checksum

if __name__ == '__main__':
    
    with open('input.txt') as f:
        lines = f.read().splitlines()
        disk = []
        for line in lines:
            for char in line:
                disk.append(int(char))
    
    decompressed = decompress(disk)
    pretty_print(decompressed)
    decompressed = swap_first_gap_and_last_number(decompressed)
    print(checksum(decompressed))

    # 00...111...2...333.44.5555.6666.777.888899