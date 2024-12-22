from typing import List, Tuple


data = []
with open("input.txt") as file:
    for line in file.readlines():
        data.append(int(line.strip()))

mix = lambda value, secret: value ^ secret
prune = lambda secret: secret & (16777216 - 1)

assert mix(42, 15) == 37
assert prune(100000000) == 16113920

mix_and_prune = lambda value, secret: prune(mix(value, secret))


def next_secret(secret: int) -> int:
    # step 1
    tmp = secret << 6  # 64
    secret = mix_and_prune(secret, tmp)
    # step 2
    tmp = round(secret >> 5)  # 32
    secret = mix_and_prune(secret, tmp)
    # step 3
    tmp = secret << 11  # 2048
    secret = mix_and_prune(secret, tmp)
    return secret


def get_secret_last_digit(secret: int) -> int:
    return int(str(secret)[-1])


def get_Nth_secret(secret: int, N: int) -> Tuple[int, List[int], List[int]]:
    prices = [get_secret_last_digit(secret)]
    changes = [None]
    previous_last_digit = prices[0]
    for _ in range(N):
        secret = next_secret(secret)
        last_digit = get_secret_last_digit(secret)
        change = last_digit - previous_last_digit
        previous_last_digit = last_digit
        prices.append(last_digit)
        changes.append(change)
    return secret, prices, changes


order_book = {}


def prices_and_changes_to_dict(prices: List[int], changes: List[int]) -> dict:
    only_first = set()
    for i in range(1, len(prices) - 4):
        change_slice = tuple(changes[i : i + 4])
        if change_slice in order_book and change_slice not in only_first:
            order_book[change_slice] += prices[i + 3]
        elif change_slice not in order_book:
            order_book[change_slice] = prices[i + 3]
        only_first.add(change_slice)


# secret = 123
# secret, prices, changes = get_Nth_secret(secret, 10)
# prices_and_changes_to_dict(prices, changes)
# print(order_book)

for i, d in enumerate(data):
    secret, prices, changes = get_Nth_secret(d, 2000)
    prices_and_changes_to_dict(prices, changes)
    print(f"Secret {i} is from {len(data)-1}")

best = 0
best_key = None
for k, v in order_book.items():
    if v > best:
        best = v
        best_key = k

print(best_key, best)

# 466 too low
