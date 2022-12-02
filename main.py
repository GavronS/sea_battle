from random import randint
# импортируем функцию randint из библиотеки random. функция позволяет генерировать
# случайное целое число из диапазона целых чисел

class Dot:
# класс точек с двумя "волшебными методами"
# метод __eq__  позволяет сравнивать 2 точки(self и other)
# метод __repr__ возвращает значения точек в виде кортежа
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass
# класс ошибок или по другому исключений. странно что классы исключений проходят на курсе как раз
# после этого задания...


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
# класс корабля в инит записывается начальная координата корабля, его длинна(она же жизнь)
# и ориентация о(0 - вертикальный корабль, 1 - горизонтальный)
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
 # функция dots в декораторе @property возвращает список точек корабля в виде списка точек класса Dot
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

# функция shooten сравнивает точку выстрела(shot) со списком точек корабля (self.dots)
    def shooten(self, shot):
        return shot in self.dots


class Board:
#класс рисования игровой доски.В init передается не так уж и много параметров видимость доски (видимая
# собственная доска) и размер поля
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0  # в count создается счетчик убитых кораблей

        self.field = [["O"] * size for _ in range(size)]  # в списке field списки с пустыми ячейками доски
                                                          # заполненные нулями
        self.busy = []  # busy - пустой список с точками выстрелов и кораблей
        self.ships = [] # ships - список со списками точек кораблей

    def add_ship(self, ship):   # функция добавления кораблей на доску
        for d in ship.dots: #для каждой точки корабля
            if self.out(d) or d in self.busy: # если точка вне игрового поля (функция out True) или
                                              # точка содержится в списке busy  то выдается ошибка и
                                              # функция останавливется
                raise BoardWrongShipException()
        for d in ship.dots: # для каждой точки корабля
            self.field[d.x][d.y] = "■" # меняем в списке field с координатами точки знак О на "■"
            self.busy.append(d)  # добавляем точку в список busy как занятую кораблем

        self.ships.append(ship) # добавляем в список с кораблями координаты поставленного корабля
        self.contour(ship) # передаём координаты корабля функции contour

    def contour(self, ship, verb=False):
# near список с координатами сдвигаточек корабля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:  # для каждой точки корабля
            for dx, dy in near: # для каждого кортежа из near
                cur = Dot(d.x + dx, d.y + dy)  # в переменную cur записывает объект класса Dot с координатами
                # с учетом сдвига
                if not (self.out(cur)) and cur not in self.busy: # проверяем точку cur если она внутри игрового
                                                                 # поля и не занята
                    if verb: # если видимость True, по умолчанию False
                        self.field[cur.x][cur.y] = "."  # то рисуем в месте контура точку
                    self.busy.append(cur) # точку контура при выполнении предыдущих условий кроме verb, добавляем
                                          # в список busy

    def __str__(self): #волшебный метод __str__ для рисования доски из строки
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |" # верх доски заисываем в строку
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |" # добавляем к строке символ перевода строки, затем
            # номер столбца, т.к. счетчик начинается с 0, то прибавляем 1, затем строку из символов "0"
            # разделенных "|", конструкция " | ".join(row), в конце добавляем последний разделитель

        if self.hid: # если доска невидима то все символы с кораблями заменяем на 0
            res = res.replace("■", "O")
        return res

    def out(self, d): # проверяем входят ли точки внутрь игрового поля если точки входят в игровое поле то False
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d): # функция выстрела
        if self.out(d): # если точка вне игрового поля
            raise BoardOutException() # выведет результат ошибки "Вы пытаетесь выстрелить за доску!"

        if d in self.busy: # если точка в списке busy
            raise BoardUsedException() # выведет результат ошибки "Вы уже стреляли в эту клетку"

        self.busy.append(d) # если ошибки нет то точка добавится в список busy

        for ship in self.ships: # для каждого корабля из списка кораблей
            if ship.shooten(d): # если точка выстрела d принадлежит точкам корабля
                ship.lives -= 1 # жизнь корабля уменьшается на 1
                self.field[d.x][d.y] = "X" # в точке выстрела в списке field рисуется знак убитого корабля "X"
                if ship.lives == 0: # если жизнь корабля 0
                    self.count += 1 # список убитых кораблей пополняется на 1
                    self.contour(ship, verb=True) # вокруг контура корабля рисуются точки
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."   # если предыдущие условия не выполнились, в корабль не попали, рисуем точку
        print("Мимо!")
        return False

    def begin(self):   # обнуление списка busy
        self.busy = []


class Player:  # родительский класс для игроков
    def __init__(self, board, enemy): # передаются 2 значения доска игрока и соперника
        self.board = board
        self.enemy = enemy

    def ask(self): # это функция запроса координат хода игрока, будет прописана для каждого конкретного класса отдельно
        raise NotImplementedError()

    def move(self): # функция самого хода
        while True: # в цикле пока shot не выбросит False(выстрел мимо или убитый корабль)
            try:
                target = self.ask() # запрашиваем координаты выстрела игрока
                repeat = self.enemy.shot(target) # передаем их функции shot !!! не пойму почему enemy.shot а не board.shot?
                return repeat
            except BoardException as e:
                print(e)


class AI(Player): # класс игрока компьютер
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5)) # генерирует 2 координаты передаем их в класс Dot
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split() # просим ввести координаты, преобразуем в строку используя пробел
                                               # в качестве разделтеля между введенными данными

            if len(cords) != 2:  # если длинна списка не равна двум просим ввести две координаты
                print(" Введите 2 координаты! ")
                continue

            x, y = cords # первый символ списка присваиваем х, второй y

            if not (x.isdigit()) or not (y.isdigit()): # если x или y не числа то повторяем ввод
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)  # если x и y числа то строковые значения переводим в числительные

            return Dot(x - 1, y - 1) # возвращаем значение класса Dot с координатами хода


class Game:
    def __init__(self, size=6):  #создаем игру с размером доски по умолчанию 6
        self.size = size
        pl = self.random_board()  # случайная доска игрока
        co = self.random_board()  # случайная доска компьютера
        co.hid = True             # скрываем корабли компьютера

        self.ai = AI(co, pl)  # игрок компьютер
        self.us = User(pl, co) # игрок

    def random_board(self): # функция гарантированно создающая рандомную доску
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self): # класс создания рандомной доски
        lens = [3, 2, 2, 1, 1, 1, 1] # список с количествами жизней кораблей
        board = Board(size=self.size) # создаем доску
        attempts = 0 # счетчик попыток расстановки кораблей
        for l in lens: # для каждого корабля из списка lens
            while True:
                attempts += 1 # попытка +1
                if attempts > 2000: # если попыток меньше 2000 продолжаем цикл
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1)) # генерируем случайный корабль
                try:
                    board.add_ship(ship) # если корабль с такими координатами длинной и расположением встал на доску
                                         # то переходим к следующему кораблю из списка lens
                    break
                except BoardWrongShipException:
                    pass
        board.begin() # обнуляем список busy перед следующей расстановкой или игрой
        return board

    def board_game (self): # попытка написать функцию вывода игровых досок на одном уровне. к сожалению не могу
                           # разобраться как вывести результат в функцию loop
        pl_ = str(self.us.board).split("\n")
        ai_ = str(self.ai.board).split("\n")
        for x1, x2 in zip(pl_, ai_):
            x3 = (f'{str(x1)} {" " * 10} {str(x2)}')
            print (x3)




    def greet(self):   # приветствие игры
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            # здесь функция вывода игровых досок и запроса хода игроков. в функции board_game тот же код что и
            # ниже но в отличии от результатов функции код здесь работает
            print("-" * 70)
            print(f'  Доска пользователя: {" "* 18} Доска компьютера:')
            pl_ = str(self.us.board).split("\n") # из строк получаем список со строками по рядам
            ai_ = str(self.ai.board).split("\n")
            for x1, x2 in zip(pl_, ai_): # здесь через функцию zip получаем итераторы x1 и x2 преобразуя
                                         # в строки выводим на печать с отступами
                print(f'{str(x1)} {" "* 10} {str(x2)}')
            if num % 2 == 0:
                print("-" * 70)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 70)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 70)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 70)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()