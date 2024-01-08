import time
import pygame
from pygame.locals import *
import random
import sys
import sqlite3
from button_class import ImageButton

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
clockwise_buttons = []
counter_clockwise_buttons = []
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
arrow_img = pygame.image.load("arrow.png")
black_sphere = pygame.image.load("sphere-black.png")
white_sphere = pygame.image.load("sphere-white.png")
background_image = pygame.image.load("2players_game.png")
button_before = pygame.image.load("circle_before.png")
button_after = pygame.image.load("circle_after.png")
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
current_player = 'X'


def main_func(a=board, b=last_move, c=current_player, d=0):
    global clockwise_buttons, counter_clockwise_buttons
    board = a
    last_move = b
    current_player = c
    from_db = d

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
        screen.fill(WHITE)
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
        for el in clockwise_buttons:
            el.draw(screen)
        for el in counter_clockwise_buttons:
            el.draw(screen)
        pygame.draw.line(screen, WHITE, (398, 100), (398, 700), 5)
        pygame.draw.line(screen, WHITE, (100, 398), (700, 398), 5)
        # Отрисовка кнопок
        screen.blit(arrow_img, (100, 0))
        screen.blit(mirror_image(rotate_image(arrow_img, 90), 1), (0, 100))
        screen.blit(mirror_image(rotate_image(arrow_img, 180), 1), (600, 0))
        screen.blit(rotate_image(arrow_img, 270), (700, 100))
        screen.blit(rotate_image(arrow_img, 90), (0, 600))
        screen.blit(mirror_image(arrow_img, 1), (100, 700))
        screen.blit(rotate_image(arrow_img, 180), (600, 700))
        screen.blit(rotate_image(mirror_image(arrow_img, 1), 90), (700, 600))
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
        font = pygame.font.Font("Robotocondensed Regular.ttf", 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 400))

        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        time.sleep(3)

        pygame.QUIT

    def run_game(player_number):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode([800, 800])
        base_font = pygame.font.Font("Robotocondensed Regular.ttf", 32)
        user_text = ''
        input_rect = pygame.Rect(330, 386, 140, 48)
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('grey')
        color = color_passive

        button_rect = pygame.Rect(320, 436, 160, 48)
        button_color_passive = pygame.Color('dodgerblue')
        button_color_active = pygame.Color('lightskyblue2')
        button_color = button_color_passive

        active = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        return user_text
                    else:
                        if active:
                            user_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return user_text

            screen.fill((255, 255, 255))

            if active:
                color = color_active
            else:
                color = color_passive

            text_surface = base_font.render(user_text, True, (255, 255, 255))
            input_rect.width = max(100, text_surface.get_width() + 10)
            input_rect.x = screen.get_width() // 2 - input_rect.width // 2
            input_rect.y = screen.get_height() // 2 - input_rect.height // 2

            pygame.draw.rect(screen, color, input_rect)
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = button_color_active
            else:
                button_color = button_color_passive

            pygame.draw.rect(screen, button_color, button_rect)
            button_text = base_font.render("Отправить", True, (255, 255, 255))
            screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))

            title_text = base_font.render(f"Введите имя {player_number}-ого игрока", True, (0, 0, 0))
            title_x = screen.get_width() // 2 - title_text.get_width() // 2
            title_y = input_rect.y - 40
            screen.blit(title_text, (title_x, title_y))

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    if not from_db:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        first_player = run_game(1)
        second_player = run_game(2)
        starting_player = random.choice([first_player, second_player])
        if starting_player != first_player:
            first_player, second_player = second_player, first_player
        show_text('Первым начинает ' + starting_player)

        result = cursor.execute("""SELECT id FROM games WHERE id > 0""").fetchall()
        id = max(list(result))[0] + 1
        print(id)
        conn.commit()
        cursor.close()
    else:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        result = list(cursor.execute(f"""SELECT id, player1, player2 FROM games WHERE id = {from_db}""").fetchall())
        id, first_player, second_player = result[0][0], result[0][1], result[0][2]
        cursor.execute(f"""DELETE FROM games WHERE id = {id}""")
        if current_player == 'X':
            show_text('Первым начинает ' + first_player)
        else:
            show_text('Первым начинает ' + second_player)
        conn.commit()
        cursor.close()
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn = sqlite3.connect('database.sqlite')
                cursor = conn.cursor()
                import dialog_after_closing
                if dialog_after_closing.main_func():
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
                else:
                    cursor.execute(f"""DELETE FROM games WHERE id = {id}""")
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
                print(insert_query)
                conn = sqlite3.connect('database.sqlite')
                cursor = conn.cursor()
                cursor.execute(insert_query)
                conn.commit()
                cursor.close()
                draw_board()
                time.sleep(3)
                message = f"Игрок {winner} победил!"
                show_text(message)
                pygame.QUIT
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if last_move == 'rotate':
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
                            last_move = 'cell'
                else:
                    if last_move == 'cell':
                        for grid, clockwise_button in enumerate(clockwise_buttons):
                            if clockwise_button.handle_event(event):
                                rotate_clockwise(grid)
                                last_move = 'rotate'
                                break
                        else:
                            for grid, counter_clockwise_button in enumerate(counter_clockwise_buttons):
                                if counter_clockwise_button.handle_event(event):
                                    rotate_counter_clockwise(grid)
                                    last_move = 'rotate'
                                    break
        for el in clockwise_buttons:
            el.check_hover(pygame.mouse.get_pos())
        for el in counter_clockwise_buttons:
            el.check_hover(pygame.mouse.get_pos())
        draw_board()
    pygame.QUIT


if __name__ == '__main__':
    main_func()
