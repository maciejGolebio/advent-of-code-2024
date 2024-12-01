left_locations = []
right_locations = []

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        l = "-".join(line.split())
        left, right = l.split("-")
        left_locations.append(left)
        right_locations.append(right)

counted_right_locations = {}
for right in right_locations:
    if int(right) in counted_right_locations:
        counted_right_locations[int(right)] += 1
    else:
        counted_right_locations[int(right)] = 1

cumulative_similarity = 0

for left in left_locations:
    cumulative_similarity = cumulative_similarity + (counted_right_locations.get(int(left), 0) * int(left))

print(cumulative_similarity)