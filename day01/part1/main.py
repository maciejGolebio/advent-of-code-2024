
left_locations = []
right_locations = []

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        left, right = line.split('   ')
        left_locations.append(left)
        right_locations.append(right)

left_locations.sort()
right_locations.sort()

cumulative_distance = 0
for left, right in zip(left_locations, right_locations):
    cumulative_distance += abs(int(left) - int(right))

print(cumulative_distance)