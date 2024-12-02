def is_previous_fine(previous, current, direction):
    if direction == 'increasing':
        return int(previous) <= int(current) and 1 <= (int(current) - int(previous)) <= 3 
    else:
        return int(previous) >= int(current) and 1 <= (int(previous) - int(current)) <= 3 

def guess_direction(report_line):
    if is_previous_fine(report_line[0], report_line[1], 'increasing'):
        return 'increasing'
    elif is_previous_fine(report_line[0], report_line[1], 'decreasing'):
        return 'decreasing'
    else:
        return None

def is_valid_report(report):
    counter = 0
    for i in range(1, len(report)):
        direction = guess_direction(report[i])
        is_fine = True
        if direction is None:
            continue
        for j in range(1, len(report[i])):
            if not is_previous_fine(report[i][j-1], report[i][j], direction):
                is_fine = False
                break
        if is_fine:
            counter += 1
    return counter
if __name__ == '__main__':
    reports = []

    with open('./input.txt') as f:
        lines = f.readlines()
        for line in lines:
            reports.append(line.split(' '))
    
    result = is_valid_report(reports)
    print(result)