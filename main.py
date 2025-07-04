import json
import pygame
import random

pygame.init()


# Константы
FPS = 5
RETURN = 1

# Цвета
FRAME_COLOR = (34, 139, 34)         # Зеленый цвет поля
FRAME_END = (255, 0, 0)             # Красный для конца игры
RECT_COLOR = (255, 255, 255)        # Белый
OTHER_RECT_COLOR = (204, 255, 255)  # Светло-голубой
MOUTH_COLOR = (255, 50, 50)         # Темно-красный для рта
SNAKE_COLOR = (30, 144, 255)        # Синий цвет змеи
EYE_COLOR = (0, 0, 0)               # Черный для глаз
HEADER_COLOR = (0, 0, 255)          # Синий для заголовка
FOOD_COLOR = (255, 0, 0)            # Красный для еды

# Размеры
SIZE_RECT = 20
COUNT_RECTS = 20
HEADER_RECT = 70
HEIGHT = 600
WIDTH = SIZE_RECT * COUNT_RECTS + 2 * SIZE_RECT + RETURN * SIZE_RECT
EYE_RADIUS = SIZE_RECT // 7

# Загрузка изображений
B_ON_MUSIC = pygame.image.load('images/on_music.png')
ON_MUSIC_RECT = B_ON_MUSIC.get_rect(center=(WIDTH - 40, HEIGHT // 10 - 30))
B_OFF_MUSIC = pygame.image.load('images/off_music.png')   
OFF_MUSIC_RECT = B_ON_MUSIC.get_rect(center=(WIDTH - 40, HEIGHT // 10 - 30))
B_PAUSE = pygame.image.load('images/pause.png')
PAUSE_RECT = B_PAUSE.get_rect(center=(WIDTH - 100, HEIGHT // 10 - 30))
B_PLAY = pygame.image.load('images/play.png')
PLAY_RECT = B_PLAY.get_rect(center=(WIDTH - 100, HEIGHT // 10 - 30))

# Шрифт текста
FONT = pygame.font.SysFont('Arial', 40)
FONT_SMALL = pygame.font.SysFont('Arial', 20)


# Инициализируем звуковой модуль
pygame.mixer.init()

# Загружаем музыку
pygame.mixer.music.load('Music.mp3')

# Создаем игровое окно
app = pygame.display.set_mode((WIDTH, HEIGHT))

# Задаем название окна
pygame.display.set_caption('Змейка')

# Создаем переменную-флаг, которая отвечает за состояние цикла
running = True

# Создаем файл для хранения данных и переменную data
try:
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
        music_on = data['music_status']
except FileNotFoundError:
    with open('data.json', 'w') as data_file:
        data = {
            'music_status': True, 
            'record': 0
            }
        music_on = data['music_status']

# Создаем словарь для отрисовонного текста
display_objects = {}

# Создаем класс для объектов
class Rect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Проверка на нахождение в пределах игрового поля
    def inside(self):
        return 0 <= self.x <= COUNT_RECTS - 1 and 0 <= self.y <= COUNT_RECTS - 1

    # Проверка на нахождение в пределах змеи
    def __eq__(self, other):
        return isinstance(other, Rect) and self.x == other.x and self.y == other.y


# Функция начальных переменных игры
def start_snake():
    global snake_rect, x_row, y_col, food, result, mode
    snake_rect = [Rect(9, 9), Rect(9, 10)]
    x_row = 0
    y_col = 1
    food = random_food_block()
    result = 0
    mode = 'menu'

# Функция рандомных координат для еды
def random_food_block():
    x = random.randint(0, COUNT_RECTS - 1)
    y = random.randint(0, COUNT_RECTS - 1)

    food_block = Rect(x, y)

    # Проверка на совпадение координат еды и змеи
    while food_block in snake_rect:
        x = random.randint(0, COUNT_RECTS - 1)
        y = random.randint(0, COUNT_RECTS - 1)

    return food_block

# Функция проверки столкновения головы с тулловищем
def eat_my_self(snake_rect):
    head = snake_rect[-1]
    for i in range(len(snake_rect) - 2):
        if head.x == snake_rect[i].x and head.y == snake_rect[i].y:
            return True
    return False

# Функции рисования объектов
def draw_rect(color, x, y, rounding_up=0, border_radii=None):
    rect = pygame.Rect(
        SIZE_RECT + y * SIZE_RECT + RETURN * (y + 1),
        HEADER_RECT + SIZE_RECT + x * SIZE_RECT + RETURN * (x + 1),
        SIZE_RECT, SIZE_RECT
    )
    if border_radii:
        pygame.draw.rect(app, color, rect, border_radius=rounding_up, **border_radii)
    else:
        pygame.draw.rect(app, color, rect, border_radius=rounding_up)

def draw_sprite(sprite, x, y):
    rect = pygame.Rect(
        y * SIZE_RECT + RETURN * (y + 1),
        HEADER_RECT + x * SIZE_RECT + RETURN * (x + 1)
    )
    app.blit(sprite, rect)

# Функция отрисовки змеи
def draw_snake(snake_rect):
    # Отрисовка тела
    for rect in snake_rect[1:-1]:
        draw_rect(SNAKE_COLOR, rect.x, rect.y, rounding_up=0)

    # Радиусы скругления
    radius_head = 6
    radius_tail = 8

    # По умолчанию все углы не скруглены
    border_radii = {
        "border_top_left_radius": 0,
        "border_top_right_radius": 0,
        "border_bottom_left_radius": 0,
        "border_bottom_right_radius": 0
    }

    # Отрисовка хвоста с округлением только с одной стороны
    tail = snake_rect[0]
    # Определяем направление движения
    tx = tail.x - snake_rect[1].x
    ty = tail.y - snake_rect[1].y

    # Координаты хвоста
    x = SIZE_RECT + tail.y * SIZE_RECT + RETURN * (tail.y + 1)
    y = HEADER_RECT + SIZE_RECT + tail.x * SIZE_RECT + RETURN * (tail.x + 1)

    if tx == -1:  # вверх
        border_radii["border_top_left_radius"] = radius_tail
        border_radii["border_top_right_radius"] = radius_tail
    elif tx == 1:  # вниз
        border_radii["border_bottom_left_radius"] = radius_tail
        border_radii["border_bottom_right_radius"] = radius_tail
    elif ty == -1:  # влево
        border_radii["border_bottom_left_radius"] = radius_tail
        border_radii["border_top_left_radius"] = radius_tail
    elif ty == 1:  # вправо
        border_radii["border_top_right_radius"] = radius_tail
        border_radii["border_bottom_right_radius"] = radius_tail
    
    draw_rect(SNAKE_COLOR, tail.x, tail.y, border_radii=border_radii)




    # Отрисовка головы с округлением только с одной стороны
    head = snake_rect[-1]
    # Определяем направление движения
    dx = head.x - snake_rect[-2].x
    dy = head.y - snake_rect[-2].y

    # Координаты головы
    x = SIZE_RECT + head.y * SIZE_RECT + RETURN * (head.y + 1)
    y = HEADER_RECT + SIZE_RECT + head.x * SIZE_RECT + RETURN * (head.x + 1)

    # Онуляем радиусы скругления
    border_radii = {
        "border_top_left_radius": 0,
        "border_top_right_radius": 0,
        "border_bottom_left_radius": 0,
        "border_bottom_right_radius": 0
    }

    # Скругляем только ту сторону, куда смотрит голова
    if dx == -1:  # вверх
        border_radii["border_top_left_radius"] = radius_head
        border_radii["border_top_right_radius"] = radius_head
    elif dx == 1:  # вниз
        border_radii["border_bottom_left_radius"] = radius_head
        border_radii["border_bottom_right_radius"] = radius_head
    elif dy == -1:  # влево
        border_radii["border_top_left_radius"] = radius_head
        border_radii["border_bottom_left_radius"] = radius_head
    elif dy == 1:  # вправо
        border_radii["border_top_right_radius"] = radius_head
        border_radii["border_bottom_right_radius"] = radius_head

    draw_rect(SNAKE_COLOR, head.x, head.y, border_radii=border_radii)



    # Глаза
    pygame.draw.circle(app, EYE_COLOR, (x + SIZE_RECT // 3, y + SIZE_RECT // 3), EYE_RADIUS)
    pygame.draw.circle(app, EYE_COLOR, (x + 2 * SIZE_RECT // 3, y + SIZE_RECT // 3), EYE_RADIUS)

    # Рот
    global mouth_rect
    mouth_rect = pygame.Rect(
        x + SIZE_RECT // 3,
        y + SIZE_RECT // 2,
        SIZE_RECT // 3,
        SIZE_RECT // 4
    )

# Функция отрисовки яблока
def draw_apple(x, y):
    # Центр клетки
    ax = SIZE_RECT + y * SIZE_RECT + RETURN * (y + 1) + SIZE_RECT // 2
    ay = HEADER_RECT + SIZE_RECT + x * SIZE_RECT + RETURN * (x + 1) + SIZE_RECT // 2
    radius = SIZE_RECT // 1.7

    # Яблоко (красный круг)
    pygame.draw.circle(app, FOOD_COLOR, (ax, ay), radius)

    # Листик 
    leaf_color = (34, 139, 34)
    leaf_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    leaf_rect = pygame.Rect(4, 0, 8, 12)
    pygame.draw.ellipse(leaf_surface, leaf_color, leaf_rect)
    # Поворачиваем листик на -30 градусов
    rotated_leaf = pygame.transform.rotate(leaf_surface, -30)
    # Получием координаты для размещения листика
    leaf_pos = (ax - rotated_leaf.get_width() // 2, ay - int(radius) - 10)
    app.blit(rotated_leaf, leaf_pos)


# Отрисовываем текст и добавляем его в словарь
def text_objects(text, font, a=1, b=1, x=0, y=0, size_x=WIDTH, size_y=HEIGHT):
    global display_objects
    text_display = font.render(text, 1, (255, 255, 255))
    text_display_rect = text_display.get_rect(center=(size_x // a + x, size_y // b + y)) 
    app.blit(text_display, text_display_rect)

    display_objects[text] = text_display_rect


# Вызываем функцию начальных переменных
start_snake()

clock = pygame.time.Clock()

# Пишем игровой цикл
while running:
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #######################################################################
        # Проверка на нажатие кнопок
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Проверка на нажатие кнопок в меню
            if mode == 'menu':
                if display_objects['Играть'].collidepoint(event.pos):
                    mode = 'game_complexity'
                elif display_objects['FAQ'].collidepoint(event.pos):
                    mode = 'faq'

            elif mode == 'game_complexity':
                if display_objects['Легко'].collidepoint(event.pos):
                    FPS = 5
                    mode = 'game'
                    if music_on:
                        pygame.mixer.music.play(loops=-1)
                elif display_objects['Средне'].collidepoint(event.pos):
                    FPS = 10
                    mode = 'game'
                    if music_on:
                        pygame.mixer.music.play(loops=-1)
                elif display_objects['Сложно'].collidepoint(event.pos):
                    FPS = 15
                    mode = 'game'
                    if music_on:
                        pygame.mixer.music.play(loops=-1)
                elif display_objects['Назад'].collidepoint(event.pos):
                    mode = 'menu'

            # Проверка на нажатие кнопок в FAQ
            elif mode == 'faq':
                if display_objects['Игра'].collidepoint(event.pos):
                    mode = 'faq_game'
                elif display_objects['Главное меню'].collidepoint(event.pos):
                    mode = 'faq_menu'
                elif display_objects['Сложность'].collidepoint(event.pos): 
                    mode = 'faq_complexity'
                elif display_objects['Назад'].collidepoint(event.pos):
                    mode = 'menu'

            # Проверка на нажатие кнопок в FAQ_GAME
            elif mode == 'faq_game':
                if display_objects['Назад'].collidepoint(event.pos):
                    mode = 'faq'
            
            # Проверка на нажатие кнопок в FAQ_MENU
            elif mode == 'faq_menu':
                if display_objects['Назад'].collidepoint(event.pos):
                    mode = 'faq'

            elif mode == 'faq_complexity':
                if display_objects['Назад'].collidepoint(event.pos):
                    mode = 'faq'

        elif event.type == pygame.KEYDOWN:

            if mode == 'end' and event.key == pygame.K_r:
                # Сброс игры
                start_snake()

            # Управление змейкой
            if event.key in (pygame.K_UP, pygame.K_w) and y_col != 0:
                x_row = -1
                y_col = 0
            if event.key in (pygame.K_DOWN, pygame.K_s) and y_col != 0:
                x_row = 1
                y_col = 0
            if event.key in (pygame.K_RIGHT, pygame.K_d) and x_row != 0:
                x_row = 0
                y_col = 1
            if event.key in (pygame.K_LEFT, pygame.K_a) and x_row != 0:
                x_row = 0
                y_col = -1
        #######################################################################

    # Отрисовываем объекты в меню
    if mode == 'menu':
        # Заполняем фон цветом
        app.fill(FRAME_COLOR)

        # Отрисовываем кнопку "FAQ"
        text_objects('FAQ', FONT, 10, 10,)

        # Отрисовываем ryjgre "Играть"
        text_objects('Играть', FONT, a=4, b=2, x=115, y=-50)

        # Пауза музыки
        pygame.mixer.music.pause()

    # Отрисовываем объекты в game_complexity
    elif mode == 'game_complexity':
        # Заполняем фон цветом
        app.fill(FRAME_COLOR)

        # Отрисовываем кнопку "Назад"
        text_objects('Назад', FONT, a=10, b=9, x=4, y=300)

        # Отрисовываем текст
        text_objects('Выберите сложность игры', FONT, a=2, b=2, x=-7, y=-150)

        # Отрисовываем кнопки
        text_objects('Легко', FONT, a=4, b=2, x=-50, y=-50)
        text_objects('Средне', FONT, a=4, b=2, x=100, y=-50)
        text_objects('Сложно', FONT, a=4, b=2, x=250, y=-50)
        
    # Отрисовываем объекты в FAQ
    elif mode == 'faq':
        # Заполняем фон цветом
        app.fill(FRAME_COLOR)

        # Отрисовываем кнопку "Главное меню"
        text_objects('Главное меню', FONT, 10, 10, 70, 0)

        # Отрисовываем кнопку "Игра"
        text_objects('Игра', FONT, 10, 9, -4, 50)

        # Отрисовываем кнопку "Сложность"
        text_objects('Сложность', FONT, 10, 9, 40, 100)

        # Отрисовываем кнопку "Назад"
        text_objects('Назад', FONT, 10, 9, 4, 300)

    # Отрисовываем объекты в FAQ_GAME
    elif mode == 'faq_game':
        # Заполняем фон цветом
        app.fill(FRAME_COLOR)
        
        # Составляем список для отрисовки текста
        faq_game_list = [
            'Игра:',
            'W, A, S, D - перемещать змейку',
            'Съедая яблоко Вы увеличиваете свою змейку',
            'Съедая яблоко Вы повышаете свои очки',
            'Рекорд - максимальное количество очков за все время'
        ]
        
        # Отрисовываем текст
        for i, line in enumerate(faq_game_list):
            text_objects(line, FONT_SMALL, a=2, b=4, y=i * 40)

        # Отрисовываем кнопку "Назад"
        text_objects('Назад', FONT, a=10, b=9, x=4, y=300)

    # Отрисовываем объекты в FAQ_MENU
    elif mode == 'faq_menu':
        app.fill(FRAME_COLOR)

        # Составляем список для отрисовки текста
        faq_menu_list = [
            'Главное меню:',
            'Цифры - это уровень сложности игры.',
            'FAQ - это кнопка для получения информации об игре.',
        ]

        # Отрисовываем текст
        for i, line in enumerate(faq_menu_list):
            text_objects(line, FONT_SMALL, a=2, b=4, y=i * 40)
        
        # Отрисовываем кнопку "Назад"
        text_objects('Назад', FONT, a=10, b=9, x=4, y=300)

    elif mode == 'faq_complexity':
        # Заполняем фон цветом
        app.fill(FRAME_COLOR)

        # Составляем список для отрисовки текста
        faq_complexity_list = [
            'Сложность:',
            'Легко - 5 FPS',
            'Средне - 10 FPS',
            'Сложно - 15 FPS',
        ]

        # Отрисовываем текст
        for i, line in enumerate(faq_complexity_list):
            text_objects(line, FONT_SMALL, a=2, b=4, y=i * 40)

        # Отрисовываем кнопку "Назад"
        text_objects('Назад', FONT, a=10, b=9, x=4, y=300)

    # Отрисовываем объекты в режиме game
    elif mode == 'game':

        # Заполняем фон цветом
        app.fill(FRAME_COLOR)

        # Отрисовываем сетку
        for row in range(COUNT_RECTS):
            for column in range(COUNT_RECTS):
                # Проверка на четность/нечетность
                if (row + column) % 2 == 0:
                    color = RECT_COLOR
                else:
                    color = OTHER_RECT_COLOR
                draw_rect(color, row, column)

        # Отрисовываем яблоко
        draw_apple(food.x, food.y)

        # Отрисовываем змею
        draw_snake(snake_rect)
        pygame.draw.arc(app, MOUTH_COLOR, mouth_rect, 3.14, 0, 2)

        # Определение головы змеи
        head = snake_rect[-1]

        # Проверка на съедание еды
        if food == head:
            result += 1
            snake_rect.append(food)
            food = random_food_block()

        # Проверка на столкновение с границами
        if not head.inside() or eat_my_self(snake_rect):
            pygame.mixer.music.pause()
            mode = 'end'

        # Перемещение змеи
        new_head = Rect(head.x + x_row, head.y + y_col)
        snake_rect.append(new_head)
        snake_rect.pop(0)
        
        # Отрисовываем текст
        text_objects(f'Очки: {result}', FONT, x=40, y=-5, size_x=SIZE_RECT, size_y=SIZE_RECT)
        text_objects(f'Рекорд: {data['record']}', FONT, x=66, y=35, size_x=SIZE_RECT, size_y=SIZE_RECT)

        # Проверка на включение/выключение музыки
        if music_on:
            app.blit(B_ON_MUSIC, ON_MUSIC_RECT)
        else:
            app.blit(B_OFF_MUSIC, OFF_MUSIC_RECT)

        app.blit(B_PAUSE, PAUSE_RECT)
        
        # Пауза музыки
        if OFF_MUSIC_RECT.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            music_on = not music_on
            if music_on:
                pygame.mixer.music.unpause()
                data['music_status'] = music_on
            else:
                pygame.mixer.music.pause()
                data['music_status'] = music_on

        if PAUSE_RECT.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mode == 'game':
                mode = 'pause'
                pygame.mixer.music.pause()

    # Отрисовываем объекты в режиме pause
    elif mode == 'pause':
        app.fill(FRAME_COLOR)
        text_objects('Продолжить', FONT, 2, 2, y=-30)
        text_objects('Выход в меню', FONT, 2, 2, y=50)

        if display_objects['Продолжить'].collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mode = 'game'
            pygame.mixer.music.unpause()
        elif display_objects['Выход в меню'].collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mode = 'menu'

    # Отрисовываем объекты в режиме end
    elif mode == 'end':
        app.fill(FRAME_END)

        # Записываем результат в data, как рекорд, если он больше старого рекорда
        if result > data['record']:
            data['record'] = result

        # Отрисовываем результат и кнопку "Еще раз"
        text_objects('Игра окончена. Ваш счет: ' + str(result), FONT, 2, 2, y=-30)
        text_objects('Главное меню', FONT, 2, 2, y=50)

        # Добавляем проверку события MOUSEBUTTONDOWN в режиме end
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if display_objects['Главное меню'].collidepoint(event.pos):
                start_snake()

    # Обновление экрана
    pygame.display.update()
    clock.tick(FPS)

# Записываем результат в файл
with open('data.json', 'w') as file:
    json.dump(data, file)

# Останавливаем игру
pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.quit()