#import pygame

import random
from variables import *

class Rect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inside(self):
        return 0 < self.x <= COUNT_RECTS - 1 and 0 < self.y <= COUNT_RECTS - 1

    def __eq__(self, other):
        return isinstance(other, Rect) and self.x == other.x and self.y == other.y

# Функция рисования объектов
def draw_rect(color, row, column):
    pygame.draw.rect(app, color, (SIZE_RECT + column * SIZE_RECT + RETURN * (column + 1), 
                                              HEADER_RECT + SIZE_RECT + row * SIZE_RECT + RETURN * (row + 1), SIZE_RECT, SIZE_RECT))

# Функция проверки столкновения головы с тулловищем
def eat_my_self(snacke_rect):
    head = snake_rect[-1]
    for i in range(len(snacke_rect) - 2):
        if head.x == snacke_rect[i].x and head.y == snacke_rect[i].y:
            return True
    return False

# Функция рандомных координат для еды
def random_food_block():
    x = random.randint(0, COUNT_RECTS - 1)
    y = random.randint(0, COUNT_RECTS - 1)

    food_block = Rect(x, y)

    while food_block in snake_rect:
        x = random.randint(0, COUNT_RECTS - 1)
        y = random.randint(0, COUNT_RECTS - 1)

    return food_block

# Функция начальных переменных игры
def start_snake():
    global snake_rect, x_row, y_col, food, result, mode
    snake_rect = [Rect(9, 9), Rect(9, 10)]
    x_row = 0
    y_col = 1
    food = random_food_block()
    result = 0
    mode = 'menu'

# Создаем игровое окно
app = pygame.display.set_mode((WIDTH, HEIGHT))
