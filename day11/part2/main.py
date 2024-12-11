from functools import cache


@cache
def blink(stone, blinks):
    if blinks == 0:
        return 1

    if stone == 0:
        return blink(1, blinks - 1)
    
    str_stone = str(stone)
    
    if len(str_stone) % 2 == 0:
        middle = len(str_stone) // 2
        return blink(int(str_stone[:middle]), blinks - 1) + blink(
            int(str_stone[middle:]), blinks - 1
        )

    return blink(stone * 2024, blinks - 1)


if __name__ == "__main__":
    import sys

    BLINKS = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    stones = [890, 0, 1, 935698, 68001, 3441397, 7221, 27]
    result = 0
    for stone in stones:
        partial_result = blink(stone, BLINKS)
        result += partial_result
        print(
            f"Stone: {stone} Current Result: {result}  Partial Result: {partial_result}"
        )

    print(f"Result: {result}")