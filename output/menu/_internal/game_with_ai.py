import copy
import sys
import time
import random
import pygame
from button_class import ImageButton

pygame.init()
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пентаго")
screen.fill((255, 255, 255))
end_flag = False
cell_flag, rotate_flag = True, False
winner = ''
black_sphere = pygame.image.load("sphere-black.png")
white_sphere = pygame.image.load("sphere-white.png")
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
max_depth = 1
count = 0
arrow_img = pygame.image.load("arrow.png")
background_image = pygame.image.load("ai_background.png")
background_image = pygame.transform.scale(background_image, (800, 800))
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
button_size = 100
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
clockwise_buttons = []
counter_clockwise_buttons = []
button_radius = button_size // 2
for i in range(8):
    x, y = button_positions[i]
    x -= 50
    y -= 50
    if i >= 4:
        i += 1
    if i % 2 == 0:
        clockwise_button = ImageButton(x, y, 100, 100, '', "circle_before.png", "circle_after.png")
        clockwise_buttons.append(clockwise_button)
    else:
        counter_clockwise_button = ImageButton(x, y, 100, 100, '', "circle_before.png", "circle_after.png")
        counter_clockwise_buttons.append(counter_clockwise_button)
    i -= 1

user_move = 'X'
ai_move = 'O'


def main_func():
    global max_depth, count, board

    def mirror_image(image, mirror_axis):
        # Отражение картинки по заданной оси (остановка = 0, вертикальная = 1, горизонтальная = 2)
        mirrored_image = pygame.transform.flip(image, False, mirror_axis)
        return mirrored_image

    def rotate_image(image, angle):
        # Поворот картинки на заданный угол (в градусах)
        rotated_image = pygame.transform.rotate(image, angle)
        return rotated_image

    def draw_board():
        global clockwise_buttons, counter_clockwise_buttons
        screen.blit(background_image, (0, 0))
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
                        screen.blit(white_sphere, (x - 42, y - 42))
                    elif board[grid][row][col] == 'O':
                        screen.blit(black_sphere, (x - 42, y - 42))
                    else:
                        pygame.draw.circle(screen, DARK_RED, (x, y), 30)
        pygame.draw.line(screen, WHITE, (398, 100), (398, 700), 5)
        pygame.draw.line(screen, WHITE, (100, 398), (700, 398), 5)
        for el in clockwise_buttons:
            el.draw(screen)
        for el in counter_clockwise_buttons:
            el.draw(screen)
        screen.blit(arrow_img, (100, 0))
        screen.blit(mirror_image(rotate_image(arrow_img, 90), 1), (0, 100))
        screen.blit(mirror_image(rotate_image(arrow_img, 180), 1), (600, 0))
        screen.blit(rotate_image(arrow_img, 270), (700, 100))
        screen.blit(rotate_image(arrow_img, 90), (0, 600))
        screen.blit(mirror_image(arrow_img, 1), (100, 700))
        screen.blit(rotate_image(arrow_img, 180), (600, 700))
        screen.blit(rotate_image(mirror_image(arrow_img, 1), 90), (700, 600))
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

    def find_four(board):
        sp = [board[0][0] + board[1][0]], [board[0][1] + board[1][1]], [board[0][2] + board[1][2]], [
            board[2][0] + board[3][0]], [board[2][1] + board[3][1]], [board[2][2] + board[3][2]]
        for i in range(3):
            for j in range(3):
                if sp[i][0][j] == sp[i + 1][0][j + 1] == sp[i + 2][0][j + 2] == sp[i + 3][0][j + 3] and sp[i][0][
                    j] != '':
                    return (True, sp[i][0][j])
        # Проверка добавочной диагонали
        for i in range(3):
            for j in range(3):
                if sp[i][0][j + 3] == sp[i + 1][0][j + 2] == sp[i + 2][0][j + 1] == sp[i + 3][0][j] and sp[i][0][
                    j + 3] != '':
                    return (True, sp[i][0][j + 3])
        # Проверка горизонталей
        for i in range(6):
            for j in range(3):
                if sp[i][0][j] == sp[i][0][j + 1] == sp[i][0][j + 2] == sp[i][0][j + 3] and sp[i][0][j] != '':
                    return (True, sp[i][0][j])
        # Проверка вертикалей
        for i in range(3):
            for j in range(6):
                if sp[i][0][j] == sp[i + 1][0][j] == sp[i + 2][0][j] == sp[i + 3][0][j] and sp[i][0][j] != '':
                    return (True, sp[i][0][j])
        return (False, '')

    def find_triple_in_grid(board):
        count = 0
        for i in range(4):
            grid = board[i]
            for row in range(3):
                if grid[row][0] == grid[row][1] == grid[row][2] != '':
                    if grid[row][0] == 'O':
                        count += 10
                    else:
                        count -= 10
                if grid[0][row] == grid[1][row] == grid[2][row] != '':
                    if grid[0][row] == 'O':
                        count += 10
                    else:
                        count -= 10
                if grid[0][0] == grid[1][1] == grid[2][2] != '':
                    if grid[0][0] == 'O':
                        count += 5
                    else:
                        count -= 5
                if grid[0][2] == grid[1][1] == grid[2][0] != '':
                    if grid[0][2] == 'O':
                        count += 5
                    else:
                        count -= 5
        return count

    def get_rotate(board):
        for rotate in range(2):
            for quot in range(4):
                if rotate == 0:
                    if check_win(rotate_clockwise(board, quot)[0]) == (True, 'O'):
                        return (rotate, quot)
        return (random.choice([0, 1]), random.choice([0, 1, 2, 3]))

    def check_centers(board):
        count = 0
        flag = False
        for grid in range(4):
            if board[grid][1][1] == '':
                flag = True
            if board[grid][1][1] == 'O':
                count += 10
            if board[grid][1][1] == 'X':
                count -= 10
        if flag:
            return count
        return 0

    def minimax(field, depth, flag, max_depth, alpha=-sys.maxsize, beta=sys.maxsize):
        if check_win(field) == (True, 'O'):
            return 100
        if check_win(field) == (True, 'X'):
            return -100
        if check_centers(field) != 0:
            return check_centers(field)
        if find_triple_in_grid(field) != 0:
            return find_triple_in_grid(field)
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
                            alpha = max(alpha, best_score)
                            if beta <= alpha:
                                return best_score
            return best_score
        else:
            best_score = sys.maxsize
            for grid in range(4):
                for row in range(3):
                    for col in range(3):
                        if field[grid][row][col] == '':
                            field[grid][row][col] = 'X'
                            for quot in range(0, 4):
                                for direct in range(2):
                                    field_copy = copy.deepcopy(field)
                                    if direct == 0:
                                        rotate_clockwise(field, quot)
                                    else:
                                        rotate_counter_clockwise(field, quot)
                                    score = minimax(field, depth + 1, True, 2)
                                    best_score = min(best_score, score)
                                    beta = min(beta, best_score)
                                    if beta <= alpha:
                                        return best_score
                            field[grid][row][col] = ''
            return best_score

    def get_computer_position(board):
        field = copy.deepcopy(board)
        best_score = -sys.maxsize
        move = None
        sp_of_moves = []
        for grid in range(4):
            for row in range(3):
                for col in range(3):
                    if field[grid][row][col] == '':
                        field[grid][row][col] = 'O'
                        for quot in range(0, 4):
                            for direct in range(2):
                                field_copy = copy.deepcopy(field)
                                if direct == 0:
                                    rotate_clockwise(field, quot)
                                else:
                                    rotate_counter_clockwise(field, quot)
                                score = minimax(field, 0, False, 2)
                                move = (grid, row, col, quot, direct)
                                if score > best_score:
                                    best_score = score
                                    sp_of_moves = [move]
                                if score == best_score:
                                    sp_of_moves.append(move)
                                field = copy.deepcopy(field_copy)
                        field[grid][row][col] = ''
        return sp_of_moves

    scores = {'X': -100,
              '0': 100}

    def show_text(text):
        pygame.init()
        screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Text Window")
        screen.fill(WHITE)
        font = pygame.font.Font("Robotocondensed Regular.ttf", 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 400))

        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        time.sleep(3)

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
    running = True
    draw_board()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT
            result = check_win(board)
            end_flag, winner = result[0], result[1]
            if end_flag:
                if winner == 'X':
                    winner = 'Человек'
                else:
                    winner = 'Компьютер'
                message = f"Игрок {winner} победил!"
                draw_board()
                time.sleep(3)
                show_text(message)
                running = False
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
                        if clockwise_button.handle_event(event):
                            rotate_clockwise(board, grid)
                            last_move = 'rotate'
                            count += 1
                            break
                    else:
                        for grid, counter_clockwise_button in enumerate(counter_clockwise_buttons):
                            if counter_clockwise_button.handle_event(event):
                                rotate_counter_clockwise(board, grid)
                                last_move = 'rotate'
                                count += 1
                                break
                    rotate_flag = True
                result = check_win(board)
                end_flag, winner = result[0], result[1]
                if end_flag:
                    if winner == 'X':
                        winner = 'Человек'
                    else:
                        winner = 'Компьютер'
                    message = f"Игрок {winner} победил!"
                    draw_board()
                    time.sleep(3)
                    show_text(message)
                    running = False
                    sys.exit()
                draw_board()
                if count == 5:
                    max_depth += 1
                elif count == 10:
                    max_depth += 1
                if rotate_flag and cell_flag:
                    a = random.choice(get_computer_position(board))
                    grid, row, col, quot, direct = a[0], a[1], a[2], int(a[3]), a[4]
                    board[int(grid)][int(row)][int(col)] = 'O'
                    draw_board()
                    time.sleep(1.5)
                    res = get_rotate(board)
                    if res[0] == 0:
                        board = rotate_clockwise(board, res[1])[0]
                    else:
                        board = rotate_counter_clockwise(board, res[1])[0]
                    rotate_flag, cell_flag = False, False
        for el in clockwise_buttons:
            el.check_hover(pygame.mouse.get_pos())
        for el in counter_clockwise_buttons:
            el.check_hover(pygame.mouse.get_pos())
        draw_board()


if __name__ == '__main__':
    main_func()
