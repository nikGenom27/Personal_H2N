import numpy as np

"""Проверка, что введенные данные подходят для того что б их преобразовывать"""


def data_can_be_processed(inf):
    if "*** HOLE CARDS ***" not in inf:
        return False
    elif "Hand was run three times" in inf:
        return False
    else:
        return True


class Hand:
    def __init__(self, hand_info):


        """
        1st pos - btn
        2nd pos - sb
        3rd pos - bb
        4th pos - utg
        5th pos - hj
        6th pos - co
        """

        """Information"""

        self.common_inf = hand_info.split("*** HOLE CARDS ***")[0]
        self.info = hand_info.split("*** HOLE CARDS ***")[1]

        self.position_inf = [i for i in self.common_inf.split("\n")[2:] if "Seat" in i]  # Список строк с информацией о том какой игрок за каким местом(номером) сидит
        self.blind_post = [i for i in self.common_inf.split("\n")[2:] if "Seat" not in i]  # Имена игроков которые ставили блайнды и сколько они заплатили
        self.players_lst = list()
        self.btn_seat = int(self.common_inf.split('\n')[1].split()[4][-1])  # номер места btn за столом

        # vars init
        self.hero_position = str()  # информация о позиции игрока(btn, sb и тд)
        self.stack_sizes = dict()  # key: никнейм игрока, value: его размер стека
        self.limit = float()  # Сколько в одном блайнде долларов
        self.seats = dict()  # key: номер позиции(циффра), value: никнейм игрока
        self.positions = dict()  # key: никнейм игрока, value: его позиция
        self.niknames_from_positions = dict()  # key: позиция, value: никнейм игрока
        self.players_at_table = int()  # Количество игроков за столом

        self.limit = float(self.common_inf.split("/$")[1].split(")")[0])
        self.positions_define()

        """Pre-flop"""
        # vars init
        self.preflop_tags = {"pot_type": "No_action", "Hero_action_tags": [], "Position_action_tags": {}}  # список тегов на префлопе
        self.blind_post_action = list()
        self.preflop_pot_size = float()
        self.players_preflop_money_in_pot = dict()  # key: никнейм игрока, value: сколько блайндов он внес в общий банк на префлопе
        self.end_of_preflop_players_in = dict()  # key: никнейм игрока, value: True/False остался ли игрок в раздаче к концу префлопа
        self.end_of_preflop_stack_sizes = dict()  # key: никнейм игрока, value: сколько блайндов осталось у игрока в стеке к концу префлопа
        self.preflop_action = list()  # Список действий соверешенных игроками на префлопе
        self.preflop_inf = str()  # Текст содержащий информацию о префлопе(как он представлен в .txt)
        self.preflop_action_inf = list()  # Текст содержащий информацию о действиях совершенных на префлопе(как он представле в .txt)
        self.hero_cards = list()  # Информация о картах hero в формате ['Ah', 'Ac'] где первый символ это номинал, а второй масть(2 элемента 2 карты соответственно)
        self.flop_exist = True
        self.turn_exist = True
        self.river_exist = True
        self.run_it_twice = 'Hand was run two times' in hand_info
        # end of vars init

        # preflop actions
        self.preflop_act()

        """Flop"""

        # vars init
        self.flop_pot_size = float()
        self.flop_inf = str()
        self.flop_action = list()  # Список действий соверешенных игроками на флопе
        self.end_of_flop_stack_sizes = dict()  # key: никнейм игрока, value: сколько блайндов он внес в общий банк на префлопе
        self.end_of_flop_players_in = dict()  # key: никнейм игрока, value: True/False остался ли игрок в раздаче к концу префлопа
        self.players_flop_money_in_pot = dict()  # key: никнейм игрока, value: сколько блайндов осталось у игрока в стеке к концу префлопа
        self.flop_board = list()  # Карты которые выложили на флопе
        self.flop_action_inf = list()
        # end of vars init

        # flop actions
        self.flop_pot_size = self.preflop_pot_size
        self.end_of_flop_stack_sizes = self.end_of_preflop_stack_sizes.copy()
        self.end_of_flop_players_in = self.end_of_preflop_players_in.copy()
        if self.flop_exist:
            self.flop_act()

        """Turn"""

        # vars init
        self.turn_pot_size = float()
        self.turn_inf = str()
        self.turn_action = list()
        self.end_of_turn_stack_sizes = dict()  # key: никнейм игрока, value: сколько блайндов он внес в общий банк на префлопе
        self.end_of_turn_players_in = dict()  # key: никнейм игрока, value: True/False остался ли игрок в раздаче к концу префлопа
        self.players_turn_money_in_pot = dict()  # key: никнейм игрока, value: сколько блайндов осталось у игрока в стеке к концу префлопа
        self.turn_card = str()  # Карта которую выложили на терне
        self.turn_action_inf = list()
        # end of vars init

        # turn actions
        self.turn_pot_size = self.flop_pot_size
        self.end_of_turn_stack_sizes = self.end_of_flop_stack_sizes.copy()
        self.end_of_turn_players_in = self.end_of_flop_players_in.copy()
        if self.turn_exist:
            self.turn_act()

        """River"""

        # vars init
        self.river_pot_size = float()
        self.river_inf = str()
        self.river_action = list()
        self.end_of_river_stack_sizes = dict()  # key: никнейм игрока, value: сколько блайндов он внес в общий банк на префлопе
        self.end_of_river_players_in = dict()  # key: никнейм игрока, value: True/False остался ли игрок в раздаче к концу префлопа
        self.players_river_money_in_pot = dict()  # key: никнейм игрока, value: сколько блайндов осталось у игрока в стеке к концу префлопа
        self.river_card = str()  # Карта которую выложили на терне
        self.river_action_inf = list()
        # end of vars init

        # river actions
        self.river_pot_size = self.turn_pot_size
        self.end_of_river_stack_sizes = self.end_of_turn_stack_sizes.copy()
        self.end_of_river_players_in = self.end_of_turn_players_in.copy()
        if self.river_exist:
            self.river_act()

        '''Второй борд когда выкладываются два ряда карт'''
        self.first_flop = list()
        self.first_turn = str()
        self.first_river = str()
        self.second_flop = list()
        self.second_turn = str()
        self.second_river = str()

        if self.run_it_twice:
            if not self.flop_exist:
                self.first_flop = self.info.split("*** FIRST FLOP ***")[1].split("\n")[0][2:-1].split()
                self.second_flop = self.info.split("*** SECOND FLOP ***")[1].split("\n")[0][2:-1].split()
            if not self.turn_exist:
                self.first_turn = self.info.split("*** FIRST TURN ***")[1].split("\n")[0][-3:-1]
                self.second_turn = self.info.split("*** SECOND TURN ***")[1].split("\n")[0][-3:-1]
            if not self.river_exist:
                self.first_river = self.info.split("*** FIRST RIVER ***")[1].split("\n")[0][-3:-1]
                self.second_river = self.info.split("*** SECOND RIVER ***")[1].split("\n")[0][-3:-1]
        """Summary"""

        self.hero_results = float()  # Сколько блайндов в раздаче выиграл/проиграл игрок
        self.hero_wins = False  # T/F в зависимости от того победил hero или нет
        self.show_down = str()  # Текст содержащий информацию о шоудауне(как он представлен в .txt)
        self.first_show_down = str()  # Текст содержащий информацию о первом шоудауне(как он представлен в .txt)
        self.second_show_down = str()  # Текст содержащий информацию о втором шоудауне(как он представлен в .txt)
        self.sum_info = str()  # Текст содержащий информацию о summary(как он представлен в .txt)
        self.winner = dict()  # key: никнейм игрока, value: сколько блайндов он выиграл. Информация о тех кто победил в раздаче(один банк может быть разделен между несколькими участниками раздачи)
        self.collected = float()  # размер банка в блайндах который делили игроки за вычетом рейка
        self.rake = float()  # количество денег которое забирает рум в каждой раздаче

        if not self.run_it_twice:
            self.showdown()
        else:
            self.twice_showdown()

    """
    Метод, который определяет какому месту(номеру) соответвтвует какой игрок за столом
    """
    def positions_define(self):
        """
        Список используемых переменных
        self.seats
        self.stack_sizes
        self.limit
        self.players_lst
        self.players_at_table
        """

        for i in self.position_inf:
            if "Seat" in i:
                self.seats[int(i.split()[1][0])] = i.split()[2]
                self.stack_sizes[i.split()[2]] = np.round(float(i.split("($")[1].split()[0]) / self.limit, 1)
        self.players_lst = list(self.seats.values())
        self.players_at_table = len(self.seats)
        self.position_visualisation()

    """
    Метод, который распределяет позиции(sb, bb, btn и тд) в зависимости от того какое место за столом занимает btn
    """
    def position_visualisation(self):
        """
        Список используемых переменных
        self.players_at_table
        self.seats
        self.positions
        self.players_lst
        self.btn_seat
        self.hero_position
        self.positions
        """

        positions_lst = ['BTN', 'SB', 'BB', 'UTG', 'HJ', 'CO']  # Список позиций отсортированый по порядку(начиная с btn)
        seat_lst = list(self.seats.keys())  # Список номеров мест которые заняты за столом
        if self.players_at_table == 5:
            positions_lst = ['BTN', 'SB', 'BB', 'UTG', 'CO']  # данное действеи сделаноч что бы в 5 max у нас перед btn сидел CO, а не HJ

        """
        Далее цикл дает игрокам позицие такие которые игроки привыкли называть
        конкретно часть self.players_lst[(i + self.btn_seat - 1) % self.players_at_table] дает имя игрока,
        которое берется из словоря в котороя
        что б это не вызывало ошибку, а именно делит нацело(если у нас btn на 6 месте то придя по циклу в 7 автоматом 
        перенесется на 1 место и ему присвоит utg)
        """

        for i in range(self.players_at_table):
            self.positions[self.players_lst[(i + seat_lst.index(self.btn_seat)) % self.players_at_table]] = positions_lst[i]
            self.niknames_from_positions[positions_lst[i]] = self.players_lst[(i + seat_lst.index(self.btn_seat)) % self.players_at_table]

        self.hero_position = self.positions['Hero']

    """
    Метод который отвечает за все что происходит на префлопе
    """
    def preflop_act(self):

        """
        Список используемых переменных
        self.blind_post
        self.stack_sizes
        self.info
        self.flop_exist
        self.turn_exist
        self.river_exist
        self.hero_cards
        self.preflop_inf
        self.preflop_action_inf
        self.preflop_action
        self.preflop_pot_size
        self.players_preflop_money_in_pot
        self.end_of_preflop_players_in
        self.end_of_preflop_stack_sizes
        """

        """
        цикл который инициализирует словарь players_preflop_money_in_pot
        """
        for i in self.seats.values():
            self.players_preflop_money_in_pot[i] = float()
        """
        добваление поставленных блайндов в players_preflop_money_in_pot
        """
        for i in self.blind_post:
            if len(i) != 0:
                player_name = i.split()[0][:-1]
                if player_name in self.players_preflop_money_in_pot.keys():
                    if i.split()[-1] != "all-in":
                        self.players_preflop_money_in_pot[player_name] += np.round(float(i.split()[-1][1:]) / self.limit, 1)
                        self.blind_post_action.append(
                            [player_name, ['blind posts', np.round(float(i.split()[-1][1:]) / self.limit, 1)]])
                    else:
                        self.players_preflop_money_in_pot[player_name] += np.round(
                            float(i.split()[-4][1:]) / self.limit, 1)
                        self.blind_post_action.append(
                            [player_name, ['blind posts', np.round(float(i.split()[-4][1:]) / self.limit, 1)]])

        """
        подготовительное копирование стек сайзов до начала раздачи, что б далее работать уже с 
        end_of_preflop_stack_sizes, это нужно для того что б у нас была уже готовая информация какой стек был у игроков
        на каждом этапе раздаче, включая этап до ее начала.
        """
        self.end_of_preflop_stack_sizes = self.stack_sizes.copy()
        self.preflop_inf = self.info.split("*** FLOP *** ")[0]  # отделение префлоп информации от информации о всей раздачи

        """
        проверка есть ли после префлопа ещё улицы
        """
        if len(self.info.split("*** FLOP *** ")) > 1:
            self.info = self.info.split("*** FLOP *** ")[1]
        else:
            self.flop_exist = False
            self.turn_exist = False
            self.river_exist = False

        self.preflop_action_inf = self.preflop_inf.split("\n")[self.players_at_table+1:-1]  # отделение информации о действиях на префлопе
        self.hero_cards = self.preflop_inf.split('Dealt to Hero [')[1].split("]")[0].split()  # определение карт игрока

        self.end_of_preflop_players_in = {i: True for i in self.positions.keys()}

        self.preflop_action, self.players_preflop_money_in_pot, self.end_of_preflop_players_in = self.action(
            self.preflop_action_inf, self.players_preflop_money_in_pot, self.end_of_preflop_players_in, "pre-flop")

        self.preflop_action = self.blind_post_action + self.preflop_action

        """
        Подсчет стеков игроков к концу префлопа
        """
        for i in self.end_of_preflop_stack_sizes.keys():
            self.end_of_preflop_stack_sizes[i] = np.round(self.end_of_preflop_stack_sizes[i] - self.players_preflop_money_in_pot[i], 1)

        self.preflop_pot_size = sum(self.players_preflop_money_in_pot.values())
        self.preflop_pot_size = np.round(self.preflop_pot_size, 1)

    """
    Метод который отвечает за все что происходит на флопе
    """
    def flop_act(self):
        """
        Список используемых переменных
        self.flop_inf
        self.info
        self.turn_exist
        self.river_exist
        self.seats
        self.flop_board
        self.players_flop_money_in_pot
        self.flop_action_inf
        self.flop_action
        self.end_of_flop_players_in
        self.end_of_flop_stack_sizes
        self.flop_pot_size
        """

        """Проверка существуют ли еще улицы"""
        self.flop_inf = self.info.split("*** TURN *** ")[0]
        if "*** TURN *** " in self.info:
            self.info = self.info.split("*** TURN *** ")[1]
        else:
            self.turn_exist = False
            self.river_exist = False

        """
        цикл который инициализирует словарь players_flop_money_in_pot
        """
        for i in self.seats.values():
            self.players_flop_money_in_pot[i] = float()

        """
        Определние того какие карты вышли на флопе
        """
        self.flop_board = self.flop_inf.split("\n")[0][1:-1].split()
        """
        Представление информации о действиях на флопе в виде списка
        Каждый элемент представляет собой строку в которой написано, какое действие и кем было совершено
        """
        self.flop_action_inf = self.flop_inf.split("\n")[1:-1]

        self.flop_action, self.players_flop_money_in_pot,  self.end_of_flop_players_in = self.action(
            self.flop_action_inf, self.players_flop_money_in_pot, self.end_of_flop_players_in, "flop")

        """
        Подсчет стеков игроков к концу флопа
        """
        for i in self.end_of_flop_stack_sizes.keys():
            self.end_of_flop_stack_sizes[i] = np.round(
                self.end_of_flop_stack_sizes[i] - self.players_flop_money_in_pot[i], 1)

        self.flop_pot_size += sum(self.players_flop_money_in_pot.values())
        self.flop_pot_size = np.round(self.flop_pot_size, 1)

    """
    Метод который отвечает за все что происходит на терне
    """
    def turn_act(self):
        """
        Список используемых переменных
        self.turn_inf
        self.info
        self.river_exist
        self.seats
        self.turn_card
        self.players_turn_money_in_pot
        self.turn_action_inf
        self.turn_action
        self.end_of_turn_players_in
        self.end_of_turn_stack_sizes
        self.turn_pot_size
        """

        """Проверка существуют ли еще улицы"""
        self.turn_inf = self.info.split("*** RIVER *** ")[0]
        if "*** RIVER *** " in self.info:
            self.info = self.info.split("*** RIVER *** ")[1]
        else:
            self.river_exist = False

        """
        цикл который инициализирует словарь players_turn_money_in_pot
        """
        for i in self.seats.values():
            self.players_turn_money_in_pot[i] = float()
        self.turn_card = self.turn_inf.split("\n")[0][-3:-1]
        self.turn_action_inf = self.turn_inf.split("\n")[1:-1]

        self.turn_action, self.players_turn_money_in_pot, self.end_of_turn_players_in = self.action(
            self.turn_action_inf, self.players_turn_money_in_pot, self.end_of_turn_players_in, "turn")

        """
        Подсчет стеков игроков к концу терна
        """
        for i in self.end_of_turn_stack_sizes.keys():
            self.end_of_turn_stack_sizes[i] = np.round(
                self.end_of_turn_stack_sizes[i] - self.players_turn_money_in_pot[i], 1)

        self.turn_pot_size += sum(self.players_turn_money_in_pot.values())
        self.turn_pot_size = np.round(self.turn_pot_size, 1)

    """
    Метод который отвечает за все что происходит на ривере
    """
    def river_act(self):
        """
        Список используемых переменных
        self.river_inf
        self.info
        self.seats
        self.river_card
        self.players_river_money_in_pot
        self.river_action_inf
        self.river_action
        self.end_of_river_players_in
        self.end_of_river_stack_sizes
        self.river_pot_size
        """
        self.river_inf = self.info.split("*** SHOWDOWN ***")[0]

        """
        цикл который инициализирует словарь players_river_money_in_pot
        """
        for i in self.seats.values():
            self.players_river_money_in_pot[i] = float()

        self.river_card = self.river_inf.split("\n")[0][-3:-1]
        self.river_action_inf = self.river_inf.split("\n")[1:-1]

        self.river_action, self.players_river_money_in_pot, self.end_of_river_players_in = self.action(
            self.river_action_inf, self.players_river_money_in_pot, self.end_of_river_players_in, "river")

        """
        Подсчет стеков игроков к концу ривера
        """
        for i in self.end_of_river_stack_sizes.keys():
            self.end_of_river_stack_sizes[i] = np.round(
                self.end_of_river_stack_sizes[i] - self.players_river_money_in_pot[i], 1)

        self.river_pot_size += sum(self.players_river_money_in_pot.values())
        self.river_pot_size = np.round(self.river_pot_size, 1)

    """
    Метод структурирующий действия игроков на флопе, подсчет блайндов 
    внесенных в общий банк на флопе каждым отдельным игроком
    и определение оставшихся в раздаче игроков после флопа
    """
    def action(self, action_inf, money_in_pot, end_of_street_players_in, street):
        """
        Список используемых переменных
        action_inf
        money_in_pot
        end_of_street_players_in
        street
        street_action_lst
        mon_in_pot
        end_of_street_pl_in
        player_info
        action
        """

        street_action_lst = list()
        mon_in_pot = money_in_pot.copy()  # Инициализируем переменную, которую будем обрабатываеть и в конце вернем
        end_of_street_pl_in = end_of_street_players_in.copy()  # Инициализируем переменную, которую будем обрабатываеть и в конце вернем

        """
        Цикл который проходит по списку строк с информацией о действиях игроков на префлопе/флопе/терне/ривере
        """
        for string in action_inf:
            player_info = list()  # Список состоящий из имени игрока и того какое он действие совершил
            act = string.split(": ")  # Промежуточная переменная во имя оптимихации
            player_info.append(act[0])

            """
            Первичная обработка действия которое было совершено. Обычно в текстовом документе все действия записнаны по шаблону:
            *Имя игрока*: *совершенное действие* *количество вложенных денег(если нужно)*
            Однако Uncalled bet не следует данному правилу и выглядит:
            Uncalled bet (*Количество денег*) returned to Hero
            """
            if len(act) > 1:
                action = act[1].split()
            else:
                """
                Этот иф нужен тк в списке строк есть ещё и пустая строка(последняя)
                Это нужно будет когда нибудь переделать что б было красиво и функционально, но пока что это работает и так
                """
                if "Uncalled bet" in string:
                    act = string.split()
                    player_info = act[-1]
                    mon_in_pot[player_info] -= np.round(float(act[2][2:-1]) / self.limit, 1)
                    action = ['Returned uncalled bet', np.round(float(act[2][2:-1]) / self.limit, 1)]
                    street_action_lst.append([player_info, action])
                """
                Uncalled bet это всегда последняя запись в списке с записями, поэтому после нее можно прописать остановку цикла
                """
                break

            """
            Преобразовании действия из текстового в формат списка:
            [*действие*,  *сколько денег в него было вложено(если необходимо)*]
            """
            if action[0] == "raises":
                action = [action[0], np.round(float(action[3][1:]) / self.limit, 1)]
                mon_in_pot[player_info[0]] = action[1]
            elif action[0] == "calls":
                action = [action[0], np.round(float(action[1][1:]) / self.limit, 1)]
                mon_in_pot[player_info[0]] += action[1]
            elif action[0] == "bets":
                action = [action[0], np.round(float(action[1][1:]) / self.limit, 1)]
                mon_in_pot[player_info[0]] = action[1]
            elif action[0] == "shows":
                action = ' '.join(action)
                action = action.split('(')[0].split()
                if len(action) == 3:
                    action = [action[0], [action[1][1:3], action[2][-3:-1]]]
                else:
                    action = [action[0], [action[1][1:3]]]
            elif action[0] == "folds":
                end_of_street_pl_in[player_info[0]] = False
            """
            Добавление действия в список со всеми действиями на данной улице в формате
            [*Имя игрока*, [*действие*,  *сколько денег в него было вложено*(если необходимо)]]
            """
            player_info.append(action)
            street_action_lst.append(player_info)

            """Вызов метода определения тегов для раздачи"""
            self.tag_addition(street, player_info)

        return street_action_lst, mon_in_pot, end_of_street_pl_in

    def tag_addition(self, street, player_info):
        if street == "pre-flop":
            pot_type_tags = {"Limped": ["No_action", "Limp", "Isolate", "3bet", "4bet", "5bet"],
                             "Raised": ["No_action", "SRP", "3bet", "4bet", "5bet"]}
            if player_info[1][0] == "raises":
                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "No_action":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_NoAction")
                    elif self.preflop_tags["pot_type"] == "Limp":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_Limp")
                    elif self.preflop_tags["pot_type"] == "Isolate":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_Isolate")
                    elif self.preflop_tags["pot_type"] == "SRP":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_RFI")
                    elif self.preflop_tags["pot_type"] == "3bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_3bet")
                    elif self.preflop_tags["pot_type"] == "4bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_4bet")

                if "Limp" in self.preflop_tags["Position_action_tags"] and self.preflop_tags["pot_type"] != pot_type_tags["Limped"][-1]:
                    self.preflop_tags["pot_type"] = pot_type_tags["Limped"][pot_type_tags["Limped"].index(self.preflop_tags["pot_type"]) + 1]
                elif self.preflop_tags["pot_type"] != pot_type_tags["Raised"][-1]:
                    self.preflop_tags["pot_type"] = pot_type_tags["Raised"][pot_type_tags["Raised"].index(self.preflop_tags["pot_type"]) + 1]

                if self.preflop_tags["pot_type"] == "SRP":
                    if "Limp" not in self.preflop_tags["Position_action_tags"].keys():
                        self.preflop_tags["Position_action_tags"]["RFI"] = self.positions[player_info[0]]
                    else:
                        self.preflop_tags["Position_action_tags"]["Isolate"] = self.positions[player_info[0]]
                else:
                    self.preflop_tags["Position_action_tags"][self.preflop_tags["pot_type"]] = self.positions[player_info[0]]

            elif player_info[1][0] == "calls":
                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "No_action":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_NoAction")
                    elif self.preflop_tags["pot_type"] == "Limp":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_Limp")
                    elif self.preflop_tags["pot_type"] == "Isolate":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_Isolate")
                    elif self.preflop_tags["pot_type"] == "SRP":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_RFI")
                    elif self.preflop_tags["pot_type"] == "3bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_3bet")
                    elif self.preflop_tags["pot_type"] == "4bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_4bet")
                    elif self.preflop_tags["pot_type"] == "5bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_5bet")

                if self.preflop_tags["pot_type"] == "No_action":
                    self.preflop_tags["pot_type"] = pot_type_tags["Limped"][
                        pot_type_tags["Limped"].index(self.preflop_tags["pot_type"]) + 1]
                    self.preflop_tags["Position_action_tags"]["Limp"] = self.positions[player_info[0]]

            elif player_info[1][0] == "folds":
                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "No_action":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_NoAction")
                    elif self.preflop_tags["pot_type"] == "Limp":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_Limp")
                    elif self.preflop_tags["pot_type"] == "Isolate":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_Isolate")
                    elif self.preflop_tags["pot_type"] == "SRP":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_RFI")
                    elif self.preflop_tags["pot_type"] == "3bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_3bet")
                    elif self.preflop_tags["pot_type"] == "4bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_4bet")
                    elif self.preflop_tags["pot_type"] == "5bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_5bet")

    def showdown(self):
        self.info = self.info.split("*** SHOWDOWN ***")[1]
        self.show_down = self.info.split("*** SUMMARY ***")[0]
        self.sum_info = self.info.split("*** SUMMARY ***")[1].split("\n")[1]
        for i in self.show_down.split("\n"):
            if len(i) != 0:
                name = i.split()[0]
                if name in self.winner.keys():
                    self.winner[name] += np.round(float(i.split()[2][1:]) / self.limit, 1)
                else:
                    self.winner[name] = np.round(float(i.split()[2][1:]) / self.limit, 1)
        self.rake = np.round(float(self.sum_info.split(" | ")[1].split("$")[1]) / self.limit + float(
            self.sum_info.split(" | ")[2].split("$")[1]) / self.limit, 1)
        self.collected = np.round(self.river_pot_size - self.rake, 1)
        if "Hero" in self.winner.keys():
            self.hero_wins = True
            self.hero_results = np.round(self.winner["Hero"] + self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)
        else:
            self.hero_results = np.round(self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)

    def twice_showdown(self):
        self.info = self.info.split("*** FIRST SHOWDOWN ***")[1]
        self.first_show_down = self.info.split("*** SECOND SHOWDOWN ***")[0]
        self.second_show_down = self.info.split("*** SECOND SHOWDOWN ***")[1].split("*** SUMMARY ***")[0]
        self.sum_info = self.info.split("*** SUMMARY ***")[1].split("\n")[1]
        for i in self.first_show_down.split("\n"):
            if len(i) != 0:
                name = i.split()[0]
                if name in self.winner.keys():
                    self.winner[name] += np.round(float(i.split()[2][1:]) / self.limit, 1)
                else:
                    self.winner[name] = np.round(float(i.split()[2][1:]) / self.limit, 1)
        for i in self.second_show_down.split("\n"):
            if len(i) != 0:
                name = i.split()[0]
                if name in self.winner.keys():
                    self.winner[name] += np.round(float(i.split()[2][1:]) / self.limit, 1)
                elif len(i) != 0:
                    self.winner[name] = np.round(float(i.split()[2][1:]) / self.limit, 1)

        self.rake = np.round(float(self.sum_info.split(" | ")[1].split("$")[1]) / self.limit + float(
            self.sum_info.split(" | ")[2].split("$")[1]) / self.limit, 1)
        self.collected = np.round(self.river_pot_size - self.rake, 1)
        if "Hero" in self.winner.keys():
            self.hero_wins = True
            self.hero_results = np.round(self.winner["Hero"] + self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)
        else:
            self.hero_results = np.round(self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)

    def __repr__(self):
        return self.hero_results

    def __str__(self):
        return str(self.hero_results)
