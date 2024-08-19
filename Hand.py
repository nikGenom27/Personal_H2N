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

        self.position_inf = [i for i in self.common_inf.split("\n")[2:] if "Seat" in i]
        self.blind_post = [i for i in self.common_inf.split("\n")[2:] if "Seat" not in i]
        self.players_lst = list()
        self.btn_position = int(self.common_inf.split('\n')[1].split()[4][-1])

        # vars init
        self.hero_position = str()
        self.stack_sizes = dict()
        self.limit = float()
        self.seats = dict()
        self.positions = dict()
        self.players_at_table = int()  # Количество игроков за столом

        self.limit = float(self.common_inf.split("/$")[1].split(")")[0])
        self.positions_define()

        """Pre-flop"""
        # vars init
        self.preflop_tags = {"pot_type": "No_raise_pot", "Hero_action_tags": [], "Position_action_tags": {}}
        self.preflop_pot_size = float()
        self.players_preflop_money_in_pot = dict()
        self.end_of_preflop_players_in = dict()
        self.end_of_preflop_stack_sizes = dict()
        self.preflop_action = list()
        self.preflop_inf = str()
        self.preflop_action_inf = list()
        self.hero_cards = list()
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
        self.flop_action = list()
        self.end_of_flop_stack_sizes = dict()
        self.end_of_flop_players_in = dict()
        self.players_flop_money_in_pot = dict()
        self.flop_board = list()
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
        self.end_of_turn_stack_sizes = dict()
        self.end_of_turn_players_in = dict()
        self.players_turn_money_in_pot = dict()
        self.turn_card = str()
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
        self.end_of_river_stack_sizes = dict()
        self.end_of_river_players_in = dict()
        self.players_river_money_in_pot = dict()
        self.river_card = str()
        self.river_action_inf = list()
        # end of vars init

        # river actions
        self.river_pot_size = self.turn_pot_size
        self.end_of_river_stack_sizes = self.end_of_turn_stack_sizes.copy()
        self.end_of_river_players_in = self.end_of_turn_players_in.copy()
        if self.river_exist:
            self.river_act()


        '''Учет борда когда крутится 2 раза'''
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

        self.hero_results = float()
        self.hero_wins = False  # T/F в зависимости от того победил hero или нет
        self.hero_results_1 = float()
        self.hero_wins_first = False
        self.hero_results_2 = float()
        self.hero_wins_second = False
        self.show_down = str()
        self.first_show_down = str()
        self.second_show_down = str()
        self.sum_info = str()
        self.winner = dict()
        self.collected = float()
        self.collected_right = float()
        self.rake = float()
        self.prize = float()

        if not self.run_it_twice:
            self.showdown()
        else:
            self.twice_showdown()

    def positions_define(self):
        for i in self.position_inf:
            if "Seat" in i:
                self.seats[int(i.split()[1][0])] = i.split()[2]
                self.stack_sizes[i.split()[2]] = np.round(float(i.split("($")[1].split()[0]) / self.limit, 1)
        self.players_lst = list(self.seats.values())
        self.players_at_table = len(self.seats)
        self.position_visualisation()

    def position_visualisation(self):
        positions_lst = ['BTN', 'SB', 'BB', 'UTG', 'HJ', 'CO']
        seat_lst = list(self.seats.keys())
        if self.players_at_table == 5:
            positions_lst = ['BTN', 'SB', 'BB', 'UTG', 'CO']  # данное действие сделано что бы в 5 max у нас перед btn сидел CO, а не HJ
        for i in range(self.players_at_table):
            self.positions[self.players_lst[(i + seat_lst.index(self.btn_position)) % self.players_at_table]] = positions_lst[i]
            '''Предыдущая строка дает игрокам позицие такие которые покеристы привыкли называть
            конкретно часть [(i + self.btn_position - 1) % self.players_at_table] дает индекс в списке с игроками так,
            что б это не вызывало ошибку, а именно делит нацела(если у нас btn на 6 месте то придя по циклу в 7 автоматом 
            перенесется на 1 место и ему присвоит utg)'''
        self.hero_position = self.positions['Hero']

    def preflop_act(self):

        for i in self.seats.values():
            self.players_preflop_money_in_pot[i] = float()

        poses = sorted(self.seats.keys())
        sb = poses[(poses.index(self.btn_position) + 1) % self.players_at_table]
        bb = poses[(poses.index(self.btn_position) + 2) % self.players_at_table]
        # в предыдущих строках делим с остатком что бы избежать ошибок если играем хедзап

        for i in self.blind_post:
            if len(i) != 0:
                if i.split()[-1] != "all-in":
                    self.players_preflop_money_in_pot[i.split()[0][:-1]] += np.round(float(i.split()[-1][1:]) / self.limit, 1)
                else:
                    self.players_preflop_money_in_pot[i.split()[0][:-1]] += np.round(
                        float(i.split()[-4][1:]) / self.limit, 1)

        self.end_of_preflop_stack_sizes = self.stack_sizes.copy()
        self.preflop_inf = self.info.split("*** FLOP *** ")[0]
        try:
            self.info = self.info.split("*** FLOP *** ")[1]
        except IndexError:
            self.flop_exist = False
            self.turn_exist = False
            self.river_exist = False
        self.preflop_action_inf = self.preflop_inf.split("\n")[self.players_at_table+1:-1]
        self.hero_cards = self.preflop_inf.split('Dealt to Hero [')[1].split("]")[0].split()

        self.preflop_action, self.players_preflop_money_in_pot, self.end_of_preflop_players_in = self.action(
            self.preflop_action_inf, self.players_preflop_money_in_pot, self.end_of_preflop_players_in, "pre-flop")

        for i in self.end_of_preflop_stack_sizes.keys():
            self.end_of_preflop_stack_sizes[i] = np.round(self.end_of_preflop_stack_sizes[i] - self.players_preflop_money_in_pot[i], 1)

        self.preflop_pot_size = sum(self.players_preflop_money_in_pot.values())

    def flop_act(self):
        self.flop_inf = self.info.split("*** TURN *** ")[0]
        try:
            self.info = self.info.split("*** TURN *** ")[1]
        except IndexError:
            self.turn_exist = False
            self.river_exist = False

        for i in self.seats.values():
            self.players_flop_money_in_pot[i] = float()

        self.flop_board = self.flop_inf.split("\n")[0][1:-1].split()
        self.flop_action_inf = self.flop_inf.split("\n")[1:-1]

        self.flop_action, self.players_flop_money_in_pot,  self.end_of_flop_players_in = self.action(
            self.flop_action_inf, self.players_flop_money_in_pot, self.end_of_flop_players_in, "flop")

        for i in self.end_of_flop_stack_sizes.keys():
            self.end_of_flop_stack_sizes[i] = np.round(
                self.end_of_flop_stack_sizes[i] - self.players_flop_money_in_pot[i], 1)

        self.flop_pot_size += sum(self.players_flop_money_in_pot.values())

    def turn_act(self):
        self.turn_inf = self.info.split("*** RIVER *** ")[0]
        try:
            self.info = self.info.split("*** RIVER *** ")[1]
        except IndexError:
            self.river_exist = False

        for i in self.seats.values():
            self.players_turn_money_in_pot[i] = float()
        self.turn_card = self.turn_inf.split("\n")[0][-3:-1]
        self.turn_action_inf = self.turn_inf.split("\n")[1:-1]

        self.turn_action, self.players_turn_money_in_pot, self.end_of_turn_players_in = self.action(
            self.turn_action_inf, self.players_turn_money_in_pot, self.end_of_turn_players_in, "turn")

        for i in self.end_of_turn_stack_sizes.keys():
            self.end_of_turn_stack_sizes[i] = np.round(
                self.end_of_turn_stack_sizes[i] - self.players_turn_money_in_pot[i], 1)

        self.turn_pot_size += sum(self.players_turn_money_in_pot.values())

    def river_act(self):
        self.river_inf = self.info.split("*** SHOWDOWN ***")[0]
        for i in self.seats.values():
            self.players_river_money_in_pot[i] = float()

        self.river_card = self.river_inf.split("\n")[0][-3:-1]
        self.river_action_inf = self.river_inf.split("\n")[1:-1]

        self.river_action, self.players_river_money_in_pot, self.end_of_river_players_in = self.action(
            self.river_action_inf, self.players_river_money_in_pot, self.end_of_river_players_in, "river")

        for i in self.end_of_river_stack_sizes.keys():
            self.end_of_river_stack_sizes[i] = np.round(
                self.end_of_river_stack_sizes[i] - self.players_river_money_in_pot[i], 1)

        self.river_pot_size += sum(self.players_river_money_in_pot.values())
        self.river_pot_size = np.round(self.river_pot_size, 1)

    def action(self, action_inf, money_in_pot, end_of_street_players_in, street):
        street_action_lst = list()
        mon_in_pot = money_in_pot.copy()
        end_of_street_pl_in = end_of_street_players_in.copy()
        for i in action_inf:
            player_info = list()
            player_info.append(i.split(": ")[0])
            try:
                action = i.split(": ")[1].split()
            except IndexError:

                if "Uncalled bet" in i:
                    player_info = i.split()[-1]
                    mon_in_pot[player_info] -= np.round(float(i.split()[2][2:-1]) / self.limit, 1)
                    action = ['Returned uncalled bet', np.round(float(i.split()[2][2:-1]) / self.limit, 1)]
                    street_action_lst.append([player_info, action])
                break
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
                try:
                    action = [action[0], [action[1][1:], action[2][:-1]]]
                except IndexError:
                    action = [action[0], [action[1][1:]]]
            elif action[0] == "folds":
                end_of_street_pl_in[player_info[0]] = False
            player_info.append(action)
            street_action_lst.append(player_info)

            self.tag_addition(street, player_info)

        return street_action_lst, mon_in_pot, end_of_street_pl_in

    def tag_addition(self, street, player_info):
        if street == "pre-flop":
            pot_type_tags = ["Limp_pot", "SRP", "3bet", "4bet", "5bet"]
            if player_info[1][0] == "raises":
                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "Limp_pot":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_Limp")
                    elif self.preflop_tags["pot_type"] == "No_raise_pot":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises")
                    elif self.preflop_tags["pot_type"] == "SRP":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_RFI")
                    elif self.preflop_tags["pot_type"] == "3bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_3bet")
                    elif self.preflop_tags["pot_type"] == "4bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_raises_against_4bet")
                try:
                    self.preflop_tags["pot_type"] = pot_type_tags[pot_type_tags.index(self.preflop_tags["pot_type"]) + 1]
                except (IndexError, ValueError):
                    if self.preflop_tags["pot_type"] == "No_raise_pot":
                        self.preflop_tags["pot_type"] = "SRP"
                if self.preflop_tags["pot_type"] == "SRP":
                    self.preflop_tags["Position_action_tags"]["RFI"] = self.positions[player_info[0]]
                else:
                    self.preflop_tags["Position_action_tags"][self.preflop_tags["pot_type"]] = self.positions[player_info[0]]
            elif player_info[1][0] == "calls":
                if self.preflop_tags["pot_type"] == "No_raise_pot":
                    self.preflop_tags["pot_type"] = "Limp_pot"
                    self.preflop_tags["Position_action_tags"]["Limp"] = self.positions[player_info[0]]

                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "No_raise_pot" or self.preflop_tags["pot_type"] == "Limp_pot":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls")
                    elif self.preflop_tags["pot_type"] == "SRP":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_RFI")
                    elif self.preflop_tags["pot_type"] == "3bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_3bet")
                    elif self.preflop_tags["pot_type"] == "4bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_4bet")
                    elif self.preflop_tags["pot_type"] == "5bet":
                        self.preflop_tags["Hero_action_tags"].append("hero_calls_against_5bet")
            elif player_info[1][0] == "folds":
                if player_info[0] == "Hero":
                    if self.preflop_tags["pot_type"] == "Limp_pot":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds_against_Limp")
                    elif self.preflop_tags["pot_type"] == "No_raise_pot":
                        self.preflop_tags["Hero_action_tags"].append("hero_folds")
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
        self.collected_right = np.round(sum(self.winner.values()), 1)
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
        self.collected_right = np.round(sum(self.winner.values()), 1)
        if "Hero" in self.winner.keys():
            self.hero_wins = True
            self.hero_results = np.round(self.winner["Hero"] + self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)
        else:
            self.hero_results = np.round(self.end_of_river_stack_sizes["Hero"] - self.stack_sizes["Hero"], 1)


"""SPR пот это все таки не изолейт пот, так что надо сделать отделный тег для борда когда чел залимпил(upd: 
это тег limped я просто немного забыл что он существует), 
и соответственно сделать отдельные теги для лимпованых бордов: 3bet на изол, кол на изол, + надо добавить не только
теги для хиро, но и для оппов, по карайней мере в хедзап ситуациях
"""