import pygame
from sudoku.sudoku_square import SudokuSquare
from utils import SudokuUtils


def get_start_xy(col_index, row_index):
    if col_index in (0, 1, 2):
        start_x = (col_index * 57) + 38
    if col_index in (3, 4, 5):
        start_x = (col_index * 57) + 99
    if col_index in (6, 7, 8):
        start_x = (col_index * 57) + 159
    if row_index in (0, 1, 2):
        start_y = (row_index * 57) + 35
    if row_index in (3, 4, 5):
        start_y = (row_index * 57) + 100
    if row_index in (6, 7, 8):
        start_y = (row_index * 57) + 165

    return start_x, start_y


def get_sudoku_board(values):
    rows = 'ABCDEFGHI'
    cols = '123456789'
    the_squares = []

    for row_index in range(9):
        for col_index in range(9):
            start_x, start_y = get_start_xy(col_index, row_index)

            string_number = values[rows[row_index] + cols[col_index]]

            if len(string_number) > 1 or string_number == '' or string_number == '.':
                number = None
            else:
                number = int(string_number)

            the_squares.append(
                SudokuSquare(number, start_x, start_y, "N", col_index, row_index)
            )

    return the_squares


def play(values, result, history):
    size = (700, 700)

    sdk = SudokuUtils(history=history)
    assignments = sdk.reconstruct(result, sdk.history)
    pygame.init()

    screen = pygame.display.set_mode(size)

    background_image = pygame.image.load("./images/sudoku-board-bare.jpg").convert()

    clock = pygame.time.Clock()

    while True:
        pygame.event.pump()

        the_squares = get_sudoku_board(values)

        screen.blit(background_image, (0, 0))
        for num in the_squares:
            num.draw()

        pygame.display.flip()
        pygame.display.update()
        clock.tick(5)

        if len(assignments) == 0:
            break
        box, value = assignments.pop()
        values[box] = value

    # leave game showing until closed by user
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
