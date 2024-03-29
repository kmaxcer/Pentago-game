import pygame
import sqlite3

# Инициализация Pygame
pygame.init()
sp = []
# Определение цветов
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
# Создание окна Pygame
width, height = 800, 800
screen = pygame.display.set_mode((width, height))


def main_func():
    pygame.display.set_caption("Таблица игроков")
    global sp, roll_count
    roll_count = 0

    # Создание функции для извлечения данных из базы данных
    def get_players(roll_count=0):
        global cursor
        # Подключение к базе данных
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()

        # Выполнение запроса к базе данных
        cursor.execute("SELECT id, player1, player2, coordinates, flag FROM games WHERE result = 'in_game'")

        # Получение результатов запроса
        players = cursor.fetchall()
        # Закрытие подключения к базе данных
        cursor.close()
        conn.close()

        return players[roll_count:]

    def get_all_players():
        global cursor
        # Подключение к базе данных
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()

        # Выполнение запроса к базе данных
        cursor.execute("SELECT id, player1, player2, coordinates, flag FROM games WHERE result = 'in_game'")

        # Получение результатов запроса
        playerss = cursor.fetchall()
        # Закрытие подключения к базе данных
        cursor.close()
        conn.close()
        print(playerss)
        return playerss

    # Функция для отображения таблицы данных
    def display_table(players):
        # Определение размеров ячейки
        column1_width = 100
        column2_width = 350
        column3_width = 350
        cell_height = 100
        x_offset = 0

        # Заполнение фона белым цветом
        screen.fill(WHITE)

        # Отрисовка заголовка таблицы
        title = ["Номер", "Игрок 1", "Игрок 2"]
        column_widths = [column1_width, column2_width, column3_width]
        for i in range(1, len(title)):
            pygame.draw.rect(screen, WHITE, (x_offset, 0, column_widths[i], cell_height), 1)
            pygame.draw.rect(screen, WHITE, (x_offset + 1, 1, column_widths[i] - 2, cell_height - 2))
            font = pygame.font.Font("Robotocondensed Regular.ttf", 40)
            text = font.render(str(title[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x_offset + column_widths[i] // 2 + 120, cell_height // 2))
            screen.blit(text, text_rect)
            x_offset += column_widths[i]

        font = pygame.font.Font("Robotocondensed Regular.ttf", 40)
        text = font.render("Номер", True, (0, 0, 0))
        text_rect = text.get_rect(center=(70, cell_height // 2))
        screen.blit(text, text_rect)

        # Отрисовка данных таблицы
        for i, player in enumerate(players):
            x_offset = 0
            y_offset = (i + 1) * cell_height
            pygame.draw.rect(screen, GREY, (x_offset, y_offset, width, cell_height), 1)

            for j, value in enumerate(player[:3]):
                pygame.draw.rect(screen, GREY, (x_offset, y_offset, column_widths[j], cell_height), 1)
                pygame.draw.rect(screen, GREY, (x_offset + 1, y_offset + 1, column_widths[j] - 2, cell_height - 2))
                font = pygame.font.Font("Robotocondensed Regular.ttf", 60)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x_offset + column_widths[j] // 2 + 20, y_offset + cell_height // 2))
                screen.blit(text, text_rect)
                x_offset += column_widths[j]
        pygame.draw.line(screen, WHITE, (160, 0), (160, 800), 3)
        pygame.draw.line(screen, WHITE, (480, 0), (480, 800), 3)
        for i in range(6):
            pygame.draw.line(screen, WHITE, (0, 200 + i * 100), (800, 200 + i * 100), 3)

        # Обновление экрана
        pygame.display.flip()

    def scroll_down():
        global roll_count
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        res = list(cursor.execute("SELECT id, player1, player2, coordinates, flag FROM games WHERE result = 'in_game'"))
        cursor.close()
        conn.close()
        count = len(res) - 7
        if count - 1 - roll_count >= 0:
            roll_count += 1

    def scroll_up():
        global roll_count
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        res = list(cursor.execute("SELECT id, player1, player2, coordinates, flag FROM games WHERE result = 'in_game'"))
        cursor.close()
        conn.close()
        if roll_count >= 1:
            roll_count -= 1

    # Функция для обработки нажатий мыши
    def handle_mouse_click(click_pos):
        cell_height = 100

        for i, player in enumerate(get_all_players()):
            y_offset = (i + 1 - roll_count) * cell_height
            if y_offset <= click_pos[1] <= y_offset + cell_height:
                print(player)
                # Запись значения coordinates в список sp
                coords = [player[3], player[4]]
                sp_X = coords[0].split(';')[0].split(',')
                sp_O = coords[0].split(';')[1].split(',')
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
                if sp_X != []:
                    for el in sp_X:
                        el = list(map(int, list(el)))
                        x, y, z = el[0], el[1], el[2]
                        board[x][y][z] = 'X'
                if sp_O != ['']:
                    for el in sp_O:
                        el = list(map(int, list(el)))
                        x, y, z = el[0], el[1], el[2]
                        board[x][y][z] = 'O'
                else:
                    sp_O = []
                last_move = 'rotate'
                if coords[1] == 0:
                    last_move = 'cell'
                if len(sp_X) != len(sp_O):
                    current_player = 'O'
                else:
                    current_player = 'X'
                print(player[0])
                import main
                main.main_func(board, last_move, current_player, player[0])

    # Основной цикл игры
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    # Обработка нажатия мыши
                    handle_mouse_click(pygame.mouse.get_pos())
                elif event.button == 4:
                    scroll_up()
                elif event.button == 5:
                    scroll_down()

        # Получение данных из базы данных
        players = get_players(roll_count)

        # Отображение таблицы данных
        display_table(players)

    # Завершение работы Pygame
    pygame.display.set_caption("Меню Пентаго")


if __name__ == '__main__':
    main_func()
