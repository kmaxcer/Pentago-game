import time
import pygame
from pygame.locals import *
import random
import sys
import sqlite3

pygame.init()
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()
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
current_player = 'X'


def main_func(a=board, b=last_move, c=current_player, d=0):
    board = a
    last_move = b
    current_player = c
    from_db = d

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

    def rotate_clockwise(grid):
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]

    def rotate_counter_clockwise(grid):
        board[grid] = [list(row) for row in zip(*board[grid][::-1])]

    running = True

    def check_winner(board):
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

    def show_dialog(num):
        pygame.init()

        screen_width = 800
        screen_height = 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Введите имя ' + str(num) + '-ого игрока')

        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 64)

        text = ""
        input_active = True

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                    pygame.QUIT
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return text
                    elif event.key == K_BACKSPACE:
                        if input_active:
                            text = text[:-1]
                    else:
                        if input_active:
                            text += event.unicode

            screen.fill((255, 255, 255))

            text_surf = font.render(text, True, (255, 0, 0))
            screen.blit(text_surf, text_surf.get_rect(center=screen.get_rect().center))
            font = pygame.font.Font(None, 36)
            text_render = 'Введите имя ' + str(num) + '-ого игрока'
            text_surface = font.render(text_render, True, (0, 0, 0))
            text_rect_render = text_surface.get_rect(center=(400, 250))

            screen.blit(text_surface, text_rect_render)
            pygame.display.flip()
            clock.tick(30)

        pygame.QUIT

    if not from_db:
        first_player = show_dialog(1)
        second_player = show_dialog(2)
        starting_player = random.choice([first_player, second_player])
        if starting_player != first_player:
            first_player, second_player = second_player, first_player
        show_text('Первым начинает ' + starting_player)

        result = cursor.execute("""SELECT * FROM games WHERE id > 0""").fetchall()
        id = len(list(result)) + 1
    else:
        result = list(cursor.execute(f"""SELECT id, player1, player2 FROM games WHERE id = {from_db}""").fetchall())
        id, first_player, second_player = result[0][0], result[0][1], result[0][2]
        cursor.execute(f"""DELETE FROM games WHERE id = {id}""")
        print(id, first_player, second_player)

    pygame.init()
    print(current_player, last_move)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = 1
                if last_move == 'rotate':
                    flag = 0
                sp_X = []
                sp_O = []
                for grid in range(4):
                    for row in range(3):
                        for col in range(3):
                            if board[grid][row][col] == 'X':
                                sp_X.append(str(grid) + str(row) + str(col))
                            elif board[grid][row][col] == 'O':
                                sp_O.append(str(grid) + str(row) + str(col))
                str_X = ','.join(sp_X)
                str_O = ','.join(sp_O)
                coords = str_X + ';' + str_O
                data = (id, first_player, second_player, coords, flag, 'in_game')
                data = str(data)
                insert_query = "INSERT INTO games (id, player1, player2, coordinates, flag, result) VALUES " + data
                cursor.execute(insert_query)
                conn.commit()
                cursor.close()
                pygame.QUIT
                sys.exit()
            result = check_winner(board)
            end_flag, winner = result[0], result[1]
            if end_flag:
                if winner == 'X':
                    winner = first_player
                else:
                    winner = second_player
                data = (id, first_player, second_player, '', 1, winner)
                data = str(data)
                insert_query = "INSERT INTO games (id, player1, player2, coordinates, flag, result) VALUES " + data
                cursor.execute(insert_query)
                conn.commit()
                cursor.close()
                message = f"Игрок {winner} победил!"
                show_text(message)
                pygame.QUIT
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if last_move == 'rotate':
                    last_move = 'cell'
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
                            board[grid][row_x][row_y] = current_player
                            if current_player == 'X':
                                current_player = 'O'
                            else:
                                current_player = 'X'
                else:
                    if last_move == 'cell':
                        for grid, clockwise_button in enumerate(clockwise_buttons):
                            if clockwise_button.collidepoint(event.pos):
                                rotate_clockwise(grid)
                                last_move = 'rotate'
                                break
                        else:
                            for grid, counter_clockwise_button in enumerate(counter_clockwise_buttons):
                                if counter_clockwise_button.collidepoint(event.pos):
                                    rotate_counter_clockwise(grid)
                                    last_move = 'rotate'
                                    break
        draw_board()
    pygame.QUIT


if __name__ == '__main__':
    main_func()
