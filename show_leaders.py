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
pygame.display.set_caption("Таблица игроков")

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# Получение данных из базы данных
cursor.execute('SELECT player1, player2, result FROM games')
games = cursor.fetchall()

# Создание словаря для хранения результатов
results = {}
games_played = {}

# Подсчет побед каждого игрока и подсчет общего количества игр
for game in games:
    player1, player2, result = game
    if result != 'in_game':
        if result == player1:
            if player1 in results:
                results[player1] += 1
            else:
                results[player1] = 1
        elif result == player2:
            if player2 in results:
                results[player2] += 1
            else:
                results[player2] = 1

        if player1 in games_played:
            games_played[player1] += 1
        else:
            games_played[player1] = 1

        if player2 in games_played:
            games_played[player2] += 1
        else:
            games_played[player2] = 1

# Сортировка результатов
sorted_results = sorted(results.items(),
                        key=lambda x: (-x[1], -x[1] / games_played[x[0]], -games_played[x[0]], x[0]))

# Создание списка sp с данными об игроках
for i, (player, wins) in enumerate(sorted_results, 1):
    total_games = games_played[player]
    win_percentage = (wins / total_games) * 100
    sp.append((i, player, wins, total_games, str(round(win_percentage, 2)) + '%'))


def main_func():
    global sp, roll_count
    roll_count = 0

    # Создание функции для извлечения данных из базы данных
    def get_players(roll_count=0):
        return sp[roll_count:]

    # Функция для отображения таблицы данных
    def display_table(players):
        # Определение размеров ячейки
        column_width = 160
        cell_height = 100
        x_offset = 0

        # Заполнение фона белым цветом
        screen.fill(WHITE)

        # Отрисовка заголовка таблицы
        title = ["Место", "Имя", "Победы", "Игры", "Процент побед"]
        column_widths = [160, 160, 160, 160, 160]
        for i in range(len(title)):
            pygame.draw.rect(screen, WHITE, (x_offset, 0, column_widths[i], cell_height), 1)
            pygame.draw.rect(screen, WHITE, (x_offset + 1, 1, column_widths[i] - 2, cell_height - 2))
            font = pygame.font.Font(None, 30)
            text = font.render(str(title[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x_offset + column_widths[i] // 2, cell_height // 2))
            screen.blit(text, text_rect)
            x_offset += column_widths[i]

        # Отрисовка данных таблицы
        for i, player in enumerate(players):
            x_offset = 0
            y_offset = (i + 1) * cell_height
            pygame.draw.rect(screen, GREY, (x_offset, y_offset, width, cell_height), 1)

            for j, value in enumerate(player[:5]):
                pygame.draw.rect(screen, GREY, (x_offset, y_offset, column_widths[j], cell_height), 1)
                pygame.draw.rect(screen, GREY, (x_offset + 1, y_offset + 1, column_widths[j] - 2, cell_height - 2))
                font = pygame.font.Font(None, 60)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x_offset + column_widths[j] // 2, y_offset + cell_height // 2))
                screen.blit(text, text_rect)
                x_offset += column_widths[j]

        # Обновление экрана
        pygame.display.flip()

    def scroll_down():
        global roll_count
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        r1 = list(cursor.execute("SELECT id FROM games WHERE result = 'in_game'"))
        r2 = list(cursor.execute("SELECT id FROM games WHERE id > 0"))
        res = len(r2) - len(r1)
        cursor.close()
        conn.close()
        count = res - 7
        if count - 1 - roll_count > 0:
            roll_count += 1

    def scroll_up():
        global roll_count
        if roll_count >= 1:
            roll_count -= 1

    # Функция для обработки нажатий мыши
    def handle_mouse_click(click_pos, players):
        cell_height = 100

        for i, player in enumerate(players):
            y_offset = (i + 1) * cell_height
            if y_offset <= click_pos[1] <= y_offset + cell_height:
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
                for el in sp_X:
                    el = list(map(int, list(el)))
                    x, y, z = el[0], el[1], el[2]
                    board[x][y][z] = 'X'
                for el in sp_O:
                    el = list(map(int, list(el)))
                    x, y, z = el[0], el[1], el[2]
                    board[x][y][z] = 'O'
                last_move = 'rotate'
                if coords[1] == 0:
                    last_move = 'cell'
                if len(sp_X) != len(sp_O):
                    current_player = 'O'
                else:
                    current_player = 'X'

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
                if event.button == 4:
                    scroll_up()
                elif event.button == 5:
                    scroll_down()

        # Получение данных из базы данных
        players = get_players(roll_count)

        # Отображение таблицы данных
        display_table(players)

    # Завершение работы Pygame
    pygame.QUIT


if __name__ == '__main__':
    main_func()
