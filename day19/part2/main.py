from typing import List, Tuple

def read_input(filename="input.txt") -> Tuple[List[str], List[str]]:
    with open(filename, "r") as file:
        lines = [l.strip() for l in file if l.strip()]
    patterns = lines[0].split(", ")
    designs = lines[1:]
    return patterns, designs

def count_ways(patterns: List[str], design: str) -> int:
    filtered_patterns = [p for p in patterns if any(c in design for c in p)]

    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(n):
        if dp[i] == 0:
            continue

        for pattern in filtered_patterns:
            
            plen = len(pattern)
            if i + plen <= n and design[i:i+plen] == pattern:
                dp[i+plen] += dp[i]
    
    return dp[n]

if __name__ == "__main__":
    patterns, designs = read_input("input.txt")

    total_ways = 0
    for i, design in enumerate(designs):
        ways = count_ways(patterns, design)
        total_ways += ways
        print(f"Progress: {i+1}/{len(designs)}")

    print(f"Total ways: {total_ways}")