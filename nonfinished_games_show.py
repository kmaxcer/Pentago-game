import pygame
import sqlite3

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLUE = (0, 0, 0)
GREY = (200, 200, 200)

# Создание окна Pygame
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Таблица игроков")


# Создание функции для извлечения данных из базы данных
def main_func():
    def get_players():
        # Подключение к базе данных
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()

        # Выполнение запроса к базе данных
        cursor.execute("SELECT id, player1, player2 FROM games WHERE result = 'in_game'")

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
            pygame.draw.rect(screen, WHITE, (x_offset, 0, column_widths[i], cell_height), 1)
            pygame.draw.rect(screen, WHITE, (x_offset + 1, 1, column_widths[i] - 2, cell_height - 2))
            font = pygame.font.Font(None, 60)
            text = font.render(str(title[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x_offset + column_widths[i] // 2, cell_height // 2))
            screen.blit(text, text_rect)
            x_offset += column_widths[i]

        # Отрисовка данных таблицы
        for i, player in enumerate(players):
            x_offset = 0
            for j in range(len(player)):
                pygame.draw.rect(screen, GREY, (x_offset, (i + 1) * cell_height, column_widths[j], cell_height), 1)
                pygame.draw.rect(screen, GREY,
                                 (x_offset + 1, (i + 1) * cell_height + 1, column_widths[j] - 2, cell_height - 2))
                font = pygame.font.Font(None, 60)
                text = font.render(str(player[j]), True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(x_offset + column_widths[j] // 2, (i + 1) * cell_height + cell_height // 2))
                screen.blit(text, text_rect)
                x_offset += column_widths[j]

        # Обновление экрана
        pygame.display.flip()

    # Основной цикл игры
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT

        # Получение данных из базы данных
        players = get_players()

        # Отображение таблицы данных
        display_table(players)

    # Завершение работы Pygame
    pygame.QUIT


if __name__ == '__main__':
    main_func()
