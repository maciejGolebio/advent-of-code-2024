
LEVEL = 1

def debug_log(*args):
    if LEVEL == 0:
        print(*args)
    

def is_row_xmas(matrix, i, j):
    counter = 0
    if j + 3 < len(matrix[i])  and matrix[i][j] == 'X' and matrix[i][j + 1] == 'M' and matrix[i][j + 2] == 'A' and matrix[i][j + 3] == 'S':
        debug_log('row natural')
        counter += 1

    if j - 3 >= 0 and matrix[i][j] == 'X' and matrix[i][j - 1] == 'M' and matrix[i][j - 2] == 'A' and matrix[i][j - 3] == 'S':
        debug_log('row reverse')
        counter += 1
    return counter

def is_vertical_xmas(matrix, i, j):
    counter = 0
    if i + 3 < len(matrix) and matrix[i][j] == 'X' and matrix[i + 1][j] == 'M' and matrix[i + 2][j] == 'A' and matrix[i + 3][j] == 'S':
        debug_log('vertical natural')
        counter += 1

    if i - 3 >= 0 and matrix[i][j] == 'X' and matrix[i - 1][j] == 'M' and matrix[i - 2][j] == 'A' and matrix[i - 3][j] == 'S':
        debug_log('vertical reverse')
        counter += 1
    return counter

def is_diagonal_xmas(matrix, i, j):
        counter = 0
        if i + 3 < len(matrix) and j + 3 < len(matrix[i]) and matrix[i][j] == 'X' and matrix[i + 1][j + 1] == 'M' and matrix[i + 2][j + 2] == 'A' and matrix[i + 3][j + 3] == 'S':
            debug_log('diagonal i+3 j+3')
            counter += 1
    
        if i - 3 >= 0 and j - 3 >= 0 and matrix[i][j] == 'X' and matrix[i - 1][j - 1] == 'M' and matrix[i - 2][j - 2] == 'A' and matrix[i - 3][j - 3] == 'S':
            debug_log('diagonal i-3 j-3')
            counter += 1
    
        if i + 3 < len(matrix) and j - 3 >= 0 and matrix[i][j] == 'X' and matrix[i + 1][j - 1] == 'M' and matrix[i + 2][j - 2] == 'A' and matrix[i + 3][j - 3] == 'S':
            debug_log('diagonal i+3 j-3')
            counter += 1
    
        if i - 3 >= 0 and j + 3 < len(matrix[i]) and matrix[i][j] == 'X' and matrix[i - 1][j + 1] == 'M' and matrix[i - 2][j + 2] == 'A' and matrix[i - 3][j + 3] == 'S':
            debug_log('diagonal i-3 j+3')
            counter += 1
        return counter

def count_xmas_index(matrix, i, j):
    index_counter = is_row_xmas(matrix, i, j)
    index_counter += is_vertical_xmas(matrix, i, j)
    index_counter += is_diagonal_xmas(matrix, i, j)
    return index_counter

if __name__ == '__main__':
    xmas_matrix = []
    with open('input.txt') as f:
        lines = f.readlines()
        for line in lines:
            line_to_list = []
            for i in line.strip():
                line_to_list.append(i)

            xmas_matrix.append(line_to_list)


    response = 0

    for i in range(len(xmas_matrix)):
        for j in range(len(xmas_matrix[i])):
            if xmas_matrix[i][j] == 'X':
                try:
                    response += count_xmas_index(xmas_matrix, i, j)
                except:
                    debug_log(f'Error in count_xmas_index, index i: {i}, j: {j}')
                    raise Exception('Error in count_xmas_index')


    print(response)