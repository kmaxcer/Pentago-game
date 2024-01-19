import pygame
from pygame.locals import *

window_width = 800
window_height = 800
background_color = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)

background_image = pygame.image.load("background.png")
menu_button = pygame.image.load("menu_button.png")
menu_pic = pygame.image.load("menu_pic.png")
points = pygame.image.load("about_game.png")

background_image = pygame.transform.scale(background_image, (window_width, window_height))
pygame.init()


# Функция для отображения главного меню
def draw_menu(window):
    global button_rect, button_rect_1, button_rect_2, button_rect_3, menu_button, menu_pic, points, button_menu_rect
    # Очистите экран и установите цвет фона
    window.fill(background_color)
    button_width, button_height = 265, 21
    button_x, button_y = 266, 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_width_1, button_height_1 = 534, 25
    button_x_1, button_y_1 = 131, 200
    button_rect_1 = pygame.Rect(button_x_1, button_y_1, button_width_1, button_height_1)
    button_width_2, button_height_2 = 266, 23
    button_x_2, button_y_2 = 265, 250
    button_rect_2 = pygame.Rect(button_x_2, button_y_2, button_width_2, button_height_2)
    button_width_3, button_height_3 = 454, 20
    button_x_3, button_y_3 = 185, 300
    button_rect_3 = pygame.Rect(button_x_3, button_y_3, button_width_3, button_height_3)
    button_menu_width, button_menu_height = 40, 40
    button_menu_rect = pygame.Rect(0, 0, button_menu_width, button_menu_height)
    font = pygame.font.Font("Pressstart2p.ttf", 40)
    title_text = font.render("Меню", True, (0, 0, 0))
    font = pygame.font.Font("Pressstart2p.ttf", 27)
    button1_text = font.render("Новая игра", True, (0, 0, 0))
    button2_text = font.render("Просмотр прошлых игр", True, (0, 0, 0))
    button3_text = font.render("Все игроки", True, (0, 0, 0))
    button4_text = font.render("Игра с компьтером", True, (0, 0, 0))

    # Отобразите текст на экране в нужных позициях

    window.blit(background_image, (0, 0))
    pygame.draw.rect(window, LIGHT_GREY, button_menu_rect)
    points = pygame.transform.scale(points, (40, 40))
    window.blit(points, (0, 0))
    menu_pic = pygame.transform.scale(menu_pic, (330, 100))
    window.blit(menu_pic, (230, 20))
    menu_button = pygame.transform.scale(menu_button, (330, 50))
    window.blit(menu_button, (202, 137))
    menu_button = pygame.transform.scale(menu_button, (660, 50))
    window.blit(menu_button, (5, 187))
    menu_button = pygame.transform.scale(menu_button, (335, 50))
    window.blit(menu_button, (195, 237))
    menu_button = pygame.transform.scale(menu_button, (560, 50))
    window.blit(menu_button, (80, 287))
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 50))
    window.blit(button1_text, (window_width // 2 - button1_text.get_width() // 2, 150))
    window.blit(button2_text, (window_width // 2 - button2_text.get_width() // 2, 200))
    window.blit(button3_text, (window_width // 2 - button3_text.get_width() // 2, 250))
    window.blit(button4_text, (185, 300))
    # Добавьте код для отображения текста и кнопок меню

    # Обновите экран
    pygame.display.update()


# Функция для начала новой игры
def start_new_game():
    # Добавьте код для начала новой игры
    import main
    main.main_func()


# Проверка на нажатие текста
def is_text_clicked(text_rect):
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos):
        return True
    return False


# Функция для продолжения сохраненной игры
def show_old_games():
    import nonfinished_games_show
    nonfinished_games_show.main_func()


# Показать лидеров
def show_leaders():
    import show_leaders
    show_leaders.main_func()


# Игра с ИИ
def game_with_ai():
    import game_with_ai
    game_with_ai.main_func()


# Показать информацию об игре
def show_about():
    import about_game
    about_game.main_func()


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
                if event.key == K_1:  # Нажата клавиша "1" - начать новую игру
                    start_new_game()
                if event.key == K_2:  # Нажата клавиша "2" - посмотреть старые игры
                    show_old_games()
                if event.key == K_3:  # Нажата клавиша "3" - показать лидеров
                    show_leaders()
                if event.key == K_4:  # Нажата клавиша "4" - начать игру с ИИ
                    game_with_ai()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        start_new_game()
                    if button_rect_1.collidepoint(event.pos):
                        show_old_games()
                    if button_rect_2.collidepoint(event.pos):
                        show_leaders()
                    if button_rect_3.collidepoint(event.pos):
                        game_with_ai()
                    if button_menu_rect.collidepoint(event.pos):
                        show_about()


if __name__ == "__main__":
    main()
