import pygame
import math
import numpy as np
pygame.font.init()

# Initialize global variables
WIDTH = 800
DARK_BLUE = (58, 145, 181)
LIGHT_BLUE = (129, 198, 227)
DARK_GREEN = (64, 125, 88)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (96, 224, 147)
GREY = (128, 128, 128)
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Backtracking Algorithm")
STAT_FONT = pygame.font.SysFont("comicsans", 25)

# Define class for each colored block
class Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width

        # starting position of the drawn cubes
        self.x = row * width
        self.y = col * width

        # initialize all blocks to white
        self.color = WHITE
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.score = ''

    def get_pos(self):
        return self.col, self.row

    def is_path(self):
        return self.color == DARK_BLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == LIGHT_GREEN

    def is_end(self):
        return self.color == DARK_GREEN
    
    def is_empty(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = LIGHT_GREEN

    def make_path(self):
        if not self.is_start() and not self.is_end():
            self.color = DARK_BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = DARK_GREEN

    # draw the cube
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

# initialize the grid
def make_grid(num_rows, width):
    grid = []
    gap = width // num_rows
    for i in range(num_rows):
        grid.append([])
        for j in range(num_rows):
            block = Block(i, j, gap)
            grid[i].append(block)

    return grid


def draw_grid(win, num_rows, width):
    gap = width // num_rows
    for i in range(num_rows):
        # draw a horizontal line to separate every row
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))

    for j in range(num_rows):
        # draw a vertical line to separate every column
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))
# draw the grids and each spots

def draw_connections(win, num_rows, width, connection_list):
    gap = width // num_rows
    
    for i in range(len(connection_list) - 1):
        cur_y, cur_x = connection_list[i].get_pos()
        next_y, next_x = connection_list[i+1].get_pos()
        pygame.draw.line(win, RED, (cur_x*gap + gap/2, cur_y*gap + gap/2),
                         (next_x*gap + gap/2, next_y*gap + gap/2))


def draw(win, grid, num_rows, width, score, connection_list):
    # win.fill(WHITE)

    for row in grid:
        for block in row:
            block.draw(win)

    draw_grid(win, num_rows, width)
    draw_connections(win, num_rows, width, connection_list)
    text = STAT_FONT.render("Path Count: " + str(score), 1, (0, 0, 0))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()
# helper function to return row and col number from coordinates


def get_clicked_pos(pos, num_rows, width):
    gap = width // num_rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


# ---------------------------- Main Functions for the Backtracking Algorithm ----------------------------
def isValid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_empty():
                return False
    return True


def backtrackSolve(win, num_rows, width, grid, pos, score_container, connection_list):
    # Add option to quit PyGame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    row = pos[0]
    col = pos[1]

    if grid[row][col].is_end():
        if isValid(grid):
            score_container[0] += 1
            draw(win, grid, num_rows, width, score_container[0], connection_list)
            pygame.time.wait(1000)
            return True
        else:
            return False

    # Up
    if row - 1 >= 0:
        if not grid[row-1][col].is_barrier() and not grid[row-1][col].is_path() and not grid[row-1][col].is_start():
            if not grid[row-1][col].is_end():
                grid[row-1][col].make_path()
            
            connection_list.append(grid[row-1][col])
            backtrackSolve(win, num_rows, width, grid,
                           (row-1, col), score_container, connection_list)
            connection_list.pop()
            
            if not grid[row-1][col].is_end():
                grid[row-1][col].reset()

    # Down
    if row + 1 < len(grid):
        if not grid[row+1][col].is_barrier() and not grid[row+1][col].is_path() and not grid[row+1][col].is_start():
            if not grid[row+1][col].is_end():
                grid[row+1][col].make_path()
            
            connection_list.append(grid[row+1][col])
            backtrackSolve(win, num_rows, width, grid,
                           (row+1, col), score_container, connection_list)
            connection_list.pop()
            
            if not grid[row+1][col].is_end():
                grid[row+1][col].reset()

    # Left
    if col - 1 >= 0:
        if not grid[row][col-1].is_barrier() and not grid[row][col-1].is_path() and not grid[row][col-1].is_start():
            if not grid[row][col-1].is_end():
                grid[row][col-1].make_path()
            
            connection_list.append(grid[row][col-1])
            backtrackSolve(win, num_rows, width, grid,
                           (row, col-1), score_container, connection_list)
            connection_list.pop()
            
            if not grid[row][col-1].is_end():
                grid[row][col-1].reset()

    # Right
    if col + 1 < len(grid[0]):
        if not grid[row][col+1].is_barrier() and not grid[row][col+1].is_path() and not grid[row][col+1].is_start():
            if not grid[row][col+1].is_end():
                grid[row][col+1].make_path()
            
            connection_list.append(grid[row][col+1])
            backtrackSolve(win, num_rows, width, grid,
                           (row, col+1), score_container, connection_list)
            connection_list.pop()
            
            if not grid[row][col+1].is_end():
                grid[row][col+1].reset()

    return False

def backtrackPathfinder(win, width, grid, start, end, num_rows):
    connection_list = []
    
    # Must be kept inside a mutable
    score_container = [0]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].is_start():
                start_row = i
                start_col = j
    
    connection_list.append(grid[start_row][start_col])

    backtrackSolve(win, num_rows, width, grid, (start_row, start_col), score_container, connection_list)
    return score_container[0]

# -------------------------- End of Functions for the Backtracking Algorithm --------------------------


def main(win, width):
    pygame.init()
    num_rows = 5
    grid = make_grid(num_rows, width)
    score = 0

    # player decides start and end location
    start = None
    end = None

    run = True
    started = False
    finished = False

    while run:
        if not started:
            draw(win, grid, num_rows, width, score, [])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # prevent user from triggering events when algorithm is underway
            if started and not finished:
                continue

            # [0] indicates left mouse button
            if not started:
                if pygame.mouse.get_pressed()[0]:
                    # obtains mouse position
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, num_rows, width)

                    # access the block object
                    block = grid[row][col]

                    # if the "starting" block has not been initialized, set it first
                    if not start and block != end:
                        start = block
                        start.make_start()

                    # if the "end" block has not been initialized, set it second
                    elif not end and block != start:
                        end = block
                        end.make_end()

                    # next, just initialize all the barriers
                    elif block != start and block != end:
                        block.make_barrier()

                # [2] indicates right mouse button to reset spots
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, num_rows, width)
                    block = grid[row][col]
                    block.reset()
                    if block == start:
                        start = None
                    if block == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                # Click space to trigger the algorithm
                if event.key == pygame.K_SPACE and not started and start and end:
                    started = True
                    score = 0
                    backtrackPathfinder(win, width, grid, start, end, num_rows)
                    finished = True

                # Click escape to restart the grid
                if event.key == pygame.K_ESCAPE and started:
                    # reset and empty grid
                    for i in range(num_rows):
                        for k in range(num_rows):
                            block = grid[i][k]
                            block.reset()
                    score = 0
                    draw(win, grid, num_rows, width, score, [])
                    started = False
                    finished = False
                    start = None
                    end = None
    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
