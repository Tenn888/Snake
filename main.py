# Импортируем компоненты из модулей приложения
from variables import *
import functions as func

# Инициализируемзвуковой модуль
pygame.mixer.init()

# Включаем проигрывание звука
pygame.mixer.music.play(-1)

# Задаем название окна
pygame.display.set_caption('Змейка')

text = pygame.font.SysFont('courier', 36)

func.start_snake()

clock = pygame.time.Clock()

# Пишем игровой цикл
while running:
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #######################################################################
        elif func.mode == 'menu' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if LVL_1_RECT.collidepoint(event.pos):
                FPS = 5
                func.mode = 'game'
                pygame.mixer.music.play(loops=-1)
            elif LVL_2_RECT.collidepoint(event.pos):
                FPS = 10
                func.mode = 'game'
                pygame.mixer.music.play(loops=-1)
            elif LVL_3_RECT.collidepoint(event.pos):
                FPS = 15
                func.mode = 'game'
                pygame.mixer.music.play(loops=-1)

        elif event.type == pygame.KEYDOWN:

            if func.mode == 'end' and event.key == pygame.K_r:
                # Сброс игры
                snake_rect = [func.Rect(9, 9)]
                food = func.random_food_block()
                result = 0
                func.mode = 'menu'

            # Проверка на нажатие клавиш клавиатуры
            if event.key == pygame.K_UP and func.y_col != 0:
                func.x_row = -1
                func.y_col = 0
            if event.key == pygame.K_DOWN and func.y_col != 0:
                func.x_row = 1
                func.y_col = 0
            if event.key == pygame.K_RIGHT and func.x_row != 0:
                func.x_row = 0
                func.y_col = 1
            if event.key == pygame.K_LEFT and func.x_row != 0:
                func.x_row = 0
                func.y_col = -1

    # Отрисовка меню
    if func.mode == 'menu':
        func.app.fill(FRAME_COLOR)
        func.app.blit(LVL_1, LVL_1_RECT)
        func.app.blit(LVL_2, LVL_2_RECT)
        func.app.blit(LVL_3, LVL_3_RECT)
        pygame.mixer.music.pause()

    # Отрисовка игры
    elif func.mode == 'game':

        func.app.fill(FRAME_COLOR)

        # Отрисовываем сетку
        for row in range(COUNT_RECTS):
            for column in range(COUNT_RECTS):
                if (row + column) % 2 == 0:
                    color = RECT_COLOR
                else:
                    color = OTHER_RECT_COLOR
                func.draw_rect(color, row, column)

        # Отрисовываем яблоко
        func.draw_rect(FOOD_COLOR, func.food.x, func.food.y)
        # Отрисовываем змею
        for rect in func.snake_rect:
            func.draw_rect(SNAKE_COLOR, rect.x, rect.y)

        # Голова змеи
        head = func.snake_rect[-1]

        # Проверка на съедание еды
        if func.food == head:
            func.result += 1
            func.snake_rect.append(func.food)
            func.food = func.random_food_block()

        # Проверка на столкновение с границами
        if not head.inside() or func.eat_my_self(func.snake_rect):
            pygame.mixer.music.pause()
            func.mode = 'end'

        # Перемещение змеи
        new_head = func.Rect(head.x + func.x_row, head.y + func.y_col)
        func.snake_rect.append(new_head)
        func.snake_rect.pop(0)

        # Вывод полученных очков 
        text_result = text.render(f'Очки: {func.result}', 0, RECT_COLOR)
        func.app.blit(text_result, (SIZE_RECT, SIZE_RECT))

    # Отрисовка окончания игры
    elif func.mode == 'end':
        func.app.fill(FRAME_END)
        TEXT_END = FONT_END.render('Игра окончена. Ваш счет: ' + str(func.result), 1, (255, 255, 255))

        func.app.blit(TEXT_END, TEXT_END_RECT)
        func.app.blit(AGAIN, AGAIN_RECT)

        # Добавляем проверку события MOUSEBUTTONDOWN в режиме end
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if AGAIN_RECT.collidepoint(event.pos):
                func.start_snake()
                pygame.mixer.music.play(-1)

    # Обновление экрана
    pygame.display.update()
    clock.tick(FPS)

# Остановка игры
pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.quit()