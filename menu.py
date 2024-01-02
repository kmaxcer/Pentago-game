import pygame
import sys
from pygame.locals import *

window_width = 800
window_height = 800
background_color = (255, 255, 255)
pygame.init()


# Функция для отображения главного меню
def draw_menu(window):
    # Очистите экран и установите цвет фона
    window.fill(background_color)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Меню Пентаго", True, (0, 0, 0))
    button1_text = font.render("1. Новая игра", True, (0, 0, 0))
    button2_text = font.render("2. Просмотр прошлых игр", True, (0, 0, 0))

    # Отобразите текст на экране в нужных позициях
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
    window.blit(button1_text, (window_width // 2 - button1_text.get_width() // 2, 300))
    window.blit(button2_text, (window_width // 2 - button2_text.get_width() // 2, 350))
    # Добавьте код для отображения текста и кнопок меню

    # Обновите экран
    pygame.display.update()


# Функция для начала новой игры
def start_new_game():
    # Добавьте код для начала новой игры
    import main
    main.main_func()


# Функция для продолжения сохраненной игры

# Основной цикл программы
def main():
    pygame.init()
    # Создайте окно с указанными размерами
    window = pygame.display.set_mode((window_width, window_height))

    # Установите заголовок окна
    pygame.display.set_caption("Меню Пентаго")
    running = True
    while running:
        # Отображение главного меню
        draw_menu(window)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    # Нажата клавиша "1" - начать новую игру
                    start_new_game()

    # Завершение программы
    pygame.quit()


if __name__ == "__main__":
    main()
