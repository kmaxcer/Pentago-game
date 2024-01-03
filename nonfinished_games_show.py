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


def main_func():
    global sp

    # Создание функции для извлечения данных из базы данных
    def get_players():
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

        return players

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
        title = ["ID", "Player 1", "Player 2"]
        column_widths = [column1_width, column2_width, column3_width]
        for i in range(len(title)):
            pygame.draw.rect(screen, BLUE, (x_offset, 0, column_widths[i], cell_height), 1)
            pygame.draw.rect(screen, BLUE, (x_offset + 1, 1, column_widths[i] - 2, cell_height - 2))
            font = pygame.font.Font(None, 20)
            text = font.render(str(title[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x_offset + column_widths[i] // 2, cell_height // 2))
            screen.blit(text, text_rect)
            x_offset += column_widths[i]

        # Отрисовка данных таблицы
        for i, player in enumerate(players):
            x_offset = 0
            y_offset = (i + 1) * cell_height
            pygame.draw.rect(screen, GREY, (x_offset, y_offset, width, cell_height), 1)

            for j, value in enumerate(player[:3]):
                pygame.draw.rect(screen, GREY, (x_offset, y_offset, column_widths[j], cell_height), 1)
                pygame.draw.rect(screen, GREY, (x_offset + 1, y_offset + 1, column_widths[j] - 2, cell_height - 2))
                font = pygame.font.Font(None, 20)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x_offset + column_widths[j] // 2, y_offset + cell_height // 2))
                screen.blit(text, text_rect)
                x_offset += column_widths[j]

        # Обновление экрана
        pygame.display.flip()

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
                if event.button == pygame.BUTTON_LEFT:
                    # Обработка нажатия мыши
                    handle_mouse_click(pygame.mouse.get_pos(), get_players())

        # Получение данных из базы данных
        players = get_players()

        # Отображение таблицы данных
        display_table(players)

    # Завершение работы Pygame
    pygame.QUIT


if __name__ == '__main__':
    main_func()
