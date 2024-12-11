def apply_rules(data):
    new_data = []
    for i in range(len(data)):
        if data[i] == 0:
            new_data.append(1)
            continue

        if len(str(data[i])) % 2 == 0:
            str_i = str(data[i])
            middle = len(str_i) // 2
            left, right = int(str_i[:middle]), int(str_i[middle:])
            new_data.append(left)
            new_data.append(right)
            continue

        new_data.append(data[i] * 2024)

    return new_data

if __name__ == "__main__":
    BLINKS = 25
    data = []
    with open("input.txt") as f:
        for line in f.read().splitlines():
            data = [int(x) for x in line.split(" ")]

    
    for i in range(BLINKS):
        data = apply_rules(data)
        print(f"Step {i + 1}: {len(data)}")
        # print(data)

    print(f"Result: {len(data)}")