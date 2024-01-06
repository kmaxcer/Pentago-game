import pygame

pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Инициализация окна и поверхности
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Меню пентаго")

# Создание кнопки для открытия информационного меню
button_menu_width, button_menu_height = 25, 25
button_menu_rect = pygame.Rect(0, 0, button_menu_width, button_menu_height)

# Загрузка шрифта
font = pygame.font.SysFont("Arial", 20)


def main_func():
    def draw_text(text, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_menu():
        # Заполнение фона информационного меню
        screen.fill(GRAY)

        # Отрисовка текста с правилами игры
        draw_text("Правила игры:", WHITE, 20, 20)
        draw_text("- Пентаго -", WHITE, 20, 50)
        draw_text("Игра для двух игроков.", WHITE, 20, 80)
        draw_text("Цель игры - выстроить 5 шариков", WHITE, 20, 110)
        draw_text("в ряд по горизонтали, вертикали или диагонали,", WHITE, 20, 140)
        draw_text("повернув одну из четырех частей поля", WHITE, 20, 170)
        draw_text("на 90 градусов или собрав ряд.", WHITE, 20, 200)

        # Отрисовка текста с дополнительной информацией и управлением
        draw_text("Дополнительная информация:", WHITE, 20, 250)
        draw_text("- Управление -", WHITE, 20, 280)
        draw_text("Используйте мышь, чтобы выбрать ячейку", WHITE, 20, 310)
        draw_text("и кнопки мыши, чтобы повернуть часть поля.", WHITE, 20, 340)
        draw_text("и кнопки мыши, чтобы повернуть часть поля.", WHITE, 20, 340)

        draw_text("1. На кнопку 'Новая игра' откроется 2 окна с заполнением имен игроков", WHITE, 20, 370)
        draw_text("после откроется сама игра, система случайно решит, кто ходит первым", WHITE, 20, 400)
        draw_text("2. На кнопку 'Просмотр прошлых игр' откроется таблица", WHITE, 20, 430)
        draw_text("с данными о незавершённых играх", WHITE, 20, 460)
        draw_text("чтобы продолжить какую-либо игру, просто нажмите на нужную строку", WHITE, 20, 490)
        draw_text("3. На кнопку 'Все игроки' откроется таблица со всеми когда-либо", WHITE, 20, 520)
        draw_text("игравшими. Напротив их имен написана их статистика", WHITE, 20, 550)
        draw_text("4. На кнопку 'Игра с компьютером' откроется игра с компьютером,", WHITE, 20, 580)
        draw_text("алгоритм работы которого расчитан на среднего игрока", WHITE, 20, 610)
        pygame.display.flip()

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill(WHITE)
            draw_menu()
    pygame.QUIT


if __name__ == '__main__':
    main_func()
