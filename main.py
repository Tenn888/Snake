import json
import pygame
import random

pygame.init()

# Прописываем константы
HEIGHT = 600
FRAME_COLOR = (70, 130, 180)
FRAME_END = (255, 0, 0)
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

# Загрузка кнопок
B_ON_MUSIC = pygame.image.load('buttons/on_music.png')
ON_MUSIC_RECT = B_ON_MUSIC.get_rect(center=(WIDTH - 40, HEIGHT // 10 - 40))
B_OFF_MUSIC = pygame.image.load('buttons/off_music.png')   
OFF_MUSIC_RECT = B_ON_MUSIC.get_rect(center=(WIDTH - 40, HEIGHT // 10 - 40))

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

# Функция рисования объектов
def draw_rect(color, row, column):
    pygame.draw.rect(app, color, (SIZE_RECT + column * SIZE_RECT + RETURN * (column + 1), 
                                              HEADER_RECT + SIZE_RECT + row * SIZE_RECT + RETURN * (row + 1), SIZE_RECT, SIZE_RECT))

# Функция проверки столкновения головы с тулловищем
def eat_my_self(snake_rect):
    head = snake_rect[-1]
    for i in range(len(snake_rect) - 2):
        if head.x == snake_rect[i].x and head.y == snake_rect[i].y:
            return True
    return False

# Создаем класс Змеи
class Rect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inside(self):
        return 0 <= self.x <= COUNT_RECTS - 1 and 0 <= self.y <= COUNT_RECTS - 1

    def __eq__(self, other):
        return isinstance(other, Rect) and self.x == other.x and self.y == other.y

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

# Функция начальных переменных игры
def start_snake():
    global snake_rect, x_row, y_col, food, result, mode
    snake_rect = [Rect(9, 9), Rect(9, 10)]
    x_row = 0
    y_col = 1
    food = random_food_block()
    result = 0
    mode = 'menu'

# Отрислвываем текст и добавляем его в словарь
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
        draw_rect(FOOD_COLOR, food.x, food.y)
        
        # Отрисовываем змею
        for rect in snake_rect:
            draw_rect(SNAKE_COLOR, rect.x, rect.y)

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
        
        # Пауза музыки
        if OFF_MUSIC_RECT.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            music_on = not music_on
            if music_on:
                pygame.mixer.music.unpause()
                data['music_status'] = music_on
            else:
                pygame.mixer.music.pause()
                data['music_status'] = music_on

    # Отрисовываем объекты в режиме end
    elif mode == 'end':
        app.fill(FRAME_END)

        # Записываем результат в data, как рекорд, если он больше старого рекорда
        if result > data['record']:
            data['record'] = result

        # Отрисовываем результат и кнопку "Еще раз"
        text_objects('Игра окончена. Ваш счет: ' + str(result), FONT, 2, 2, y=-30)
        text_objects('Начать заново', FONT, 2, 2, y=50)

        # Добавляем проверку события MOUSEBUTTONDOWN в режиме end
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if display_objects['Начать заново'].collidepoint(event.pos):
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