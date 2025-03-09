import pygame
import random

pygame.init()

# Прорисываем константы
HEIGHT = 600
FRAME_COLOR = (70, 130, 180)
RECT_COLOR = (255, 255, 255)
OTHER_RECT_COLOR = (204, 255, 255)
SIZE_RECT = 20
COUNT_RECTS = 20
RETURN = 1
WIDTH = SIZE_RECT * COUNT_RECTS + 2 * SIZE_RECT + RETURN * SIZE_RECT
HEADER_RECT = 70
HEADER_COLOR = (0, 0, 255)
SNAKE_COLOR = (0, 128, 0)
FOOD_COLOR = (255, 0, 0)
FPS = 5

###################### Текст проигрыша
# Шрифт окна проигрыша
FONT_END = pygame.font.SysFont(None, 40)
# Текст проигрыша
TEXT_END = FONT_END.render('Игра окончена. Ваш счет: ', 1, (255, 255, 255))
TEXT_END_RECT = TEXT_END.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
FRAME_END = (255, 0, 0)

###################### Меню
B_1 = pygame.image.load('buttons/button_1.png')
LVL_1 = pygame.transform.scale(B_1, (40, 40))
LVL_1_RECT = LVL_1.get_rect(center=(WIDTH // 4, HEIGHT // 2))
B_2 = pygame.image.load('buttons/button_2.png')
LVL_2 = pygame.transform.scale(B_2, (40, 40))
LVL_2_RECT = LVL_2.get_rect(center=(WIDTH // 4 * 2, HEIGHT // 2))
B_3 = pygame.image.load('buttons/button_3.png')
LVL_3 = pygame.transform.scale(B_3, (40, 40))
LVL_3_RECT = LVL_3.get_rect(center=(WIDTH // 4 * 3, HEIGHT // 2))

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

snake_rect = [Rect(9, 9), Rect(9, 10)]
x_row = 0
y_col = 1
food = random_food_block()
result = 0
text = pygame.font.SysFont('courier', 36)

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

    pygame.display.update()
    clock.tick(FPS)
pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.quit()