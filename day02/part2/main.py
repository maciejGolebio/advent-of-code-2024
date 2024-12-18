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

def is_safe(report_line):
    direction = guess_direction(report_line)
    if direction is None:
        return False
    
    for j in range(1, len(report_line)):
        if not is_previous_fine(report_line[j-1], report_line[j], direction):
            return False
                
    return True
        

def count_safe_reports(reports):
    counter = 0
    for report_line in reports:
        if is_safe(report_line):
            counter += 1
        else:
            for j in range(0, len(report_line)):
                modified = report_line[:j] + report_line[j+1:]
                if is_safe(modified):
                    counter += 1
                    break
    return counter


if __name__ == '__main__':
    reports = []

    with open('./input.txt') as f:
        lines = f.readlines()
        for line in lines:
            reports.append([int(x) for x in line.split(' ')])

    
    result = count_safe_reports(reports)
    print(result)