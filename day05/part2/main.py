def are_in_order(array, expected_before, expected_after):
    if expected_before in array and expected_after in array:
        if array.index(expected_before) < array.index(expected_after):
            return True
    return False


def swap_elements(array, first, second):
    array[array.index(first)], array[array.index(second)] = (
        array[array.index(second)],
        array[array.index(first)],
    )


def fix_order(array, rules_before):
    changed = True
    while changed:
        changed = False
        for i in range(len(array)):
            element = array[i]
            if element in rules_before:
                for rule in rules_before[element]:
                    if rule not in array:
                        continue
                    if not are_in_order(array, element, rule):
                        print(f"Swapping {element} and {rule}")
                        swap_elements(array, element, rule)
                        changed = True
                        break
                if changed:
                    break  

def is_order_correct(array, rules_before):
    for element in array:

        if element in rules_before:
            for rule in rules_before[element]:
                if rule not in array:
                    continue
                if are_in_order(array, element, rule):
                    print(f"Element {element} is before {rule}")
                else:
                    print(f"Element {element} is not before {rule}")
                    return False
    return True


def find_middle_element_in_array(array):
    middle = array[len(array) // 2]
    print(f"Middle element is {middle}")
    return middle


if __name__ == "__main__":
    order_rules = []
    pages = set()
    rules_before = {}
    # rules_after = {}
    with open("inputA.txt") as f:
        lines = f.readlines()
        for line in lines:
            before, after = line.strip().split("|")
            order_rules.append((int(before), int(after)))
            pages.add(int(before))
            pages.add(int(after))
            if rules_before.get(int(before)):
                rules_before[int(before)].append(int(after))
            else:
                rules_before[int(before)] = [int(after)]

            # if rules_after.get(int(after)):
            #     rules_after[int(after)].append(int(before))
            # else:
            #     rules_after[int(after)] = [int(before)]

    manuals = []
    with open("inputB.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = [int(x) for x in line.strip().split(",")]
            ignore = False
            for x in line:
                if x not in pages:
                    print(f"Page {x} not in pages")
                    ignore = True
                    break
            if not ignore:
                manuals.append(line)

    counter = 0
    
    for index in range(len(manuals)):
        if is_order_correct(manuals[index], rules_before):
            print("line is correct\n\n")
            # counter += find_middle_element_in_array(manuals[index])
        else:
            fix_order(manuals[index], rules_before)
            print(f"Fixed line {manuals[index]}\n\n")
            counter += find_middle_element_in_array(manuals[index])
    print(counter)

# 75,97,47,61,53 becomes 97,75,47,61,53.
# 61,13,29 becomes 61,29,13.
# 97,13,75,29,47 becomes 97,75,47,29,13.
