from seabattle import *
from misc import SeaBattleMisc
from random import randint
from random import choice
import time


class BattleField(object):

    @staticmethod
    def print_field_when_put_ships(battlefield_start):
        sc = ' '

        # Title_string in string_one default( coordinats ), sc = empty space
        string_one = '(1)' + sc + 'A' + sc * 2 + 'B' + sc * 2 + 'C' + sc * 2 + 'D' + sc * 2 + 'E' + sc * 2 + 'F' + \
                     sc * 2 + 'G' + sc * 2 + 'H' + sc * 2 + 'I' + sc * 2 + 'J' + '\n'

        string_counter = 0

        for z in range(10, 101, 10):
            string_counter += 1

            if string_counter < 10:
                string_one += str(string_counter) + '. '
            if string_counter == 10:
                string_one += '10.'

            for i in range(z - 10, z, 1):
                if type(battlefield_start[i]) == int:
                    string_one += '[ ]'
                else:
                    string_one += '[' + str(battlefield_start[i]) + ']'
            string_one += '\n'
        return string_one

    @staticmethod
    def valid_compare(arg1, arg2, vector=None):
        a = arg1  # текущий
        b = arg2  # предыдущий

        if vector is not None:
            if vector == 0:
                if b + 10 == a:
                    return True
                else:
                    print('Так нельзя ставить')
                    raise ValueError
            if vector == 1:
                if str(b + 1)[1] != 0:
                    if b + 1 == a:
                        return True
                else:
                    print('Так нельзя ставить')
                    raise ValueError
        else:
            if len(str(a)) == 1:
                if len(str(b)) == 1:
                    if b < 9:
                        if b + 1 == a:
                            return True
                        else:
                            raise ValueError
            if len(str(a)) == 2:
                if len(str(b)) == 1:
                    if b + 10 == a:
                        return True
                    else:
                        raise ValueError
                if len(str(b)) == 2:
                    if a == b + 10:
                        return True
                    if str(b + 1)[1] != 0:
                        if b + 1 == a:
                            return True
                        else:
                            raise ValueError

            else:
                print('так нельзя ставить')
                raise ValueError

    def __init__(self):
        self.field = None
        self.prev_choice = None
        self.aured_field = None
        self.vector = None
        self.direction = None

    def set_prev_choice(self, arg):
        self.prev_choice = arg
    def set_vector(self, arg):
        self.vector = arg

    def legitchoice(self, your_choice, prev_field, aura_field):

        index_dict = SeaBattleMisc.dict_one
        command = your_choice
        index_in_field = 1111
        if len(command) == 2:

            try:
                index_in_field = int(str(int(command[0]) - 1) + str(index_dict[command[1]]))
            except Exception:
                raise ValueError
        if len(command) == 3:
            try:
                index_in_field = int(str(int(command[0]) - 1) + str(int(command[1]) + 9) + str(index_dict[command[2]]))
            except Exception:
                raise ValueError

        def try_put_on_field():
            try:
                #index_in_field = int(str(int(command[0])-1) + str(index_dict[command[1]]))
                if type(aura_field[index_in_field]) == int and type(self.field[index_in_field]) == int:
                    print('Подтверждаю')
                    self.field[index_in_field] = 'X'
                    if self.prev_choice is not None:
                        vector = (index_in_field - self.prev_choice) % 2
                        self.set_vector(vector)

                    self.set_prev_choice(index_in_field)
                    return prev_field
                else:
                    raise ValueError

            except ValueError:
                print('что-то не так')
                raise ValueError
            except IndexError:
                print('неверный ввод')
                raise IndexError
            except Exception:
                raise ValueError

        if self.prev_choice is not None:
            self.valid_compare(index_in_field, self.prev_choice, self.vector)
            try_put_on_field()
            return index_in_field
        else:
            try_put_on_field()
            return index_in_field

    def declare_ship(self, size, prev_field, aura_field):
        checked_choice = []

        while size > 0:
            try:

                print(self.print_field_when_put_ships(prev_field))
                print('Осталось {} клетки корабля'.format(str(size)))
                my_choice = input('Введите координаты клетки куда хотите поставить корабль \n')
                self.field = prev_field
                checked_choice.append(self.legitchoice(my_choice, prev_field, aura_field))
                size -= 1

            except ValueError:
                print('вы ошиблись')
            except IndexError:
                print('вы ошиблись')
        else:
            print('Корабль декларирован !')
            return self.field, checked_choice


class BattleShip(object):

    def __init__(self):
        pass

    @staticmethod
    def get_aura(prev_field):
        right_field = prev_field.copy()
        for z, i in enumerate(prev_field):
            if type(i) == str and i == 'X':

                try:
                    if type(right_field[z + 1]) == int and z + 1 >= 0:
                        if len(str(z)) == 1 and z != 9:
                            right_field[z + 1] = 'Y'
                        if len(str(z)) == 2 and int(str(z)[1]) != 9:
                            right_field[z + 1] = 'Y'

                    if type(right_field[z - 1]) == int and z - 1 >= 0:
                        if len(str(z)) == 1 and z - 1 >= 0:
                            right_field[z - 1] = 'Y'
                        if len(str(z)) == 2 and int(str(z)[1]) != 0:
                            right_field[z - 1] = 'Y'

                    if type(right_field[z - 10]) == int and z - 10 >= 0:
                        right_field[z - 10] = 'Y'

                    if type(right_field[z + 10]) == int and z + 10 <= 99:
                        right_field[z + 10] = 'Y'

                    if type(right_field[z - 11]) == int and z - 11 >= 0:
                        if len(str(z)) == 2 and int(str(z)[1]) != 0:
                            right_field[z - 11] = 'Y'

                    if type(right_field[z + 11]) == int and z + 11 <= 99:
                        if len(str(z)) == 2 and int(str(z)[1]) != 9:
                            right_field[z + 11] = 'Y'
                        if len(str(z)) == 1 and z != 9:
                            right_field[z + 11] = 'Y'

                    if type(right_field[z - 9]) == int and z - 9 >= 0:
                        if len(str(z)) == 2 and int(str(z)[1]) != 9:
                            right_field[z - 9] = 'Y'
                        if len(str(z)) == 1 and z != 9:
                            right_field[z - 9] = 'Y'

                    if type(right_field[z + 9]) == int and z + 9 <= 99:
                        if len(str(z)) == 2 and int(str(z)[1]) != 0:
                            right_field[z + 9] = 'Y'
                        if len(str(z)) == 1 and z != 0:
                            right_field[z + 9] = 'Y'

                except Exception:

                    continue
        return right_field


class FourDeck(BattleShip):

    # four cages in battlefield

    @staticmethod
    def label():
        return 'FourDeck'

    def __init__(self):
        super().__init__()
        self.number = 1
        self.extra_var = None
        self.size = 4
        self.positions = []

    def __str__(self):
        if self.number > 0:
            return ' Четырёхпалубный ({}) осталось'.format(self.number)

    def change_number_of_ships(self):
        self.number -= 1

    def put_ship_on_battlefield(self, prev_field):
        current_pos = None

        if self.number > 0:
            ship_size = self.size
            put_ship = BattleField()
            aura_field = self.get_aura(prev_field)
            self.extra_var, current_pos = put_ship.declare_ship(ship_size, prev_field, aura_field)
            self.positions.append(current_pos)
            self.change_number_of_ships()
            return self.extra_var

        else:
            raise ValueError


class ThreeDeck(BattleShip):

    # three cages in battlefield

    @staticmethod
    def label():
        return 'ThreeDeck'

    def __init__(self):
        super().__init__()
        self.number = 2
        self.extra_var = None
        self.size = 3
        self.positions = []

    def __str__(self):
        if self.number > 0:
            return ' Трёхпалубный ({}) осталось'.format(self.number)

    def change_number_of_ships(self):
        self.number -= 1

    def put_ship_on_battlefield(self, prev_field):
        current_pos = []

        if self.number > 0:
            ship_size = self.size
            put_ship = BattleField()
            aura_field = self.get_aura(prev_field)
            self.extra_var, current_pos = put_ship.declare_ship(ship_size, prev_field, aura_field)
            self.positions.append(current_pos)
            self.change_number_of_ships()
            return self.extra_var

        else:
            raise ValueError


class TwoDeck(BattleShip):

    # two cages in battlefield

    @staticmethod
    def label():
        return 'TwoDeck'

    def __init__(self):
        super().__init__()
        self.number = 3
        self.extra_var = None
        self.size = 2
        self.positions = []

    def __str__(self):
        if self.number > 0:
            return ' Двухпалубный ({}) осталось'.format(self.number)

    def change_number_of_ships(self):
        self.number -= 1

    def put_ship_on_battlefield(self, prev_field):
        current_pos = []

        if self.number > 0:
            ship_size = self.size
            put_ship = BattleField()
            aura_field = self.get_aura(prev_field)
            self.extra_var, current_pos = put_ship.declare_ship(ship_size, prev_field, aura_field)
            self.positions.append(current_pos)
            self.change_number_of_ships()
            return self.extra_var

        else:
            raise ValueError


class OneDeck(BattleShip):

    # one cage in battlefield

    @staticmethod
    def label():
        return 'FourDeck'

    def __init__(self):
        super().__init__()
        self.number = 4
        self.extra_var = None
        self.size = 1
        self.positions = []

    def __str__(self):
        if self.number > 0:
            return ' Однопалубный ({}) осталось'.format(self.number)

    def change_number_of_ships(self):
        self.number -= 1

    def put_ship_on_battlefield(self, prev_field):
        current_pos = []

        if self.number > 0:
            ship_size = self.size
            put_ship = BattleField()
            aura_field = self.get_aura(prev_field)
            self.extra_var, current_pos = put_ship.declare_ship(ship_size, prev_field, aura_field)
            self.positions.append(current_pos)
            self.change_number_of_ships()
            return self.extra_var

        else:
            raise ValueError


class ComputersField(object):

    def __init__(self):

        self.prime_field = list(range(0, 100, 1))
        self.possible_indexs = []
        self.aura_field = []
        self.list_of_ships_big = [['X', 'X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X'], ['X', 'X'],
        ['X', 'X']]
        self.list_of_ships_small = [['X'], ['X'], ['X'], ['X']]
        self.y_index = []
        self.ship_pos = []

    def first_quater(self):
        a = - 1
        for i in range(10, 101, 10):
            a += 1
            n = i - a
            while n != i:
                self.prime_field[n] = 'Y'
                n += 1
            else:
                continue

    def second_quater(self):
        a = -1
        for i in range(10, 101, 10):
            a += 1
            n = i + a
            while n != i-1 and n < 100:
                self.prime_field[n] = 'Y'
                n -= 1
            else:
                continue

    def third_quater(self):
        a = 2

        for i in range(10, 101, 10):
            n = i - a
            a += 1
            while n != (i - 11) and n > -1:
                self.prime_field[n] = 'Y'
                n -= 1
            else:
                continue

    def fourth_quater(self):
        a = 1

        for i in range(0, 100, 10):
            n = i + a
            a += 1
            while n != i + 10:
                self.prime_field[n] = 'Y'
                n += 1
            else:
                continue

    def whole_field(self):
        pass

    def choose_algorhytm(self):
        result = randint(0, 1)
        if result == 0:
            self.perform_field_algo_one()
        if result == 1:
            self.perform_field_algo_two()

    def load_quaters_as_list(self):
        return [self.first_quater, self.second_quater, self.third_quater, self.fourth_quater]

    def random_choose_quater(self):
        a_list_of_quaters = self.load_quaters_as_list()
        index_of_quater = randint(0, 3)
        a_list_of_quaters[index_of_quater]()
        self.aura_field = self.prime_field

    def everything_possible(self, index_of_length):

        if index_of_length == 4:
            for i in self.aura_field:
                if type(i) == int:
                    if len(str(i)) == 1:
                        if type(self.aura_field[i + 1]) == int and len(str(i+1)) == 1:
                            if type(self.aura_field[i + 2]) == int and len(str(i+1)) == 1:
                                if type(self.aura_field[i + 3]) == int and len(str(i+3)) == 1:
                                    self.possible_indexs.append(i)
                        if type(self.aura_field[i + 10]) == int:
                            if type(self.aura_field[i + 20]) == int:
                                if type(self.aura_field[i + 30]) == int:
                                    self.possible_indexs.append(i+100)
                    if len(str(i)) == 2:
                        if i + 3 <= 99:
                            if type(self.aura_field[i + 1]) == int and str(i+1)[0] == str(i)[0]:
                                if type(self.aura_field[i + 2]) == int and str(i+2)[0] == str(i)[0]:
                                    if type(self.aura_field[i + 3]) == int and str(i+3)[0] == str(i)[0]:
                                        self.possible_indexs.append(i)
                        if i + 30 <= 99:
                            if type(self.aura_field[i + 10]) == int:
                                if type(self.aura_field[i + 20]) == int:
                                    if type(self.aura_field[i + 30]) == int:
                                        self.possible_indexs.append(i+100)
                else:
                    continue

        if index_of_length == 3:
            for i in self.aura_field:
                if type(i) == int:
                    if len(str(i)) == 1:
                        if type(self.aura_field[i + 1]) == int and len(str(i+1)) == 1:
                            if type(self.aura_field[i + 2]) == int and len(str(i+2)) == 1:
                                self.possible_indexs.append(i)
                        if type(self.aura_field[i + 10]) == int:
                            if type(self.aura_field[i + 20]) == int:
                                self.possible_indexs.append(i+100)
                    if len(str(i)) == 2:
                        if i + 2 <= 99:
                            if type(self.aura_field[i + 1]) == int and str(i+1)[0] == str(i)[0]:
                                if type(self.aura_field[i + 2]) == int and str(i+2)[0] == str(i)[0]:
                                    self.possible_indexs.append(i)
                        if i + 20 <= 99:
                            if type(self.aura_field[i + 10]) == int:
                                if type(self.aura_field[i + 20]) == int:
                                    self.possible_indexs.append(i+100)
        if index_of_length == 2:
            for i in self.aura_field:
                if type(i) == int:
                    if len(str(i)) == 1:
                        if type(self.aura_field[i + 1]) == int and len(str(i+1)) == 1:
                            self.possible_indexs.append(i)
                        if type(self.aura_field[i + 10]) == int:
                            self.possible_indexs.append(i+100)
                    if len(str(i)) == 2:
                        if i + 1 <= 99:
                            if type(self.aura_field[i + 1]) == int and str(i + 1)[0] == str(i)[0]:
                                self.possible_indexs.append(i)
                        if i + 10 <= 99:
                            if type(self.aura_field[i + 10]) == int:
                                self.possible_indexs.append(i+100)
        if index_of_length == 1:
            for i in self.aura_field:
                if type(i) == int:
                    self.possible_indexs.append(i)

    def get_aura(self):
        spec_var = BattleShip()
        self.aura_field = spec_var.get_aura(self.prime_field)

    def put_ships(self):
        for i in self.list_of_ships_big:
            len_ship = len(i)
            self.everything_possible(len_ship)
            ship_to_put = choice(self.possible_indexs)
            ship_for_list = []
            if len(str(ship_to_put)) <= 2:
                if len_ship == 4:

                    self.prime_field[ship_to_put] = 'X'
                    ship_for_list.append(ship_to_put)

                    self.prime_field[ship_to_put + 1] = 'X'
                    ship_for_list.append(ship_to_put + 1)

                    self.prime_field[ship_to_put + 2] = 'X'
                    ship_for_list.append(ship_to_put + 2)

                    self.prime_field[ship_to_put + 3] = 'X'
                    ship_for_list.append(ship_to_put + 3)

                if len_ship == 3:
                    self.prime_field[ship_to_put] = 'X'
                    ship_for_list.append(ship_to_put)

                    self.prime_field[ship_to_put + 1] = 'X'
                    ship_for_list.append(ship_to_put + 1)

                    self.prime_field[ship_to_put + 2] = 'X'
                    ship_for_list.append(ship_to_put + 2)

                if len_ship == 2:
                    self.prime_field[ship_to_put] = 'X'
                    ship_for_list.append(ship_to_put)

                    self.prime_field[ship_to_put + 1] = 'X'
                    ship_for_list.append(ship_to_put + 1)

            if len(str(ship_to_put)) == 3:
                if len_ship == 4:
                    self.prime_field[ship_to_put - 100] = 'X'
                    ship_for_list.append(ship_to_put - 100)
                    self.prime_field[ship_to_put - 90] = 'X'
                    ship_for_list.append(ship_to_put - 90)
                    self.prime_field[ship_to_put - 80] = 'X'
                    ship_for_list.append(ship_to_put - 80)
                    self.prime_field[ship_to_put - 70] = 'X'
                    ship_for_list.append(ship_to_put - 70)
                if len_ship == 3:
                    self.prime_field[ship_to_put - 100] = 'X'
                    ship_for_list.append(ship_to_put - 100)
                    self.prime_field[ship_to_put - 90] = 'X'
                    ship_for_list.append(ship_to_put - 90)
                    self.prime_field[ship_to_put - 80] = 'X'
                    ship_for_list.append(ship_to_put - 80)
                if len_ship == 2:
                    self.prime_field[ship_to_put - 100] = 'X'
                    ship_for_list.append(ship_to_put - 100)
                    self.prime_field[ship_to_put - 90] = 'X'
                    ship_for_list.append(ship_to_put - 90)

            self.ship_pos.append(ship_for_list)
            self.get_aura()
            self.possible_indexs = []

    def refresh_prime_field(self):
        temp_field = list(range(1, 101, 1))
        for index, i in enumerate(self.prime_field):
            if i == 'Y':
                temp_field[index] = index
                self.y_index.append(index)
            else:
                temp_field[index] = i
        self.prime_field = temp_field
        self.get_aura()
        for second_index, y in enumerate(self.aura_field):
            if second_index in self.y_index:
                if type(y) != int:
                    self.aura_field[second_index] = 'Z'
            else:
                self.aura_field[second_index] = 'Z'

    def put_little_ships(self):
        for i in self.list_of_ships_small:
            ship_for_list = []
            len_ship = 1
            self.everything_possible(len_ship)
            ship_to_put = choice(self.possible_indexs)
            self.prime_field[ship_to_put] = 'X'
            ship_for_list.append(ship_to_put)

            self.ship_pos.append(ship_for_list)
            self.get_aura()
            self.possible_indexs = []

    def perform_field_algo_one(self):
        self.random_choose_quater()
        self.put_ships()
        self.refresh_prime_field()
        self.put_little_ships()

    def perform_field_algo_two(self):
        self.aura_field = self.prime_field
        self.put_ships()
        self.put_little_ships()

    def choose_ur_comp(self):
        command = int(input('''Выберите уровень сложности компьютера:
        1. - средний 
        2. - сложный
        3. - сложный если играете часто '''))
        if command == 1:
            self.perform_field_algo_two()
            print('Выбран "средний" уровень сложности !')
            return True
        if command == 2:
            self.perform_field_algo_one()
            print('Выбран "сложный" уровень сложности !')
            return True
        if command == 3:
            self.choose_algorhytm()
            print('Выбран "сложный если играете часто" уровень сложности !')
            return True
        else:
            print('Команда введена не верно, попробуйте ещё раз ...')
            self.choose_ur_comp()


class ComputerPlay(object):

    def __init__(self, my_obj):

        self.last_move = 0
        self.computer_vision = list(range(0, 100, 1))
        self.gun = my_obj
        self.list_of_necessary_shots = []
        self.list_of_possible_shots = []
        self.prime = 0
        self.focus_on_ship = 0
        self.destroy_ship_list = []
        self.first_catch = None

    def check_game(self):

        print(self.gun.player_one)

    def necessary_to_shot(self, arg):

        if len(str(arg)) == 1:
            if arg == 0:
                if type(self.computer_vision[arg+1]) == int:
                    self.list_of_necessary_shots.append(arg+1)
                if type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)

            if arg == 9:
                if type(self.computer_vision[arg-1]) == int:
                    self.list_of_necessary_shots.append(arg-1)
                if type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)

            if arg >= 1 and arg <= 8:
                if type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)
                if type(self.computer_vision[arg-1]) == int:
                    self.list_of_necessary_shots.append(arg-1)
                if type(self.computer_vision[arg+1]) == int:
                    self.list_of_necessary_shots.append(arg+1)

        if len(str(arg)) == 2:
            if int(str(arg)[1]) == 9:
                if type(self.computer_vision[arg-1]) == int:
                    self.list_of_necessary_shots.append(arg-1)
                if arg <= 89 and type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)
                if arg >= 10 and type(self.computer_vision[arg - 10]) == int:
                    self.list_of_necessary_shots.append(arg - 10)

            if int(str(arg)[1]) == 0:
                if type(self.computer_vision[arg+1]) == int:
                    self.list_of_necessary_shots.append(arg+1)
                if arg <= 89 and type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)
                if arg >= 10 and type(self.computer_vision[arg - 10]) == int:
                    self.list_of_necessary_shots.append(arg - 10)

            if int(str(arg)[1]) >= 1 and int(str(arg)[1]) <= 8:
                if type(self.computer_vision[arg-1]) == int:
                    self.list_of_necessary_shots.append(arg-1)
                if type(self.computer_vision[arg+1]) == int:
                    self.list_of_necessary_shots.append(arg+1)
                if arg <= 89 and type(self.computer_vision[arg + 10]) == int:
                    self.list_of_necessary_shots.append(arg + 10)
                if arg >= 10 and type(self.computer_vision[arg - 10]) == int:
                    self.list_of_necessary_shots.append(arg - 10)

    def aura_for_vision(self):
        spec_var = BattleShip()
        self.computer_vision = spec_var.get_aura(self.computer_vision)

    def list_of_shots(self):
        for i in self.computer_vision:
            if type(i) == int:
                self.list_of_possible_shots.append(i)

    def create_focus_list(self, arg):

        vector = (arg - self.first_catch) % 2

        if vector == 0:

            if self.first_catch == arg+10:
                if type(self.computer_vision[arg + 20]) == int:
                    self.destroy_ship_list.append(arg + 20)
                if type(self.computer_vision[arg - 10]) == int:
                    self.destroy_ship_list.append(arg - 10)
                if type(self.computer_vision[arg + 30]) == int:
                    self.destroy_ship_list.append(arg + 30)
                if type(self.computer_vision[arg - 20]) == int:
                    self.destroy_ship_list.append(arg - 20)

            if self.first_catch == arg-10:
                if type(self.computer_vision[arg - 20]) == int:
                    self.destroy_ship_list.append(arg - 20)
                if type(self.computer_vision[arg + 10]) == int:
                    self.destroy_ship_list.append(arg + 10)
                if type(self.computer_vision[arg + 20]) == int:
                    self.destroy_ship_list.append(arg + 20)
                if type(self.computer_vision[arg - 30]) == int:
                    self.destroy_ship_list.append(arg - 30)

        if vector == 1:
            if len(str(arg)) == 1 and len(str(self.first_catch)) == 1:

                if self.first_catch == arg + 1:
                    if type(self.computer_vision[arg + 2]) and arg + 2 <= 9:
                        self.destroy_ship_list.append(arg + 2)
                    if type(self.computer_vision[arg - 1]) and arg - 1 >= 0:
                        self.destroy_ship_list.append(arg - 1)
                    if type(self.computer_vision[arg - 2]) and arg - 2 >= 0:
                        self.destroy_ship_list.append(arg - 2)
                    if type(self.computer_vision[arg + 3]) and arg + 3 >= 0:
                        self.destroy_ship_list.append(arg + 3)

                if self.first_catch == arg - 1:
                    if type(self.computer_vision[arg - 2]) and arg - 2 >= 0:
                        self.destroy_ship_list.append(arg - 2)
                    if type(self.computer_vision[arg + 1]) and arg + 1 <= 9:
                        self.destroy_ship_list.append(arg + 1)
                    if type(self.computer_vision[arg - 3]) and arg - 3 >= 0:
                        self.destroy_ship_list.append(arg - 3)
                    if type(self.computer_vision[arg + 2]) and arg + 2 >= 0:
                        self.destroy_ship_list.append(arg + 2)

            if len(str(arg)) == 2 and len(str(self.first_catch)) == 2:

                if self.first_catch == arg + 1:
                    if type(self.computer_vision[arg + 2]) and int(str(arg + 2)[1]) > 0:
                        self.destroy_ship_list.append(arg + 2)
                    if type(self.computer_vision[arg - 1]) and int(str(arg - 1)[1]) > 0:
                        self.destroy_ship_list.append(arg - 1)
                    if type(self.computer_vision[arg + 3]) and int(str(arg + 3)[1]) > 0:
                        self.destroy_ship_list.append(arg + 3)
                    if type(self.computer_vision[arg - 2]) and int(str(arg - 2)[1]) > 0:
                        self.destroy_ship_list.append(arg - 2)

                if self.first_catch == arg - 1:
                    if type(self.computer_vision[arg - 2]) and int(str(arg + 2)[1]) < 9:
                        self.destroy_ship_list.append(arg - 2)
                    if type(self.computer_vision[arg + 1]) and int(str(arg + 1)[1]) > 0:
                        self.destroy_ship_list.append(arg + 1)
                    if type(self.computer_vision[arg - 3]) and int(str(arg - 3)[1]) > 0:
                        self.destroy_ship_list.append(arg - 3)
                    if type(self.computer_vision[arg + 2]) and int(str(arg + 2)[1]) > 0:
                        self.destroy_ship_list.append(arg + 2)

    def destroy_ship(self):
        shot = self.destroy_ship_list[0]
        player_ships = self.gun.player_one_ships
        player_field = self.gun.player_one_field
        my_index = None

        print('!!!!!!!! Компьютер делает выстрел !!!!!!!!')
        try:
            if type(player_field[shot]) == int:
                print('!!!!!!!! Компьютер промахнулся !!!!!!!!')
                player_field[shot] = '.'
                self.computer_vision[shot] = '.'
                self.gun.change_order()
                for index, i in enumerate(self.destroy_ship_list):
                    if i == shot:
                        my_index = index
                self.destroy_ship_list.pop(my_index)
                self.prime = 1

            if player_field[shot] == 'X':
                print('!!!!!!!! Компьютер попал !!!!!!!!')
                index_one = 0
                index_two = 0
                for first_index, i in enumerate(player_ships):
                    if shot in i:
                        index_one = first_index
                        for second_index, j in enumerate(player_field[index_one]):
                            if shot == j:
                                index_two = second_index

                player_ships[index_one].pop(index_two)

                if len(player_ships[index_one]) > 0:
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    for index, i in enumerate(self.destroy_ship_list):
                        if i == shot:
                            my_index = index
                    self.destroy_ship_list.pop(my_index)
                    self.prime = 1
                    return True

                if len(player_ships[index_one]) == 0:
                    print('!!!!!!!! Компьютер уничтожил ваш корабль !!!!!!!!')
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    player_ships.pop(index_one)
                    self.aura_for_vision()
                    self.destroy_ship_list = []
                    self.first_catch = None
                    self.last_move = 0
                    self.prime = 0
                    return True

        except Exception:
            print('Вердос накосячил')

    def try_shot(self):
        self.list_of_shots()
        shot = choice(self.list_of_possible_shots)
        player_ships = self.gun.player_one_ships
        player_field = self.gun.player_one_field
        print('!!!!!!!! Компьютер делает выстрел !!!!!!!!')
        # time.sleep(5)
        try:
            if type(player_field[shot]) == int:
                print('!!!!!!!! Компьютер промахнулся !!!!!!!!')
                # time.sleep(5)
                player_field[shot] = '.'
                self.computer_vision[shot] = '.'
                self.gun.change_order()
                return True

            if player_field[shot] == 'X':
                print('!!!!!!!! Компьютер попал !!!!!!!!')
                # time.sleep(5)
                index_one = 0
                index_two = 0
                for first_index, i in enumerate(player_ships):
                    if shot in i:
                        index_one = first_index
                        for second_index, j in enumerate(player_ships[index_one]):
                            if shot == j:
                                index_two = second_index

                player_ships[index_one].pop(index_two)

                if len(player_ships[index_one]) > 0:
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    self.necessary_to_shot(shot)
                    self.last_move = 1
                    self.first_catch = shot
                    return True

                if len(player_ships[index_one]) == 0:
                    print('!!!!!!!! Компьютер уничтожил ваш корабль !!!!!!!!')
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    player_ships.pop(index_one)
                    self.aura_for_vision()
                    self.prime = 0
                    return True
        except Exception:
            print('Вердос накосячил')

    def making_necessary_shot(self):
        player_ships = self.gun.player_one_ships
        player_field = self.gun.player_one_field
        shot = choice(self.list_of_necessary_shots)
        my_index = None

        try:
            if type(player_field[shot]) == int:
                print('!!!!!!!! Компьютер промахнулся !!!!!!!!')
                player_field[shot] = '.'
                self.computer_vision[shot] = '.'
                self.gun.change_order()
                for index, i in enumerate(self.list_of_necessary_shots):
                    if i == shot:
                        my_index = index
                self.list_of_necessary_shots.pop(my_index)
                self.prime = 1

            if player_field[shot] == 'X':
                print('!!!!!!!! Компьютер попал !!!!!!!!')
                index_one = 0
                index_two = 0
                for first_index, i in enumerate(player_ships):
                    if shot in i:
                        index_one = first_index
                        for second_index, j in enumerate(player_field[index_one]):
                            if shot == j:
                                index_two = second_index

                player_ships[index_one].pop(index_two)

                if len(player_ships[index_one]) > 0:
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    self.list_of_necessary_shots = []
                    self.prime = 1
                    self.last_move = 1
                    self.create_focus_list(shot)

                    return True

                if len(player_ships[index_one]) == 0:
                    print('!!!!!!!! Компьютер уничтожил ваш корабль !!!!!!!!')
                    player_field[shot] = 'Y'
                    self.computer_vision[shot] = 'X'
                    player_ships.pop(index_one)
                    self.aura_for_vision()
                    self.last_move = 0
                    self.list_of_necessary_shots = []
                    self.first_catch = None
                    self.prime = 0
                    return True
        except Exception:
            print('Вердос накосячил')

    def comp_shots(self):
        print('!!!!!!!! Компьютер делает выстрел !!!!!!!!')
        time.sleep(3)
        self.prime = 0

        if len(self.destroy_ship_list) > 0:
            self.destroy_ship()
        if self.last_move == 1 and len(self.destroy_ship_list) == 0:
            self.making_necessary_shot()
        if self.last_move == 0 and self.prime == 0:
            self.try_shot()


