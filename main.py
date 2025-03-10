import pygame
import random
from variables import *

pygame.init()

# Инициализируем звуковой модуль
pygame.mixer.init()

# Загружаем музыку
pygame.mixer.music.load('Music.mp3')

# Включаем проигрывание звука
pygame.mixer.music.play(-1)

# Создаем игровое окно
app = pygame.display.set_mode((WIDTH, HEIGHT))

# Задаем название окна
pygame.display.set_caption('Змейка')

# Создаем переменную-флаг, которая отвечает за состояние цикла
running = True
mode = 'menu'

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

class Rect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inside(self):
        return 0 < self.x <= COUNT_RECTS - 1 and 0 < self.y <= COUNT_RECTS - 1

    def __eq__(self, other):
        return isinstance(other, Rect) and self.x == other.x and self.y == other.y

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

text = pygame.font.SysFont('courier', 36)

start_snake()

clock = pygame.time.Clock()

# Пишем игровой цикл
while running:
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #######################################################################
        elif mode == 'menu' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if LVL_1_RECT.collidepoint(event.pos):
                FPS = 5
                mode = 'game'
                pygame.mixer.music.play(loops=-1)
            elif LVL_2_RECT.collidepoint(event.pos):
                FPS = 10
                mode = 'game'
                pygame.mixer.music.play(loops=-1)
            elif LVL_3_RECT.collidepoint(event.pos):
                FPS = 15
                mode = 'game'
                pygame.mixer.music.play(loops=-1)

        elif event.type == pygame.KEYDOWN:

            if mode == 'end' and event.key == pygame.K_r:
                # Сброс игры
                snake_rect = [Rect(9, 9)]
                food = random_food_block()
                result = 0
                mode = 'menu'

            if event.key == pygame.K_UP and y_col != 0:
                x_row = -1
                y_col = 0
            if event.key == pygame.K_DOWN and y_col != 0:
                x_row = 1
                y_col = 0
            if event.key == pygame.K_RIGHT and x_row != 0:
                x_row = 0
                y_col = 1
            if event.key == pygame.K_LEFT and x_row != 0:
                x_row = 0
                y_col = -1

    if mode == 'menu':
        app.fill(FRAME_COLOR)
        app.blit(LVL_1, LVL_1_RECT)
        app.blit(LVL_2, LVL_2_RECT)
        app.blit(LVL_3, LVL_3_RECT)
        pygame.mixer.music.pause()
    elif mode == 'game':

        app.fill(FRAME_COLOR)

        # Отрисовываем сетку
        for row in range(COUNT_RECTS):
            for column in range(COUNT_RECTS):
                
                if (row + column) % 2 == 0:
                    color = RECT_COLOR
                else:
                    color = OTHER_RECT_COLOR
                draw_rect(color, row, column)
        # Отрисовываем яблоко
        draw_rect(FOOD_COLOR, food.x, food.y)
        # Отрисовываем змею
        for rect in snake_rect:
            draw_rect(SNAKE_COLOR, rect.x, rect.y)

        head = snake_rect[-1]

        if food == head:
            result += 1
            snake_rect.append(food)
            food = random_food_block()

        if not head.inside() or eat_my_self(snake_rect):
            pygame.mixer.music.pause()
            mode = 'end'

        new_head = Rect(head.x + x_row, head.y + y_col)
        snake_rect.append(new_head)
        snake_rect.pop(0)

        # Вывод полученных очков 
        text_result = text.render(f'Очки: {result}', 0, RECT_COLOR)
        app.blit(text_result, (SIZE_RECT, SIZE_RECT))

    elif mode == 'end':
        app.fill(FRAME_END)
        TEXT_END = FONT_END.render('Игра окончена. Ваш счет: ' + str(result), 1, (255, 255, 255))

        app.blit(TEXT_END, TEXT_END_RECT)
        app.blit(AGAIN, AGAIN_RECT)

        # Добавляем проверку события MOUSEBUTTONDOWN в режиме end
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if AGAIN_RECT.collidepoint(event.pos):
                start_snake()
                pygame.mixer.music.play(-1)

    pygame.display.update()
    clock.tick(FPS)
pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.quit()