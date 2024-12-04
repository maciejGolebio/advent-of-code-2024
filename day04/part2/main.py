def is_mas_x_shape(matrix, i, j):
    count_m = 0
    count_s = 0
    if matrix[i-1][j-1] == "M":
        count_m += 1
    if matrix[i-1][j+1] == "M":
        count_m += 1
    if matrix[i+1][j-1] == "M":
        count_m += 1
    if matrix[i+1][j+1] == "M":
        count_m += 1
    
    if matrix[i-1][j-1] == "S":
        count_s += 1
    if matrix[i-1][j+1] == "S":
        count_s += 1
    if matrix[i+1][j-1] == "S":
        count_s += 1
    if matrix[i+1][j+1] == "S":
        count_s += 1

    if count_m != 2 or count_s != 2:
        return False

    small_matrix = [[matrix[i - 1][j - 1], matrix[i - 1][j + 1]], [matrix[i + 1][j - 1], matrix[i + 1][j + 1]]]
    if small_matrix[0][0] == small_matrix[1][1]:
        return False
    if small_matrix[0][1] == small_matrix[1][0]:
        return False
    
    return True
    


if __name__ == "__main__":
    xmas_matrix = []
    with open("input.txt") as f:
        lines = f.readlines()
        for line in lines:
            line_to_list = []
            for i in line.strip():
                line_to_list.append(i)

            xmas_matrix.append(line_to_list)

    response = 0

    for i in range(1, len(xmas_matrix) - 1):
        for j in range(1, len(xmas_matrix[i]) - 1):
            if xmas_matrix[i][j] == "A":
                response += int(is_mas_x_shape(xmas_matrix, i, j))

    print(response)
