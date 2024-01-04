import copy
import sys
import time

import pygame

pygame.init()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пентаго")
screen.fill((255, 255, 255))
end_flag = False
cell_flag, rotate_flag = True, False
winner = ''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (100, 0, 0)
button_color = (200, 200, 200)
green_color = (0, 255, 0)
field_color = (150, 0, 0)
CELL_SIZE = 125
GRID_SIZE = 3
GRID_PADDING = 10
CELL_PADDING = 20
last_move = 'rotate'
button_size = 100
button_radius = button_size // 2
board = [[['', '', ''],
          ['', '', ''],
          ['', '', '']],
         [['', '', ''],
          ['', '', ''],
          ['', '', '']],
         [['', '', ''],
          ['', '', ''],
          ['', '', '']],
         [['', '', ''],
          ['', '', ''],
          ['', '', '']]]

user_move = 'X'
ai_move = 'O'


def main_func():
    def draw_board():
        global clockwise_buttons, counter_clockwise_buttons
        screen.fill(WHITE)
        # Отрисовка поля
        pygame.draw.rect(screen, field_color, ((100, 100), (600, 600)))

        # Размер и радиус кнопок
        button_size = 100
        button_radius = button_size // 2

        for grid in range(4):
            for row in range(3):
                for col in range(3):
                    if grid == 0:
                        x, y = 150, 150
                    elif grid == 1:
                        x, y = 450, 150
                    elif grid == 2:
                        x, y = 150, 450
                    elif grid == 3:
                        x, y = 450, 450
                    x += col * 100
                    y += row * 100
                    if board[grid][row][col] == 'X':
                        pygame.draw.circle(screen, WHITE, (x, y), 40)
                    elif board[grid][row][col] == 'O':
                        pygame.draw.circle(screen, BLACK, (x, y), 40)
                    else:
                        pygame.draw.circle(screen, DARK_RED, (x, y), 30)
        pygame.draw.line(screen, WHITE, (400, 100), (400, 700), 5)
        pygame.draw.line(screen, WHITE, (100, 400), (700, 400), 5)
        clockwise_buttons = []

        counter_clockwise_buttons = []

        button_positions = [
            (50, 150),
            (150, 50),
            (650, 50),
            (750, 150),
            (50, 650),
            (150, 750),
            (650, 750),
            (750, 650)
        ]
        # Отрисовка кнопок
        for i in range(8):
            position = button_positions[i]
            if i % 2 == 0:
                clockwise_button = pygame.draw.circle(screen, button_color, position, button_radius)
                clockwise_buttons.append(clockwise_button)
            else:
                counter_clockwise_button = pygame.draw.circle(screen, button_color, position, button_radius)
                counter_clockwise_buttons.append(counter_clockwise_button)
        pygame.display.flip()

    def check_win(board):
        # Проверка главной диагонали
        sp = [board[0][0] + board[1][0]], [board[0][1] + board[1][1]], [board[0][2] + board[1][2]], [
            board[2][0] + board[3][0]], [board[2][1] + board[3][1]], [board[2][2] + board[3][2]]
        for i in range(2):
            for j in range(2):
                if sp[i][0][j] == sp[i + 1][0][j + 1] == sp[i + 2][0][j + 2] == sp[i + 3][0][j + 3] == sp[i + 4][0][
                    j + 4] and sp[i][0][j] != '':
                    return (True, sp[i][0][j])
        # Проверка добавочной диагонали
        for i in range(2):
            for j in range(2):
                if sp[i][0][j + 4] == sp[i + 1][0][j + 3] == sp[i + 2][0][j + 2] == sp[i + 3][0][j + 1] == sp[i + 4][0][
                    j] and sp[i][0][j + 4] != '':
                    return (True, sp[i][0][j + 4])
        # Проверка горизонталей
        for i in range(6):
            for j in range(2):
                if sp[i][0][j] == sp[i][0][j + 1] == sp[i][0][j + 2] == sp[i][0][j + 3] == sp[i][0][j + 4] and sp[i][0][
                    j] != '':
                    return (True, sp[i][0][j])
        # Проверка вертикалей
        for i in range(2):
            for j in range(6):
                if sp[i][0][j] == sp[i + 1][0][j] == sp[i + 2][0][j] == sp[i + 3][0][j] == sp[i + 4][0][j] and sp[i][0][
                    j] != '':
                    return (True, sp[i][0][j])
        return (False, '')

    def minimax(field, depth, flag, max_depth):
        if check_win(field) == (True, 'O'):
            return 100
        if check_win(field) == (True, 'X'):
            return -100
        if depth >= max_depth:
            return 0
        if flag:
            best_score = -sys.maxsize
            for grid in range(4):
                for row in range(3):
                    for col in range(3):
                        if field[grid][row][col] == '':
                            field[grid][row][col] = 'O'
                            score = minimax(field, depth + 1, False, 2)
                            field[grid][row][col] = ''
                            best_score = max(best_score, score)
        else:
            best_score = sys.maxsize
            for grid in range(4):
                for row in range(3):
                    for col in range(3):
                        if field[grid][row][col] == '':
                            field[grid][row][col] = 'X'
                            for quot in range(0, 4):  #
                                for direct in range(2):  #
                                    field_copy = copy.deepcopy(field)  #
                                    if direct == 0:  #
                                        rotate_clockwise(field, quot)  #
                                    else:  #
                                        rotate_counter_clockwise(field, quot)  #
                                    score = minimax(field, depth + 1, True, 2)
                                    best_score = min(best_score, score)
                            field[grid][row][col] = ''
        return best_score

    def get_computer_position(board):
        field = copy.deepcopy(board)
        best_score = -sys.maxsize
        move = None
        for grid in range(4):
            for row in range(3):
                for col in range(3):
                    if field[grid][row][col] == '':
                        field[grid][row][col] = 'O'
                        for quot in range(0, 4):  #
                            for direct in range(2):  #
                                field_copy = copy.deepcopy(field)  #
                                if direct == 0:  #
                                    rotate_clockwise(field, quot)  #
                                else:  #
                                    rotate_counter_clockwise(field, quot)  #
                                score = minimax(field, 0, False, 2)
                                if score >= best_score:
                                    best_score = score
                                    move = (grid, row, col, quot, direct)
                                field = copy.deepcopy(field_copy)  #
                        field[grid][row][col] = ''
                    print(4 - grid, 3 - row, 3 - col)
        return move

    scores = {'X': -100,
              '0': 100}

    def show_text(text):
        pygame.init()
        screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Text Window")
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 400))

        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        time.sleep(3)

        pygame.QUIT

    def rotate_clockwise(board, grid):
        copied = copy.deepcopy(board)
        board[grid] = [list(row) for row in zip(*board[grid][::-1])]
        board[grid] = [list(row) for row in zip(*board[grid][::-1])]
        board[grid] = [list(row) for row in zip(*board[grid][::-1])]
        return [board, copied]

    def rotate_counter_clockwise(board, grid):
        copied = copy.deepcopy(board)
        board[grid] = [list(row) for row in zip(*board[grid][::-1])]
        return [board, copied]

    rotate_flag = False
    cell_flag = False
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            result = check_win(board)
            end_flag, winner = result[0], result[1]
            if end_flag:
                if winner == 'X':
                    winner = 'Человек'
                else:
                    winner = 'Компьютер'
                message = f"Игрок {winner} победил!"
                show_text(message)
                pygame.QUIT
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not cell_flag:
                    pos = pygame.mouse.get_pos()
                    grid = 100
                    if 100 <= pos[0] <= 400 and 100 <= pos[1] <= 400:
                        grid = 0
                        row_x = (pos[1] - 100) // 100
                        row_y = (pos[0] - 100) // 100
                    elif 400 <= pos[0] <= 700 and 100 <= pos[1] <= 400:
                        grid = 1
                        row_x = (pos[1] - 100) // 100
                        row_y = (pos[0] - 400) // 100
                    elif 100 <= pos[0] <= 400 and 400 <= pos[1] <= 700:
                        grid = 2
                        row_x = (pos[1] - 400) // 100
                        row_y = (pos[0] - 100) // 100
                    elif 400 <= pos[0] <= 700 and 400 <= pos[1] <= 700:
                        grid = 3
                        row_x = (pos[1] - 400) // 100
                        row_y = (pos[0] - 400) // 100
                    if grid <= 3:
                        if board[grid][row_x][row_y] == '':
                            board[grid][row_x][row_y] = 'X'
                            cell_flag = True
                elif not rotate_flag:
                    for grid, clockwise_button in enumerate(clockwise_buttons):
                        if clockwise_button.collidepoint(event.pos):
                            rotate_clockwise(board, grid)
                            rotate_flag = True
                            break
                    else:
                        for grid, counter_clockwise_button in enumerate(counter_clockwise_buttons):
                            if counter_clockwise_button.collidepoint(event.pos):
                                rotate_counter_clockwise(board, grid)
                                rotate_flag = True
                                break

                draw_board()
                if rotate_flag and cell_flag:
                    a = get_computer_position(board)
                    grid, row, col, quot, direct = a[0], a[1], a[2], int(a[3]), a[4]
                    board[int(grid)][int(row)][int(col)] = 'O'
                    if direct == 0:  #
                        rotate_clockwise(board, quot)  #
                    else:  #
                        rotate_counter_clockwise(board, quot)
                    cell_flag, rotate_flag = False, False
                    draw_board()


if __name__ == '__main__':
    main_func()
