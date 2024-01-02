import pygame
from pygame.locals import *

pygame.init()

# Задайте размеры окна и цвет фона
window_width = 800
window_height = 600
background_color = (255, 255, 255)

# Создайте окно с указанными размерами
window = pygame.display.set_mode((window_width, window_height))

# Установите заголовок окна
pygame.display.set_caption("Меню Пентаго")


def draw_menu():
    # Очистите экран и установите цвет фона
    window.fill(background_color)

    # Создайте объекты текста для вывода на экран
    font = pygame.font.Font(None, 36)
    title_text = font.render("Меню Пентаго", True, (0, 0, 0))
    start_text = font.render("1. Новая игра", True, (0, 0, 0))
    continue_text = font.render("2. Продолжить игру", True, (0, 0, 0))
    exit_text = font.render("3. Выход", True, (0, 0, 0))

    # Отобразите текст на экране в нужных позициях
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
    window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, 300))
    window.blit(continue_text, (window_width // 2 - continue_text.get_width() // 2, 350))
    window.blit(exit_text, (window_width // 2 - exit_text.get_width() // 2, 400))

    # Обновите экран
    pygame.display.update()


def main():
    running = True
    while running:
        # Отображение главного меню
        draw_menu()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    # Нажата клавиша "1" - начать новую игру
                    start_new_game()
                elif event.key == K_2:
                    # Нажата клавиша "2" - продолжить игру
                    continue_game()
                elif event.key == K_3:
                    # Нажата клавиша "3" - выход
                    running = False


if __name__ == "__main__":
    main()

# Завершение программы
pygame.quit()
