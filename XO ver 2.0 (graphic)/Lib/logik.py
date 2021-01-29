from random import choice
# Игровые константы
N = 3  # необходимое количество для победы

X = 4  # вес которым отображается Х
O = 3  # вес которым отображается O
EMPTY = 1  # вес не занятой ячейки

COFFICIENT={}

DIC = {0: [[x for x in range(-N + 1, N)], [0 for y in range(-N + 1, N)]],  # - -2---2 0
       1: [[x for x in range(-N + 1, N)], [y for y in range(-N + 1, N)]],  # \
       2: [[0 for x in range(-N + 1, N)], [y for y in range(-N + 1, N)]],  # |
       3: [[x for x in range(-N + 1, N)], [y for y in range(N - 1, -N, -1)]]  # /
       }

def init_coefficient():
    ves = N * 2
    cof = {(str(X) * (N - i - 1)).rjust(N, str(EMPTY)): ves - i*2 for i in range(N - 1)}
    ves = N * 2 - 1
    cof.update({(str(O) * (N - i - 1)).rjust(N, str(EMPTY)): ves - i*2 for i in range(N - 1)})
    cof.update({(str(O)*(N//i)+str(X)*(N//i)).rjust(N,str(EMPTY)):i for i in range(2,N-1)})
    for key, value in cof.items():
        print(key,value)
    return cof


# версия с одномерным списком работает хорошо
def check_win(point: int, field: list, win, NN):  # win - X или O
    x, y = point % NN, point // NN  ##1 x=1,y=0 # переводим одномерную точку в x y
    for key, value in DIC.items():
        count = 0
        for index in range(N * 2 - 1):
            xx = DIC[key][0][index]
            yy = DIC[key][1][index]
            if all([x + xx in range(NN), y + yy in range(NN)]):
                count = count + 1 if field[x + xx + (y + yy) * NN] == win else 0
            if count == N:
                return True
    return False


# работает
def get_computer_move(b, NN):

    w = [0] * NN * NN

    for index in range(NN * NN):
        # print(b)
        if b[index] == EMPTY:  # EMPTY пустая ячейка
            x, y = index % NN, index // NN  ##1 x=1,y=0 # переводим одномерную точку в x y
            q = []
            for key in DIC:
                # список обхода по дополнительным координатам от словаря
                ray = [b[x + DIC[key][0][i] + (y + DIC[key][1][i]) * NN] if all(
                    [x + DIC[key][0][i] in range(NN), y + DIC[key][1][i] in range(NN)]) else 0 for i in
                       range(N * 2 - 1)]
                q.append(get_coffigient(N, ray))
                w[index] = (max(q))
    for i in range(NN):
         print('w', i, w[i * NN:i * NN + NN])
    maksim = [index for index, value in enumerate(w) if value == max(w)]
    hod = choice(maksim)
    print('компьютер выбрал', hod)
    return hod


# РЕДАКТИРУЕМ  ВАРИАНТ 1
def get_coffigient(n: int, ray: list):
    rays = [ray[i:i + n] for i in range(n)]
    st_rays=[''.join(list(map(str, sorted(rays[i])))) for i in range(n)]
    mak=0
    for i in st_rays:
        if mak<COFFICIENT.get(i,1):
            mak=COFFICIENT.get(i,1)
    return mak

COFFICIENT = init_coefficient()

