# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from Lib.draw import Game, WIDTH, HEIGHT, FPS  # из модуля Lib.draw
import Lib.logik as logik

# Создаем игру и окно
pygame.mixer.pre_init(44100, -16, 1, 512)  # инициализация Звука, и библиотек для работы с звуком
pygame.init()  # инициализация дополнительных библиотек для модуля

pygame.display.set_caption("My Game")  # создаем оглавление в окне
clock = pygame.time.Clock()  # создаем обработчик задержки обнавления экрана

NN = 3 # размер поля 4х4
field = Game(WIDTH, HEIGHT, NN)  # игровое поле
field.screen.blit(field.drawField(), (0, 0))

# Цикл игры

motion = field.setup_window()  # True - игрок первый  False - первый ходит синий ПК
step = 0
running = True  # флаг для выхода из цикла программы
pt = 0
while running and step < NN*NN: # пока не заполнены все ячейки поля
    # Держим цикл на правильной скорости
    clock.tick(FPS)  # создаем задержку для того что бы экран обнавлялся нужное колво  в секунду
    # Ввод процесса (события)
    mouse_pos = pygame.mouse.get_pos()
    if motion:
        for event in pygame.event.get():  # цикл обработки событий (мышка, клавиатура, и так далее)
            # ВЫХОД ИЗ ИГРЫ
            if event.type == pygame.QUIT:  # реакуия на нажатие крестика
                running = False  # Меняем флаг для того что бы завершить игровой цикл
            # ХОДИТ ИГРОК
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, item in enumerate(field.setka):
                    if item.collidepoint(pygame.mouse.get_pos()) and field.field[index] == logik.EMPTY:
                        field.sounds[1].play()
                        step += 1
                        motion = False
                        field.upgradeFild(index, logik.O)
                        pt = index
    # ХОДИТ КОМПЬЮТЕР
    else:
        step += 1
        motion = True
        pt = logik.get_computer_move(field.getField(),NN)
        field.upgradeFild(pt, logik.X)
        print('step=',step)


    # Обновление  блок где мы обрабатываем изменения (движение персонажа и так далее)
    field.screen.blit(field.drawField(), (0, 0))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()  # отображаем обновления

    if logik.check_win(pt, field.getField(), logik.X if motion else logik.O,NN):
        print('Кто то победиол')
        x = logik.X if motion else logik.O
        [field.screen.blit(field.imageres[5], field.setka[index]) for index, value in enumerate(field.field) if
         value not in [x, logik.EMPTY]]
        pygame.display.flip()
        pygame.time.delay(5000)

        motion = field.end_round_window(logik.X if motion else logik.O)
        step = 0
    elif step == NN*NN:
        pygame.time.delay(2000)
        motion = field.end_round_window(1)
        step = 0
    # Рендеринг                        # подготовка изображения к отображению
    field.screen.blit(field.drawField(), (0, 0))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()  # отображаем обновления

pygame.quit()  # выход из модуля....
