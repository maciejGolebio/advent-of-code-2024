from typing import List, Tuple


def read_input(filename="input.txt") -> Tuple[List[str], List[str]]:
    with open(filename, "r") as file:
        lines = [l.strip() for l in file if l.strip()]
    patterns = lines[0].split(", ")
    designs = lines[2:]
    return patterns, designs


def can_be_built(patterns: List[str], design: str) -> bool:
    filtered_patterns = [p for p in patterns if any(c in design for c in p)]
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue

        for pattern in filtered_patterns:
            plen = len(pattern)

            if i + plen <= n and design[i : i + plen] == pattern:
                dp[i + plen] = True
    
    return dp[n]


if __name__ == "__main__":
    patterns, designs = read_input("input.txt")

    counter = 0
    
    for i, design in enumerate(designs):
        if can_be_built(patterns, design):
            counter += 1
        print(f"Progress: {i+1}/{len(designs)}")

    print(f"Counter: {counter}")
