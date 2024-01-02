import pygame
import sys

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
current_player = 'X'


def main_func():
    global last_move, current_player

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
        global board
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]
        board[grid] = [list(row)[::-1] for row in zip(*board[grid])]

    def rotate_counter_clockwise(grid):
        global board
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

    while running:
        for event in pygame.event.get():
            result = check_winner(board)
            end_flag, winner = result[0], result[1]
            if end_flag:
                message = f"Player {winner} wins!"
                print(message)
                font = pygame.font.Font(None, 48)
                text = font.render(message, True, WHITE)
                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(text, text_rect)
                running = False
            elif event.type == pygame.QUIT:
                running = False
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
    pygame.quit()


if __name__ == '__main__':
    main_func()
