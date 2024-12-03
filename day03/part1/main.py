import re

pattern = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
            

if __name__ == '__main__':
    result = 0 
    with open('input.txt') as f:
        lines = f.readlines()
        for line in lines:
            all_matched = pattern.findall(line)
            for matched in all_matched:
                result += int(matched[0]) * int(matched[1])

    print(result)