import pygame as pg
pygame = pg
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
B_AGAIN = pygame.image.load('buttons/button_again.png')
AGAIN = pygame.transform.scale(B_AGAIN, (40, 40))
AGAIN_RECT = AGAIN.get_rect(center=(WIDTH // 2, HEIGHT // 1.7))

# Загружаем музыку
pygame.mixer.music.load('Music.mp3')

# Создаем переменную-флаг, которая отвечает за состояние цикла
running = True