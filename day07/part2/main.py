from functools import reduce

MULT = 1
CONC = 2
ADD = 0
OPERATORS = [MULT, CONC, ADD]

def operate(a, b, operator):
    if operator == MULT:
        return a * b
    elif operator == CONC:
        return int(str(a) + str(b))
    elif operator == ADD:
        return a + b
    raise Exception("Invalid operator")

# True = add, False = multiply
permutations = {
    1: [[MULT], [CONC], [ADD]],
}
permutations_higher_key = 1

def get_permutation_list(input_list):
    global permutations_higher_key
    global permutations

    perm_len = len(input_list) - 1

    if permutations.get(perm_len):
        return permutations.get(perm_len)

    # populate permutations for lengths > 1
    while permutations_higher_key < perm_len:
        permutations[permutations_higher_key + 1] = []
        for perm in permutations[permutations_higher_key]:
            for operator in OPERATORS:
                permutations[permutations_higher_key + 1].append(perm + [operator])
        permutations_higher_key += 1

    return permutations.get(perm_len)


def is_correct_input(expected, test_input):
    
    if len(test_input) == 1:
        return test_input[0] == expected

    permutation_list = get_permutation_list(test_input)
    for perm in permutation_list:
        result = test_input[0]
        for i in range(len(perm)):
            result = operate(result, test_input[i + 1], perm[i])

        if result == expected:
            print(f"Permutation {perm} is correct for {test_input} = {expected}")
            return True

    return False


if __name__ == "__main__":
    test_data = []
    with open("input.txt", "r") as file:
        for line in file:
            expected, test_input_str = line.split(":")
            expected = int(expected.strip())
            test_input = [int(x) for x in test_input_str.strip().split()]
            test_data.append((expected, test_input))

    print("Test cases:", test_data)
    result_sum = 0
    for expected, test_input in test_data:
        if is_correct_input(expected, test_input):
            result_sum += expected
            print(f"Test passed for {expected}: {test_input}")

    print(f"Result: {result_sum}")