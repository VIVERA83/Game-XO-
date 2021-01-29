import pygame

from Lib.logik import *
from math import sqrt

# настройки
# габариты и частота обнавления экрана
WIDTH = 600
HEIGHT = 600
FPS = 30
# Границы ячейки
CELL_SIZE = 200
# Задаем цвета
GREEN = (0, 255, 0) # Цвет надписей

path = 'Lib/Image/' # 0                      1                     2              3              4               5
File_name_list = ['выбран_синий.jpg', 'выбран_желтый.jpg', 'синий200.png', 'желтый200.png', 'empty.png', 'flame.png',
                  'фон600.jpg']
                     # 6

class Game:
    """Игровое поле"""

    def __init__(self, width, height, N):
        # игровое окно
        self.cell_size = width // int(sqrt(N * N))  # размер ячейки
        self.width = self.cell_size * N  # высота
        self.height = self.cell_size * N  # длинна
        self.N = N  # ширина поля
        self.screen = pygame.display.set_mode((self.width, self.height)) #основное окно
        self.window = pygame.Surface((self.width, self.height))  #  второстепенное получаемый квадрат

        # картинки для игры Загрузка и маштабирование  если нужно
        self.bk = pygame.transform.scale(pygame.image.load(path + File_name_list[6]), (self.width, self.height))
        self.button_play = pygame.image.load(path + 'button_play_activ.png')
        self.imageres = [pygame.transform.scale(pygame.image.load(path + i), (self.cell_size, self.cell_size)) for i in
                         File_name_list]
        # Музыка и звуки
        pygame.mixer.music.load('sound/musik.mp3')
        pygame.mixer.music.play(-1)
        self.sounds = [pygame.mixer.Sound('sound/choise.ogg'),pygame.mixer.Sound('sound/move.ogg'),pygame.mixer.Sound('sound/error.ogg')]

        # логика игры
        self.step = 0  # номер хода (что бы не выйти за пределы игры)
        self.field = [EMPTY] * self.N * self.N  # поле
        self.choise_avatar = False  # выбран X
        self.choise_first = False  # ходит X ходит
        self.key_field = {X: self.imageres[2] if self.choise_avatar else self.imageres[3],
                          O: self.imageres[3] if self.choise_avatar else self.imageres[2],
                          EMPTY: self.imageres[4]}  # число : картинка
        # Сетка с координатами ячеек
        self.setka = [self.imageres[0].get_rect(x=x * self.cell_size, y=y * self.cell_size) for y in
                     range(self.N) for x in range(self.N)]

    def upgradeFild(self, index, value):
        self.field[index] = value

    def drawField(self):
        self.window.blit(self.bk, self.bk.get_rect())
        [self.window.blit(self.key_field[value], self.setka[index]) for index, value in enumerate(self.field)]
        return self.window

    def getField(self):  # Возращает список игрового поля
        return self.field

    def setup_window(self, ):

        def draw(*args):

            y = self.width // self.cell_size * 5
            self.window.blit(self.bk, self.bk.get_rect())

            avatar_rect = self.imageres[0].get_rect()
            window_rect = self.window.get_rect()
            for i in range(len(text) - 1):
                self.window.blit(text[i], (window_rect.centerx - text[i].get_rect().centerx, y))
                y += text[i].get_rect().bottom
                self.window.blit(self.imageres[2] if args[i] else self.imageres[0],
                                 (window_rect.centerx - avatar_rect.right, y))
                self.window.blit(self.imageres[1] if args[i] else self.imageres[3], (window_rect.centerx, y))

                choise_list.append(self.imageres[0].get_rect(x=window_rect.centerx - avatar_rect.right, y=y))
                choise_list.append(self.imageres[3].get_rect(x=window_rect.centerx, y=y))
                y += self.cell_size

            transform = pygame.transform.scale(self.button_play, (200, 100))

            self.window.blit(transform, (
                window_rect.centerx - transform.get_rect().centerx, window_rect.bottom - transform.get_rect().bottom))

            self.window.blit(text[len(text) - 1],
                             (window_rect.centerx - text[len(text) - 1].get_rect().centerx, y+50 ))
            choise_list.append(transform.get_rect(x=window_rect.centerx - transform.get_rect().centerx,
                                                  y=window_rect.bottom - transform.get_rect().bottom))

        message = ['Выбирите аватар:', 'Выбирите кто ходит первый!', 'Играть']
        font = pygame.font.SysFont(None, 50)
        text = [font.render(i, 1, GREEN) for i in message]
        choise_list = []

        draw(self.choise_avatar, self.choise_first)

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # реакуия на нажатие крестика
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.sounds[0].play()  # звук выбора
                    for index, item in enumerate(choise_list):
                        if item.collidepoint(pygame.mouse.get_pos()):
                            if index == 0:
                                self.choise_avatar = False
                            if index == 1:
                                self.choise_avatar = True
                            if index == 2:
                                self.choise_first = False
                            if index == 3:
                                self.choise_first = True
                            if index == 4:
                                self.key_field = {X: self.imageres[2] if self.choise_avatar else self.imageres[3],
                                                  O: self.imageres[3] if self.choise_avatar else self.imageres[2],
                                                  EMPTY: self.imageres[4]}  # число : картинка
                                return True if self.choise_first == self.choise_avatar else False
            draw(self.choise_avatar, self.choise_first)
            self.screen.blit(self.window, self.window.get_rect())
            pygame.display.flip()

    def end_round_window(self, win=1):
        retreat = 30
        message = ['Победил:', 'Победила дружба!', 'Играть', 'Настройки']
        font = pygame.font.SysFont(None, 50)
        text = font.render(message[0 if win != 1 else 1], 1, GREEN)
        text_play = font.render(message[2], 1, GREEN)
        text_settings = font.render(message[3], 1, GREEN)

        self.window.blit(self.bk, self.bk.get_rect()) # обновляем фон

        self.window.blit(text, text.get_rect(centerx=self.width // 2, top=retreat))
        self.window.blit(self.button_play, self.button_play.get_rect(
            center=(self.width // 2, self.height // 2 + retreat)))  # изображение кнопки играть
        self.window.blit(self.button_play, self.button_play.get_rect(
            center=(self.width // 2, self.height // 2 + 7 * retreat)))  # изображение кнопки настройки

        self.window.blit(text_play, self.bk.get_rect(
            centerx=self.width // 2 - text_play.get_rect().centerx).center)

        self.window.blit(text_settings, (self.width // 2 - text_settings.get_rect().centerx,
                                         self.height - 100))

        button_play_pos = self.button_play.get_rect(center=(self.width // 2, self.height // 2 + retreat))
        button_settings_pos = self.button_play.get_rect(center=(self.width // 2, self.height // 2 + 7 * retreat))

        if win == 1:

            self.window.blit(self.key_field[3],
                             self.key_field[win].get_rect(centerx=self.width // 2 - 100, top=2 * retreat))
            self.window.blit(self.key_field[4],
                             self.key_field[win].get_rect(centerx=self.width // 2 + 100, top=2 * retreat))
        else:
            self.window.blit(self.key_field[win],
                             self.key_field[win].get_rect(centerx=self.width // 2, top=2 * retreat))

        self.screen.blit(self.window, self.window.get_rect())

        self.field = [EMPTY] * self.N * self.N
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # реакуия на нажатие крестика
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_play_pos.collidepoint(pygame.mouse.get_pos()):
                        print('нажата кнопка играть')
                        return True if self.choise_first == self.choise_avatar else False
                    if button_settings_pos.collidepoint(pygame.mouse.get_pos()):
                        print('нажата кнопка настройки, vty. rjytw')
                        return self.setup_window()  # Переходим в меню настройки
            pygame.display.flip()
