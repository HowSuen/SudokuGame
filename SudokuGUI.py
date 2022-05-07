import pygame
import Sudoku
import time
import copy
pygame.font.init()

WIDTH, HEIGHT = 1000, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku!")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
ARIALBLACK_FONT = pygame.font.SysFont('arialblack', 40)
ARIAL_FONT = pygame.font.SysFont('arial', 30)
ARIAL_FONT_SMALL = pygame.font.SysFont('arial', 25)

# Grid
class Grid:
    def __init__(self, board, width, height):
        self.width = width
        self.height = height
        self.board = board
        self.grid = [[Box(j, i, board[j][i], width // 9) for i in range(9)] for j in range(9)]
        self.current = None
        self.original = copy.deepcopy(board)
        self.solved = copy.deepcopy(board)
        Sudoku.solve(self.solved)
    
    # Draw the 9x9 grid boxes
    def draw(self):
        gap = self.width // 9
        for i in range(10):
            thicc = 1
            if i % 3 == 0:
                thicc = 3
            pygame.draw.line(WIN, BLACK, (i * gap, 0), (i * gap, gap * 9), thicc)
            pygame.draw.line(WIN, BLACK, (0, i * gap), (gap * 9, i * gap), thicc)
        for i in range(9):
            for j in range(9):
                self.grid[i][j].draw()
    
    # Return the box clicked
    def click(self, pos):
        x, y = pos
        if x < self.width and y < self.height:
            j = x // (self.width // 9)
            i = y // (self.width // 9)
            return (i, j)
    
    # Select the chosen box
    def select(self, pos):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].selected = False
        self.grid[pos[0]][pos[1]].selected = True
        self.current = pos
    
    # Delete the temporary number
    def clear(self):
        x, y = self.current
        if self.grid[x][y].value == 0:
            self.grid[x][y].temp = 0
    
    # Key in the number in the grid box, returns True if correct, False otherwise
    def enter(self, x, y):
        if self.grid[x][y].value == 0:
            val = self.grid[x][y].temp
            print(val)
            self.grid[x][y].value = val
            self.board[x][y] = val
            if Sudoku.isValid(self.board, val, (x, y)) and Sudoku.solve(self.board):
                self.grid[x][y].temp = 0
                return True
            else:
                self.grid[x][y].value = 0
                self.board[x][y] = 0
                self.grid[x][y].temp = 0
                return False
    
    # Insert temporary number in the grid box
    def sketch(self, val):
        x, y = self.current
        self.grid[x][y].temp = val
    
    # Checks for any box in the grid that is not filled yet
    def isFinished(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value == 0:
                    return False
        return True

    # Reset the puzzle to its original state
    def resetBoard(self):
        self.board = self.original
        self.grid = [[Box(j, i, self.original[j][i], self.width // 9) for i in range(9)] for j in range(9)]

    # Solve the puzzle and fill empty grids with temporary numbers
    def solveBoard(self):
        self.board = self.solved
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value == 0:
                    self.grid[i][j].temp = self.board[i][j]

# Box
class Box:
    def __init__(self, row, col, value, gap):
        self.row = row
        self.col = col
        self.value = value
        self.gap = gap
        self.selected = False
        self.temp = 0

    # Draw the number in the grid box
    def draw(self):
        x = self.col * self.gap
        y = self.row * self.gap

        if self.value == 0 and self.temp != 0:
            text = ARIAL_FONT.render(str(self.temp), 1, GRAY)
            WIN.blit(text, (x + 5, y))
        elif self.value != 0:
            text = ARIALBLACK_FONT.render(str(self.value), 1, BLACK)
            WIN.blit(text, (x + self.gap // 2 - text.get_width() // 2, y + self.gap // 2 - text.get_height() // 2))
        
        if self.selected:
            pygame.draw.rect(WIN, RED, (x, y, self.gap, self.gap), 3)

# Show text in the middle of the screen
def draw_text(text, color):
    t = ARIALBLACK_FONT.render(text, 1, color)
    WIN.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - t.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Window
def draw_window(grid, strikes, total_time):
    WIN.fill(WHITE)
    # Board
    grid.draw()

    # Time
    time = ARIAL_FONT.render('Time: ' + str(total_time), 1, BLACK)
    WIN.blit(time, (grid.width + 10, grid.height - 40))

    # Strikes
    text = ARIALBLACK_FONT.render('X ' * strikes, 1, RED)
    WIN.blit(text, (grid.width + 10, grid.height - 100))
    
    # Instructions
    TITLE = ARIALBLACK_FONT.render("SUDOKU!", 1, BLACK)
    WIN.blit(TITLE, (grid.width + (WIDTH - grid.width) // 2 - TITLE.get_width() // 2, 5))
    instructions = ["CONTROLS:", 
        "MOUSE: Choose the box", 
        "ENTER: Key in the number", 
        "BACKSPACE: Delete temporary number", 
        "F1: Generate new easy puzzle",
        "F2: Generate new medium puzzle",
        "F3: Generate new hard puzzle",
        "F5: Reset the puzzle", 
        "SPACEBAR: Solve the puzzle automatically"]
    for i in range(len(instructions)):
        s = instructions[i]    
        TEXT = ARIAL_FONT_SMALL.render(s, 1, BLACK)
        WIN.blit(TEXT, (grid.width + 10, 10 + TITLE.get_height() + i * (TEXT.get_height() + 5)))
    pygame.display.update()

def main():
    difficulty = 0
    board = Sudoku.generate(difficulty)
    grid = Grid(board, 540, 540)
    strikes = 0
    run = True
    key = None
    start_time = time.time()
    while run:

        total_time = round(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                box_selected = grid.click(pos)
                if box_selected:
                    grid.select(box_selected)
                    key = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    grid.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    if grid.current:
                        x, y = grid.current
                        if grid.grid[x][y].temp != 0:
                            if grid.enter(x, y):
                                print("Success")
                            else:
                                print("Wrong")
                                strikes += 1
                            key = None
                        if grid.isFinished():
                            text = "You win! Game Over!"
                            print(text)
                            draw_text(text, GREEN)
                            grid = Grid(Sudoku.generate(difficulty), 540, 540)
                            grid.resetBoard()
                            strikes = 0
                            start_time = time.time()
                if event.key == pygame.K_F5:
                    text = "Game Reset"
                    print(text)
                    draw_text(text, BLUE)
                    grid.resetBoard()
                    strikes = 0
                    start_time = time.time()
                if event.key == pygame.K_SPACE:
                    grid.solveBoard()
                if event.key == pygame.K_F1: # EASY DIFFICULTY
                    text = "EASY LEVEL"
                    print(text)
                    draw_text(text, GREEN)
                    difficulty = 0
                    grid = Grid(Sudoku.generate(difficulty), 540, 540)
                    grid.resetBoard()
                    strikes = 0
                    start_time = time.time()
                if event.key == pygame.K_F2: # MEDIUM DIFFICULTY
                    text = "MEDIUM LEVEL"
                    print(text)
                    draw_text(text, BLUE)
                    difficulty = 1
                    grid = Grid(Sudoku.generate(difficulty), 540, 540)
                    grid.resetBoard()
                    strikes = 0
                    start_time = time.time()
                if event.key == pygame.K_F3: # HARD DIFFICULTY
                    text = "HARD LEVEL"
                    print(text)
                    draw_text(text, RED)
                    difficulty = 2
                    grid = Grid(Sudoku.generate(difficulty), 540, 540)
                    grid.resetBoard()
                    strikes = 0
                    start_time = time.time()
        if grid.current and key:
            grid.sketch(key)
    
        draw_window(grid, strikes, total_time)
        if strikes >= 5:
            text = "You lose! Game Over!"
            print(text)
            draw_text(text, RED)
            grid = Grid(Sudoku.generate(difficulty), 540, 540)
            grid.resetBoard()
            strikes = 0
            start_time = time.time()

main()