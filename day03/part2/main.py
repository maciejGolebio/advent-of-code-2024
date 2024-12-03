import re

pattern_mul = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
pattern_doable = re.compile(r'do\(\)')
patten_not_doable = re.compile(r'don\'t\(\)')

class Indexed:
    def __init__(self, index):
        self.index = index

class Mul(Indexed):
    def __init__(self, a, b, start_index):
        self.a = a
        self.b = b
        self.index = start_index

    def __str__(self):
        return f'Mul(index = {self.index} | {self.a}, {self.b})'


class Doable(Indexed):
    def __init__(self, start_index, is_doable):
        self.index = start_index
        self.is_doable = is_doable
    
    def __str__(self):
        return f'Doable(index = {self.index} | {self.is_doable})'



if __name__ == '__main__':
    operations = []


    with open('input.txt') as f:
        lines = f.readlines()
        base_index = 0
        for line in lines:
            matched = pattern_mul.search(line)
            while matched:
                operations.append(Mul(matched.group(1), matched.group(2), base_index + matched.start()))
                matched = pattern_mul.search(line, matched.end())

            matched_do = pattern_doable.search(line)
            while matched_do:
                operations.append(Doable(base_index + matched_do.start(), True))
                index = matched_do.end()
                matched_do = pattern_doable.search(line, matched_do.end())

            matched_not_do = patten_not_doable.search(line)
            while matched_not_do:
                operations.append(Doable(base_index + matched_not_do.start(), False))
                if matched_not_do.end() > index:
                    index = matched_not_do.end()
                matched_not_do = patten_not_doable.search(line, matched_not_do.end())

            base_index += len(line)

    operations.sort(key=lambda x: x.index)
    
    is_blocked = False
    result = 0
    for operation in operations:
        print(operation)
        if isinstance(operation, Mul):
            if not is_blocked:
                result += int(operation.a) * int(operation.b)
        elif isinstance(operation, Doable):
            is_blocked = not operation.is_doable

    print(result)