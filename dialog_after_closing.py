import sys
import time

import pygame

window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))

button_color_agree_passive = (0, 255, 100)
button_color_agree_active = (150, 255, 100)
button_color_disagree_passive = (255, 0, 100)
button_color_disagree_active = (255, 100, 100)
background_color = (255, 255, 255)

screen.fill(background_color)

text = 'Вы хотите сохранить данную игру?'
text_agree = 'Да'
text_disagree = 'Нет'

button_agree_rect = pygame.Rect(200, 440, 50, 40)
button_disagree_rect = pygame.Rect(510, 440, 70, 40)

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Text Window")
screen.fill(background_color)

font = pygame.font.Font("Robotocondensed Regular.ttf", 36)

text_surface = font.render(text, True, (0, 0, 0))
text_rect = text_surface.get_rect(center=(400, 300))

font_choice = pygame.font.Font("Robotocondensed Regular.ttf", 18)

text_yes_surface = font.render(text_agree, True, (0, 0, 0))
text_yes_rect = pygame.Rect(205, 435, 50, 30)

text_no_surface = font.render(text_disagree, True, (0, 0, 0))
text_no_rect = pygame.Rect(515, 435, 70, 40)

active_agree = False
active_disagree = False


def main_func():
    active_agree = False
    active_disagree = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            if button_agree_rect.collidepoint(pygame.mouse.get_pos()):
                active_agree = True
            else:
                active_agree = False
            if button_disagree_rect.collidepoint(pygame.mouse.get_pos()):
                active_disagree = True
            else:
                active_disagree = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_agree_rect.collidepoint(event.pos):
                    return 1
                elif button_disagree_rect.collidepoint(event.pos):
                    return 0
        if active_agree:
            button_color_agree = button_color_agree_active
        else:
            button_color_agree = button_color_agree_passive

        if active_disagree:
            button_color_disagree = button_color_disagree_active
        else:
            button_color_disagree = button_color_disagree_passive
        screen.fill(background_color)
        pygame.draw.rect(screen, button_color_agree, button_agree_rect)
        pygame.draw.rect(screen, button_color_disagree, button_disagree_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_yes_surface, text_yes_rect)
        screen.blit(text_no_surface, text_no_rect)
        pygame.display.flip()
    return 0
    pygame.QUIT


if __name__ == '__main__':
    main_func()
