import random

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
        if bo[j][pos[1]] == num and pos[0] != j:
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

def oneBoxFilled():
    result = [[0] * 9 for i in range(9)]
    for i in range(3):
        for j in range(3):
            if result[i][j] == 0:
                ranInt = random.randint(1, 9)
                while not isValid(result, ranInt, (i, j)):
                    ranInt = random.randint(1, 9)
                result[i][j] = ranInt
    return result

def generate(difficulty):
    puzzle = oneBoxFilled()
    solve(puzzle)
    k = 40 # number of clues removed
    if difficulty == 0: # Easy - 41 clues
        k = 40
    elif difficulty == 1: # Medium - 30 clues
        k = 51
    elif difficulty == 2: # Hard - 21 clues
        k = 60
    for i in range(k):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        while puzzle[x][y] == 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
        puzzle[x][y] = 0
    return puzzle

board = generate(2) # Hard Difficulty
printBoard(board)
print("======================")
solve(board)
printBoard(board)