from models import *
from misc import SeaBattleMisc


class SeaPlayer(object):

    def __init__(self, name='', order=False):
        self.name = name
        self.order = order
        self.state = False
        self.total_ship_number = 10
        self.my_object = None
        self.field = list(range(0, 100, 1))
        self.ship_one = FourDeck()
        self.ship_two = ThreeDeck()
        self.ship_three = TwoDeck()
        self.ship_four = OneDeck()
        self.player_ships = []

    def __str__(self):
        return self.name

    def declare_player_ships(self):
        ships = self.load_ships()
        for i in ships.keys():
            for z in i.positions:
                self.player_ships.append(z)

    def load_ships(self):
        return {
            self.ship_one: FourDeck,
            self.ship_two: ThreeDeck,
            self.ship_three: TwoDeck,
            self.ship_four: OneDeck,
        }

    def ship_menu(self, dicta):
        try_one = 0
        try_two = 0
        try_var = None
        def check_iteration():
            ax = None
            bx = None

            try:

                for one_try, second_try in enumerate(dicta.keys()):
                    bx = second_try
                    ax = str(second_try)
            except Exception:
                return bx

        api = check_iteration()

        if api is None:
            for index, name in enumerate(dicta.keys()):
                print('{}: {} '.format(index, name))
        if api is not None:
            dicta.pop(api)
            self.ship_menu(dicta)

    def player_init(self):
        while self.total_ship_number > 0:
            try:

                print('Необходимо расположить корабли на поле для игрока : ' + self.name)
                print('Корабли можно располагать сверху вниз и слева направо, будьте внимательны !')
                ships = self.load_ships()

                self.ship_menu(ships)

                while True:
                    try:
                        ship_choice = int(input('Выберите корабль из списка:'))
                        selected_key = list(ships.keys())[ship_choice]
                        break

                    except ValueError:
                        print('Bad input, try again.')
                    except IndexError:
                        print('Wrong index, try again.')
                    except Exception:
                        print('что-то не так')

                print('Selected: {}'.format(selected_key.label()))
                # ships.keys())[ship_choice]

                list(selected_key.get_aura(self.field))
                self.field = list(selected_key.put_ship_on_battlefield(self.field))

                self.total_ship_number -= 1

            except ValueError:
                print('Bad input, try again.')
            except IndexError:
                print('Wrong index, try again.')
        else:
            self.declare_player_ships()

    def change_field(self, arg):
        self.field = arg

    def print_field(self):
        print(self.field)


class Game(object):

    def __init__(self, player_one, player_two):
        self.order = randint(0, 1)
        self.player_one_field = player_one.field
        self.player_two_field = player_two.field
        self.player_one_ships = player_one.player_ships
        self.player_two_ships = player_two.player_ships
        self.player_one = player_one
        self.player_two = player_two
        # self.comp_vision = list(range(0, 100, 1))

    def string_one(self):
        sc = ' '
        return 'Кораблей потоплено' + sc * 9 + '[' + str(10 - len(self.player_one_ships)) + '/10]' + sc * 20 + \
        '[' + str(10 - len(self.player_two_ships)) + '/10]' + \
               '\n(1)' + sc + 'A' + sc * 2 + 'B' + sc * 2 + 'C' + sc * 2 + \
        'D' + sc * 2 + 'E' + sc * 2 + 'F' + \
        sc * 2 + 'G' + sc * 2 + 'H' + sc * 2 + 'I' + sc * 2 + 'J' + sc * 22 + 'J' + sc * 2 + \
        'I' + sc * 2 + 'H' + sc * 2 + 'G' + sc * 2 + 'F' + sc * 2 + 'E' + sc * 2 + 'D' + sc * 2 \
        + 'C' + sc * 2 + 'B' + sc * 2 + 'A' + sc * 2 + '(2) \n'

    def print_field(self):
        string_one = self.string_one()

        string_counter = 0

        # building each line of string
        for z in range(10, 101, 10):
            string_counter += 1

            # add start of line
            if string_counter < 10:
                string_one += str(string_counter) + '. '
            if string_counter == 10:
                string_one += '10.'

            # build each 10 of battlefield_one
            for i in range(z - 10, z, 1):
                if type(self.player_one_field[i]) == int:
                    string_one += '[ ]'
                else:
                    if self.player_one_field[i] == 'X':
                        string_one += '[ ]'
                    if self.player_one_field[i] == '.':
                        string_one += '[.]'
                    if self.player_one_field[i] == 'Y':
                        string_one += '[X]'


            # split battlefields
            string_one += '--------------------'

            # build each 10 of battlefield_two
            for y in range(z - 1, z - 11, -1):
                if type(self.player_two_field[y]) == int:
                    string_one += '[ ]'
                else:
                    if self.player_two_field[y] == 'X':
                        string_one += '[ ]'
                    if self.player_two_field[y] == '.':
                        string_one += '[.]'
                    if self.player_two_field[y] == 'Y':
                        string_one += '[X]'

            # add end of line
            if string_counter < 10:
                string_one += ' .' + str(string_counter)
            if string_counter == 10:
                string_one += '.10'

            string_one += '\n'

        print(string_one)

    def is_game_finished(self):

        if len(self.player_one_ships) == 0:
            print('Победил игрок {}'.format(self.player_two))
            return 0
        if len(self.player_two_ships) == 0:
            print('Победил игрок {}'.format(self.player_one))
            return 0

        else:
            return 1

    def change_order(self):
        prime = 0
        if self.order == 0:
            self.order = 1
            prime += 1
        if self.order == 1 and prime == 0:
            self.order = 0

    def load_players(self):
        return [self.player_one, self.player_two]

    def perform_game(self):

        scenario = self.is_game_finished()
        print(scenario)
        players = self.load_players()
        print('''Начинаем игру ! Случайным образом определено , что 
первым делает выстрел игрок '{}' !'''.format(players[self.order]))

        while scenario == 1:
            try:
                self.print_field()
                self.shot()
                scenario = self.is_game_finished()

            except Exception:
                print('Что-то не так')

        else:
            print('Игра завершена !')
            input('Введите любую команду для выхода: ')
            raise KeyboardInterrupt

    def perform_game_vs_comp(self, arg):
        scenario = self.is_game_finished()
        print(scenario)
        players = self.load_players()
        print('''Начинаем игру ! Случайным образом определено , что 
        первым делает выстрел игрок '{}' !'''.format(players[self.order]))
        game = ComputerPlay(arg)

        while scenario == 1:
            try:
                self.print_field()
                if self.order == 0:
                    self.shot_vs_comp()
                else:
                    game.comp_shots()

            except Exception:
                print('Что-то не так')

        else:
            print('Игра завершена !')
            input('Введите любую команду для выхода: ')
            raise KeyboardInterrupt

    def shot_vs_comp(self):
        players = self.load_players()
        command = input('Введи координаты выстрела, {} !'.format(players[self.order]))
        index_in_field = 0
        player = self.player_two_field
        ships = self.player_two_ships
        index_dict = SeaBattleMisc.dict_one
        if len(command) == 2:

            try:
                index_in_field = int(str(int(command[0]) - 1) + str(index_dict[command[1]]))
            except Exception:
                raise ValueError
        if len(command) == 3:
            try:
                index_in_field = int(str(int(command[0]) - 1) + str(int(command[1]) + 9)
                                     + str(index_dict[command[2]]))
            except Exception:
                raise ValueError

        if len(command) < 2 or len(command) > 3:
            raise ValueError

        def try_shot():
            print('стрельба')
            prime = 0
            try:
                if type(player[index_in_field]) == int:
                    print('Промах !')
                    player[index_in_field] = '.'
                    prime += 1
                    self.change_order()
                    return True
                if player[index_in_field] == 'X':
                    index_one = 0
                    index_two = 0
                    for first_index, i in enumerate(ships):
                        if index_in_field in i:
                            index_one = first_index
                            for second_index, j in enumerate(ships[index_one]):
                                if index_in_field == j:
                                    index_two = second_index

                    ships[index_one].pop(index_two)

                    if len(ships[index_one]) > 0:
                        print('ВЫ ПОПАЛИ !')
                        player[index_in_field] = 'Y'
                        return True

                    if len(ships[index_one]) == 0:
                        print('Корабль противника уничтожен !')
                        player[index_in_field] = 'Y'
                        ships.pop(index_one)
                        return True

                    else:
                        raise ValueError

                if player[index_in_field] == '.' and prime == 0:
                    print('Сюда нельзя стрелять !')
                if player[index_in_field] == 'Y':
                    print('Сюда нельзя стрелять !')

                else:
                    raise ValueError
            except Exception:
                raise ValueError

        try_shot()

    def shot(self):
        depend_of_order = [self.player_two_field, self.player_one_field]
        ships_depend_of_order = [self.player_two_ships, self.player_one_ships]
        player = depend_of_order[self.order]
        ships = ships_depend_of_order[self.order]
        players = self.load_players()

        command = input('Введи координаты выстрела, {} !'.format(players[self.order]))
        index_in_field = 0
        if self.order == 0:
            index_dict = SeaBattleMisc.dict_one
            if len(command) == 2:

                try:
                    index_in_field = int(str(int(command[0]) - 1) + str(index_dict[command[1]]))
                except Exception:
                    raise ValueError
            if len(command) == 3:
                try:
                    index_in_field = int(str(int(command[0]) - 1) + str(int(command[1]) + 9)
                                         + str(index_dict[command[2]]))
                except Exception:
                    raise ValueError

        if self.order == 1:
            index_dict = SeaBattleMisc.dict_one
            if len(command) == 2:
                try:
                    index_in_field = int(str(int(command[0]) - 1) + str(index_dict[command[1]]))
                except Exception:
                    raise ValueError
            if len(command) == 3:
                try:
                    index_in_field = int(
                        str(int(command[0]) - 1) + str(int(command[1]) + 9) + str(index_dict[command[2]]))
                except Exception:
                    raise ValueError

        if len(command) < 2 or len(command) > 3:
            raise ValueError

        def try_shot():
            print('стрельба')
            prime = 0
            try:
                # index_in_field = int(str(int(command[0])-1) + str(index_dict[command[1]]))
                if type(player[index_in_field]) == int:
                    print('Промах !')
                    player[index_in_field] = '.'
                    prime += 1
                    self.change_order()
                    return True
                if player[index_in_field] == 'X':
                    index_one = 0
                    index_two = 0
                    for first_index, i in enumerate(ships):
                        if index_in_field in i:
                            index_one = first_index
                            for second_index, j in enumerate(ships[index_one]):
                                if index_in_field == j:
                                    index_two = second_index

                    ships[index_one].pop(index_two)

                    if len(ships[index_one]) > 0:
                        print('ВЫ ПОПАЛИ !')
                        player[index_in_field] = 'Y'
                        return True

                    if len(ships[index_one]) == 0:
                        print('Корабль противника уничтожен !')
                        player[index_in_field] = 'Y'
                        ships.pop(index_one)
                        return True

                    else:
                        raise ValueError

                if player[index_in_field] == '.' and prime == 0:
                    print('Сюда нельзя стрелять !')
                if player[index_in_field] == 'Y':
                    print('Сюда нельзя стрелять !')

                else:
                    raise ValueError
            except Exception:
                raise ValueError

        try_shot()


def main():
    while True:
        pre_game = int(input('''Добро пожаловать в игру "Морской Бой"
         Выберите режим игры :
         1. - против компьютера
         2. - против человека'''))

        if pre_game == 2:

            try:
                player_one_name = input('Введите своё имя: ')
                player_one = SeaPlayer(player_one_name)
                player_one.player_init()

                player_two_name = input('Введите своё имя: ')
                player_two = SeaPlayer(player_two_name)
                player_two.player_init()

                gaming = Game(player_one, player_two)
                gaming.perform_game()

            except Exception as e:
                print('You have done something wrong!', e)

        if pre_game == 1:
            try:
                player_one_name = input('Введите своё имя: ')
                player_two = SeaPlayer('Компьютер')
                comp_field = ComputersField()
                comp_field.choose_ur_comp()
                player_two.field = comp_field.prime_field
                player_two.player_ships = comp_field.ship_pos
                player_one = SeaPlayer(player_one_name)
                gaming = Game(player_one, player_two)
                player_one.player_init()
                gaming.perform_game_vs_comp(gaming)

            except Exception as e:
                print('You have done something wrong!', e)

        else:
            print('Введена неверная команда, попробуйте снова !')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Закроем программу')
