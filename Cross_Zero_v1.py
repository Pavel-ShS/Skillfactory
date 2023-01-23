
class TextColor:
    RED = '\033[31m'
    PURPLE = '\033[1;35m'
    GREEN = '\033[1;92m'
    FAIL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Приветсвие
def greet():
    print(' ----------------------')
    print('|   Добро пожаловать   |')
    print('|       в игру         |')
    print(f'|   {TextColor.GREEN}Крестики-{TextColor.PURPLE}нолики{TextColor.ENDC}    |')
    print(' ----------------------')
    print()
    print(f'Помощь - {TextColor.FAIL}help{TextColor.ENDC}')
    print(f'Изменить параметры игры введите - {TextColor.FAIL}setup{TextColor.ENDC}')
    print(f'Выход - {TextColor.FAIL}quit{TextColor.ENDC}')
    print('')


def help_game():
    print('----------------')
    print('Крестики-нолики')
    print('     логическая игра между двумя противниками на квадратном поле 3 на 3 клетки.\n'
          '     Один из игроков играет «крестиками», второй — «ноликами»')
    print('Правила: \n'
          '     Игроки по очереди ставят на свободные клетки свои знаки\n'
          '     (один всегда крестики, другой всегда нолики).\n'
          '     Первый, выстроивший в ряд 3 своих фигуры \n'
          '     по вертикали, горизонтали или диагонали, выигрывает.\n'
          '     Первый ход делает игрок, ставящий крестики.')
    print()
    input('Нажмите <ENTER> для продолжения... ')
    print()
    print(f'     Игру можно разнообразить ввести {TextColor.FAIL}setup{TextColor.ENDC} в начале игры')
    print('     выбрать ряд размером 3 или 5')
    print('     и увеличить размер поля по ширине и высоте')
    print(f'{TextColor.FAIL}     при изменении стандартных параметров')
    print(f'     условия игры изменяются: {TextColor.BOLD}выиграет тот, кто больше собрал рядов{TextColor.ENDC}')
    print()


# Проверка на цифры при вводе
def try_int(n):
    while True:
        try:
            int(n)
            break
        except ValueError:
            n = input(f'{TextColor.FAIL}<err> введите цифры: {TextColor.ENDC}')
            continue
    return int(n)


# Настройки игры
def setup(width_size_, height_size_, win_lot_):
    print()
    print(f'размер ряда, который нужно собрать = {win_lot_}')
    print(f'размер поля = {width_size_} х {height_size_} клеток')
    print()
    ask_setup = input('Хотите изменить? Y/N: ')
    if ask_setup.lower() == 'y':
        while True:
            win_lot_ = input('Введите размер ряда 3 или 5: ')
            win_lot_ = try_int(win_lot_)
            if win_lot_ == 5 or win_lot_ == 3:
                break
            print(f'{TextColor.FAIL}<err> Значение не соответствует условию{TextColor.ENDC}')
        while True:
            print()
            print('Размер поля:')
            size_dict = {1: (3, 3), 2: (5, 5), 3: (10, 10), 4: (15, 15)}
            print('1 - 3x3, 2 - 5x5, 3 - 10x10, 4 - 15x15, 0 - свой')
            size_ = input('Выберите размер поля:')
            size_ = try_int(size_)
            if size_ == 0:
                print()
                print(f'{TextColor.FAIL}Есть ограничение в размере '
                      f'по горизонтали и по вертикали, не более 20 клеток{TextColor.ENDC}')
                print()
                width_size_ = input('Введите ширину поля: ')
                width_size_ = try_int(width_size_)
                height_size_ = input('Введите высоту поля: ')
                height_size_ = try_int(height_size_)
                if width_size_ < 2 or height_size_ < 2:
                    print()
                    print(f'{TextColor.FAIL}В одну строку не интересно играть :( {TextColor.ENDC}')
                    continue
                elif width_size_ < win_lot_ and height_size_ < win_lot_:
                    print()
                    print(f'{TextColor.FAIL}На таком поле невозможно собрать ряд{TextColor.ENDC}')
                    continue
                elif width_size_ > 20 or height_size_ > 20:
                    print()
                    print(f'{TextColor.FAIL}Ограничение! не более 20 клеток{TextColor.ENDC}')
                    continue
                break
            elif 0 < size_ < 5:
                width_size_, height_size_ = size_dict[size_]
                print(f'Вы выбрали поле {width_size_}х{height_size_} клеток')
                if win_lot_ > width_size_:
                    print(f'{TextColor.FAIL}<err> На таком поле '
                          f'невозможно собрать ряд размером {win_lot_}{TextColor.ENDC}')
                    continue
                break
            else:
                print(f'{TextColor.FAIL}<err>неизвестная команда{TextColor.ENDC}')

    elif ask_setup.lower() != 'n':
        print(f'{TextColor.FAIL}<err> неверная команда{TextColor.ENDC}')
        setup(width_size_, height_size_, win_lot_)
    print()
    print(f'размер ряда = {win_lot_}')
    print(f'Размер поля = {width_size_} х {height_size_}')

    return int(width_size_), int(height_size_), int(win_lot_)


# Рисует игровое поле
def draw_field(play_list, width_):
    print('-' + '-' * 4 * width_)
    for i in play_list:
        print('|', end='')
        for row in i:
            if type(row) == int:
                row += 1
            if len(str(row)) == 1 or len(str(row)) > 3:
                print(f' {row} |', end='')
            elif len(str(row)) == 2:
                print(f' {row}|', end='')
            else:
                print(f'{row}|', end='')
        print()
        print('-' + '-' * 4 * width_)


# Функция создания игрового списка и выйгрышных позиций
def lists_play_and_win_position(w, h, win_lot_):
    def create_win_position(field, a):  # создание списков по размеру win_lot
        tmp = []
        for i in field:
            j = 0
            while j < len(i):
                k = i[j: j + a]
                if len(k) >= a:
                    tmp.extend([k])
                j += 1
        return tmp

    def create_cross(field, width_, height_):  # создание диагоналей
        a = 1
        b = 0
        tmp = []
        while a >= -1:
            d = -height_
            x = height_
            if width_ >= height_:
                d = -width_
                x = width_
            while d <= x:
                while_list = []
                while_list.extend([row[a * (i + d) + a * b] for i, row in enumerate(field) if 0 <= i + d < len(row)])
                tmp.extend([while_list])
                d += 1
            b += 1
            a -= 2
        return tmp

    horizontal_arr = [[j + i * w for j in range(w)] for i in range(h)]
    h_list = create_win_position(horizontal_arr, win_lot_)

    vertical_arr = [[i + j * w for j in range(h)] for i in range(w)]
    v_list = create_win_position(vertical_arr, win_lot_)

    cross_arr = create_cross(horizontal_arr, w, h)
    cross_list = create_win_position(cross_arr, win_lot_)

    win_positions = h_list + v_list + cross_list

    return horizontal_arr, win_positions


# Проверка сколько собранный рядов
def collect_win_line_player(win_field, user):
    score_ = 0
    for p in win_field:
        if all(i == user for i in p):
            score_ += 1
            win_field.remove(p)
    return score_, win_field


# Показывает результат
def show_winner(dict_, p1, p2):
    print()
    print(f'{p1} закрыл линий = {dict_[p1]}')
    print(f'{p2} закрыл линий = {dict_[p2]}')
    print()
    if dict_[p1] == dict_[p2]:
        return f'{TextColor.FAIL}ничья{TextColor.ENDC}'
    elif dict_[p1] > dict_[p2]:
        return f'{TextColor.RED}Выиграл {TextColor.ENDC}{p1}\n' \
               f'{TextColor.RED}Поздравляем!!!{TextColor.ENDC}'

    else:
        return f'{TextColor.RED}Выиграл {TextColor.ENDC}{p2}\n' \
               f'{TextColor.RED}Поздравляем!!!{TextColor.ENDC}'


# игра
def play_game(play_list, width_, height_, line, win_lines):
    count = 0
    player1 = f'{TextColor.GREEN}X{TextColor.ENDC}'
    player2 = f'{TextColor.PURPLE}O{TextColor.ENDC}'
    tmp_dict = {player1: 0, player2: 0}  # Временный словарь посчета очков
    lock_list = []
    while True:
        if count % 2 == 0:
            user = player1
        else:
            user = player2
        if count < width_ * height_:
            x = ask(play_list, user, width_, height_, lock_list)
            for r in play_list:  # подставляем Х или О, изменяем игровой список.
                for i, j in enumerate(r):
                    if j == x-1:
                        r[i] = user
            for r in win_lines:  # подставляем Х или О в список выигрышных позиций.
                for i, j in enumerate(r):
                    if j == x-1:
                        r[i] = user
        elif count == width_ * height_:
            draw_field(play_list, width_)
            print(f'{TextColor.FAIL}Ходы закончились{TextColor.ENDC}')
            break
        score, win_lines = collect_win_line_player(win_lines, user)  # Считает сколько закрыто линий
        tmp_dict[user] += score
        if line == width_ == height_ == 3:  # с полем 3х3 стандартная игра, кто первый закроет ряд из 3 знаков
            if tmp_dict[user] == 1:
                draw_field(play_list, width_)
                break
        count += 1
    print(show_winner(tmp_dict, player1, player2))


# Запрос хода от игрока
def ask(play_list_, player_, width_, height_, lock_):
    draw_field(play_list_, width_)
    x = None
    while True:
        print()
        place = input(f"Ходит {player_}. Введите номер клетки:")
        if place.lower() == 'quit':
            exit('Выход из игры')
        if not place.isdigit():
            print('Введите цифры')
            continue
        x = int(place)
        if not (0 < x <= height_ * width_):
            print('Нет такой клетки')
            continue
        if x in lock_:
            print('Клетка занята')
            continue
        lock_.append(x)
        break
    print()
    return x


# Перезапуск игры
def restart():
    ask_repeat = input('Повторим? Y/N: ')
    if ask_repeat.lower() == 'n':
        print('выход из игры')
        exit()
    if ask_repeat.lower() != 'y':
        print(f'{TextColor.FAIL}<err> неверная команда{TextColor.ENDC}')
        restart()


greet()

# Значения по умолчанию
width_size = 3
height_size = 3
win_lot = 3

while True:
    ask_user = input('Для начала игры нажмите <Enter> или введите команду:')
    if ask_user.lower() == 'quit':
        print()
        print('Выход из игры')
        exit(0)
    elif ask_user.lower() == 'setup':
        width_size, height_size, win_lot = setup(width_size, height_size, win_lot)
        continue
    elif ask_user.lower() == 'help':
        help_game()
        continue

    play_field, win_list = lists_play_and_win_position(width_size, height_size, win_lot)
    play_game(play_field, width_size, height_size, win_lot, win_list)
    print()
    restart()
    print()
