

from random import randint

N = 3  # ширина поля
X = 2  # символ которым отображается Х
O = -3  # символ которым отображается Y
Pusto = 1  # символ которым отображается не занятая ячейка
Pole = [x for x in range(1, 10)]
PolePC = [Pusto] * N * N
Player = ['O','X']



# pm -  player move  координаты хода игрока интерпретированные в индекс списка


def drawingField(Pole,PolePC, pm=-1):
    for i in range(N):
        for j in range(N):
            if i*N+j == pm:
                st = '\033[31m'
            elif PolePC[i*N+j] == X:
                st ='\033[30m'
            elif PolePC[i*N+j] == O:
                st = '\033[35m'
            else:
                st ='\033[33m'
            s = f' {st}{Pole[i*N+j]}'
            print(s, end='')
        print('\033[37m',end='\n')


def __runComputer(pm, movepc):
    xy = functXY(pm)
    # x-

    if PolePC[funct(0, xy[1])] or PolePC[funct(1, xy[1])] or PolePC[funct(2, xy[1])] == Pusto:
        sum3 = PolePC[funct(0, xy[1])] * PolePC[funct(1, xy[1])] * PolePC[funct(2, xy[1])]
        for i in range(N): # N - это 3 ширина поля
            if PolePC[funct(i, xy[1])] == Pusto:
                if movepc[0][1] < sum3:
                    movepc[0][0] = funct(i, xy[1])
                    movepc[0][1] = sum3

    # y|
    if (PolePC[funct(xy[0], 0)] == Pusto) or (PolePC[funct(xy[0], 1)] == Pusto) or (PolePC[funct(xy[0], 2)] == Pusto):
        sum3 = PolePC[funct(xy[0], 0)] * PolePC[funct(xy[0], 1)] * PolePC[funct(xy[0], 2)]
        for i in range(3):
            if PolePC[funct(xy[0], i)] == Pusto:
                if movepc[0][1] < sum3:
                    movepc[0][0] = funct(xy[0], i)
                    movepc[0][1] = sum3

    # xy\

    if (xy[0] == xy[1] == 0) or (xy[0] == xy[1] == 1) or (xy[0] == xy[1] == 2):
        sum3 = PolePC[0] * PolePC[4] * PolePC[8]
        for i in range(3):
            if PolePC[i * 4] == Pusto:
                if movepc[0][1] <= sum3:
                    movepc[0][0] = i * 4
                    movepc[0][1] = sum3
                    break
    # xy/ и центр
    if (xy[0] == xy[1] == 1) or (xy[0] == 2 and xy[1] == 0) or (xy[0] == 0 and xy[1] == 2):
        sum3 = PolePC[2] * PolePC[4] * PolePC[6]
        for i in range(1, 4):
            if PolePC[i * 2] == Pusto:
                if movepc[0][1] <= sum3:
                    movepc[0][0] = i * 2
                    movepc[0][1] = sum3
                    break


    if PolePC[movepc[0][0]] == Pusto:
        movepc[0][1] = 1
    else:
        movepc[0][1] *= -3
        movepc[0][0] = PolePC.index(Pusto)

    return movepc


def movePC(movePC, movePCLast, pm,  PolePC):
    movePC = __runComputer(pm, movePC)  # ход компьютера от Игрока
    movePClast = __runComputer(movePCLast[0][0], movePCLast)  # ход компьютера от прошлого хода

    if movePC[0][1] <= movePCLast[0][1]:
        movePC[0][0] = movePCLast[0][0]

    PolePC[movePC[0][0]] = O

    return movePC, movePCLast

def funct(x, y):
    z = y * N + x
    return z


def functXY(plm):
    XY = []
    XY.append(plm % N)
    XY.append(plm // N)
    return XY


def controlGame(pm, win=0):
    xy = functXY(pm)
    if Pole[funct(0, xy[1])] == Pole[funct(1, xy[1])] == Pole[funct(2, xy[1])]:
        win = 1
    if Pole[funct(xy[0], 0)] == Pole[funct(xy[0], 1)] == Pole[funct(xy[0], 2)]:
        win = 1
    if (xy[0] == xy[1] == 1) or (xy[0] == xy[1] == 0) or (xy[0] == xy[1] == 2):
        if Pole[0] == Pole[4] == Pole[8]:
            win = 1
    if (xy[0] == xy[1] == 1) or (xy[0] == 2 and xy[1] == 0) or (xy[0] == 0 and xy[1] == 2):
        if Pole[2] == Pole[4] == Pole[6]:
            win = 1
    return win


def movePlayer(controlpole, playmsg):  # Готово
    """Проверка правельности ввода координат поля игроком, c проверкой на занятость
       функция возращает индекс списка в который нужно ставить Х или O"""
    playmsg = 'Игрокp'+ playmsg + ': Введите координаты хода, 1...9:'
    flag = True
    while flag:
        xy = input(playmsg)
        if len(xy) == 1 and xy in '123456789':
            xy = (int(xy) - 1) # * N + int(xy[0]) - 1  # соотносим координаты с адресом ячейки (y-1)*N+x-1
            if PolePC[xy] == Pusto:
                return xy
            else:
                print('Поле занято, введите другие координаты')
        else:
            print('Вы ввели не правельные координаты, повторите ввод')

def selectGame():
    print('Выберите режим игры:\nЧеловек против компьютера(первый ходит человек) -1\n','Компьютер против Человека - 2\n'.rjust(50),'Компьютер против Компьютера - 3'.rjust(49),'\n','Человек против Человека - 4'.rjust(49))
    choice = '0'
    while choice not in '1234':
        choice = input('сделайте выбор, введите от 1 до 4:')
    return choice

def runGame():
    choice =selectGame()
    if choice == '3':
        moveC1, movePClast1= [[randint(0,8),randint(0,8)]],[[randint(0,8),randint(0,8)]]

    moveC, movePClast= [[randint(0,8),randint(0,8)]],[[randint(0,8),randint(0,8)]]
    pm1 = 0
    i = 0
    drawingField(Pole,PolePC)  #

    if choice == '2':
        i = 2
        moveC, movePClast = movePC(moveC, movePClast, pm1, PolePC)
        pm1 = moveC[0][0]
        PolePC[pm1] = O
        Pole[pm1] = Player[i % 2]
        print()
        drawingField(Pole, PolePC, pm1)


    while (i < 9) and not controlGame(pm1):  # Певый ходит 0
        i += 1
        print()
        if i % 2:
            if choice == '3':
                moveC1, movePClast1 = movePC(moveC, movePClast, pm1, PolePC)
                pm1 = moveC1[0][0]
            else:
                pm1 = movePlayer(Pole, Player[i % 2])
        else:
            if choice == '4':
                pm1 = movePlayer(Pole, Player[i % 2])
            else:
                moveC, movePClast = movePC(moveC, movePClast, pm1, PolePC)
                pm1 = moveC[0][0]

        if i % 2:
            PolePC[pm1] = X
        else:
            PolePC[pm1] = O
        Pole[pm1] = Player[i % 2]
        drawingField(Pole, PolePC, pm1)
    else:
        if i == 9:
            print('Ничья')
        else:
            print(f'Победил игрок: {Player[i % 2]}')



runGame()

