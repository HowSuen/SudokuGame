def printBoard(bo):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end = "")

def findEmpty(bo):
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return (i, j)

def isValid(bo, num, pos):
    #Check row
    for i in range(9):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    #Check col
    for j in range(9):
        if bo[j][pos[1]] == num and pos[0] != i:
            return False
    
    #Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    
    return True

def solve(bo):
    find = findEmpty(bo)
    if not find:
        return True
    row, col = find
    for i in range(1, 10):
        if isValid(bo, i, find):
            bo[row][col] = i
            if solve(bo):
                return True
            else:
                bo[row][col] = 0
    return False


board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0], 
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# printBoard(board)
solve(board)
printBoard(board)