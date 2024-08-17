import numpy as np
import matplotlib.pyplot as plt

"""
Для Hero префлопа реализовать:
RFI(добавить для всех позиций), VPIP, 3-bet, 4-bet, PFR(любой рейз на префлопе),
ATS(отдельно с btn, co, sb), my Fold vs 3bet(мой флод)

Для Поля надо реализовать
Villain Fold vs my 3bet, Villain Fold vs my 4bet
"""


class Stats:

    def __init__(self, hand_lst):

        self.VPIP = float()
        self.RFI = float()
        self.PFR = float()
        self.ATS = dict()
        self.Fold_to_3_bet = float()
        self._3_bet = float()
        self._4_bet = float()

        self.BB_defend_count_call = dict()
        self.BB_defend_count_3bet = dict()
        self.BB_defend_opportunities = dict()

        self.hand_lst = hand_lst
        self.data_len = len(self.hand_lst)
        self.hand_dict = dict()
        self.hand_dict_open_raise = dict()
        self.hand_dict_3bet = dict()

        self.pfr_count = int()  # переменная отвечающая за кол-во раздач в которых hero играл рейзом на префлопе
        self.vpip_count = int()  # переменная отвечающая за кол-во раздач в которых hero участвовал

        self.opportunities_3bet = dict()  # переменная отвечающая за кол-во раздач в которых можно было сыграть 3-bet на префлопе
        self.count_3bet = dict()  # переменная отвечающая за кол-во раздач в которых фактически был сыгран 3-bet

        self.opportunities_4bet = dict()  # переменная отвечающая за кол-во раздач в которых можно было сыграть 4-bet на префлопе(без учета cold 4-bet'ов)
        self.count_4bet = dict()  # переменная отвечающая за кол-во раздач в которых фактически был сыгран 4-bet на префлопе(без учета cold 4-bet'ов)

        self.opportunities_open_4bet = dict()
        self.count_open_4bet = dict()

        self.rfi_count = dict()  # словарь, который ведет подсчет фактических rfi(разделяя по позициям)
        self.rfi_opportunities = dict()  # словарь, который ведет подсчет возможностей rfi(разделяя по позициям)

        # Ситуации при которых бы Hero мог бы сфолдить на 3бет, если открывался Hero(не учитывая ситуации где hero мог нажать cold 4bet)
        self.fold_to_3bet_opportunities = int()
        self.fold_to_3bet = int()

        self.fold_to_4bet_opportunities = int()
        self.fold_to_4bet = int()

        self.call_to_RFI_opportunities = dict()
        self.call_to_RFI_count = dict()

        self.call_to_3bet_opportunities = dict()
        self.call_to_3bet_count = dict()

        self.call_to_4bet_opportunities = dict()
        self.call_to_4bet_count = dict()

        self.hero_results = list()

    def result_stats(self):
        for hand in self.hand_lst:
            try:
                self.hero_results.append(hand.hero_results + self.hero_results[-1])
            except IndexError:
                self.hero_results.append(hand.hero_results)

    def result_stats_ret(self):
        return {
            "bb/100:": self.hero_results[-1]/len(self.hero_results)*100,
            "result": self.hero_results[-1]
        }

    def show_result_plot(self):
        if len(self.hero_results) != 0:
            plt.plot(self.hero_results)
            plt.show()
        else:
            print("no data")

    def pre_flop_stats(self):
        alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

        for hand in alph_lst:
            for j in alph_lst:

                if hand == j:
                    self.hand_dict_open_raise[hand + j] = [0, 0, 0]
                    self.hand_dict_3bet[hand + j] = [0, 0, 0]
                elif j + hand + "s" in self.hand_dict_open_raise.keys():
                    self.hand_dict_open_raise[j + hand + "o"] = [0, 0, 0]
                    self.hand_dict_3bet[j + hand + "o"] = [0, 0, 0]
                else:
                    self.hand_dict_open_raise[hand + j + "s"] = [0, 0, 0]
                    self.hand_dict_3bet[hand + j + "s"] = [0, 0, 0]

        for hand in self.hand_lst:
            raiser_name = str()
            open_raised = False  # булевая переменная которая проверяет был ли raise до очереди hero
            _3betted = False # показывает что в раздаче был 3бет
            hero_rfi = False # показывает что Hero открылся первым в раздаче

            card_value = sorted([hand.hero_cards[0][0], hand.hero_cards[1][0]])[::-1]  # наминалы карт, без учета мастей
            if hand.hero_cards[0][-1] == hand.hero_cards[1][-1]:
                hand = card_value[0] + card_value[1] + 's'
            elif hand.hero_cards[0][0] == hand.hero_cards[1][0]:
                hand = card_value[0] + card_value[1]
            else:
                hand = card_value[0] + card_value[1] + 'o'
            if hand not in self.hand_dict_open_raise.keys():
                hand = hand[1] + hand[0] + hand[2]

            for j in hand.preflop_action:
                # действия совершаемые Hero(тем от чьего лица игралась раздача)
                if j[0] == 'Hero':
                    if j[1][0] == "raises":

                        if hand.hero_position == "BB" and not _3betted and open_raised:
                            if hand.positions[raiser_name] not in self.BB_defend_count_3bet.keys():
                                self.BB_defend_count_3bet[hand.positions[raiser_name]] = 1
                            else:
                                self.BB_defend_count_3bet[hand.positions[raiser_name]] += 1
                            if hand.positions[raiser_name] not in self.BB_defend_opportunities.keys():
                                self.BB_defend_opportunities[hand.positions[raiser_name]] = 1
                            else:
                                self.BB_defend_opportunities[hand.positions[raiser_name]] += 1
                        self.pfr_count += 1
                        self.vpip_count += 1
                        if _3betted and hero_rfi:
                            if hand.hero_position in self.count_4bet.keys():
                                self.count_4bet[hand.hero_position] += 1
                            else:
                                self.count_4bet[hand.hero_position] = 1
                        elif open_raised:

                            self.hand_dict_3bet[hand][0] = np.round(self.hand_dict_3bet[hand][0] + hand.hero_results, 1)
                            self.hand_dict_3bet[hand][1] += 1
                            self.hand_dict_3bet[hand][2] += 1

                            if hand.hero_position in self.count_3bet.keys():
                                self.count_3bet[hand.hero_position] += 1
                            else:
                                self.count_3bet[hand.hero_position] = 1
                        else:
                            self.hand_dict_open_raise[hand][0] = np.round(self.hand_dict_open_raise[hand][0] + hand.hero_results, 1)
                            self.hand_dict_open_raise[hand][1] += 1
                            self.hand_dict_open_raise[hand][2] += 1

                            hero_rfi = True

                            if hand.hero_position in self.rfi_count.keys():
                                self.rfi_count[hand.hero_position] += 1
                            else:
                                self.rfi_count[hand.hero_position] = 1

                    elif j[1][0] == "calls":
                        self.vpip_count += 1
                        if hand.hero_position == "BB" and not _3betted and open_raised:
                            if hand.positions[raiser_name] not in self.BB_defend_count_call.keys():
                                self.BB_defend_count_call[hand.positions[raiser_name]] = 1
                            else:
                                self.BB_defend_count_call[hand.positions[raiser_name]] += 1
                            if hand.positions[raiser_name] not in self.BB_defend_opportunities.keys():
                                self.BB_defend_opportunities[hand.positions[raiser_name]] = 1
                            else:
                                self.BB_defend_opportunities[hand.positions[raiser_name]] += 1

                    elif j[1][0] == "folds":

                        if open_raised:
                            self.hand_dict_3bet[hand][0] = np.round(self.hand_dict_3bet[hand][0] + hand.hero_results, 1)
                            self.hand_dict_3bet[hand][1] += 1
                        else:
                            self.hand_dict_open_raise[hand][0] = np.round(self.hand_dict_open_raise[hand][0] + hand.hero_results, 1)
                            self.hand_dict_open_raise[hand][1] += 1

                        if hand.hero_position == "BB" and not _3betted and open_raised:
                            if hand.positions[raiser_name] not in self.BB_defend_opportunities.keys():
                                self.BB_defend_opportunities[hand.positions[raiser_name]] = 1
                            else:
                                self.BB_defend_opportunities[hand.positions[raiser_name]] += 1
                        if hero_rfi:
                            self.fold_to_3bet += 1

                    if _3betted and hero_rfi:
                        self.fold_to_3bet_opportunities += 1

                        if hand.hero_position in self.opportunities_4bet.keys():
                            self.opportunities_4bet[hand.hero_position] += 1
                        else:
                            self.opportunities_4bet[hand.hero_position] = 1
                    elif open_raised and not hero_rfi:
                        if hand.hero_position in self.opportunities_3bet.keys():
                            self.opportunities_3bet[hand.hero_position] += 1
                        else:
                            self.opportunities_3bet[hand.hero_position] = 1
                    elif not open_raised:
                        if hand.hero_position in self.rfi_opportunities.keys():
                            self.rfi_opportunities[hand.hero_position] += 1
                        else:
                            self.rfi_opportunities[hand.hero_position] = 1

                if j[1][0] == "raises":
                    if open_raised:

                        _3betted = True
                    open_raised = True
                    raiser_name = j[0]



        self.RFI = {hand: (self.rfi_count[hand] / self.rfi_opportunities[hand]) * 100 for hand in self.rfi_count.keys()}
        self.PFR = (self.pfr_count / self.data_len)*100
        self.BB_def_call = {hand: (self.BB_defend_count_call[hand] / self.BB_defend_opportunities[hand]) * 100 for hand in self.BB_defend_count_call.keys()}
        self.BB_def_3bet = {hand: (self.BB_defend_count_3bet[hand] / self.BB_defend_opportunities[hand]) * 100 for hand in self.BB_defend_count_3bet.keys()}
        self.VPIP = (self.vpip_count / self.data_len) * 100
        self._3_bet = {hand: (self.count_3bet[hand] / self.opportunities_3bet[hand]) * 100 for hand in self.count_3bet.keys()}
        self._4_bet = {hand: (self.count_4bet[hand] / self.opportunities_4bet[hand]) * self.RFI[hand] for hand in self.count_4bet.keys()}
        self.Fold_to_3_bet = (self.fold_to_3bet / self.fold_to_3bet_opportunities) * 100

    def pre_flop_stats_upd(self):

        for hand in self.hand_lst:

            """Подсчет vpip"""
            if "hero_raises" in hand.preflop_tags["Hero_action_tags"] or "hero_calls" in hand.preflop_tags["Hero_action_tags"]:
                self.vpip_count += 1

            """Подсчет pfr"""
            """добавить"""

            """Статистика бордов на которых не было лимпа"""
            if "limped" not in hand.preflop_tags["Hero_action_tags"]:

                """Ситуации с рейзом"""
                if "hero_raises" in hand.preflop_tags["Hero_action_tags"]:

                    # RFI
                    if "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.rfi_count.keys():
                            self.rfi_count[hand.hero_position] = 0
                        if hand.hero_position not in self.rfi_opportunities.keys():
                            self.rfi_opportunities[hand.hero_position] = 0

                        self.rfi_count[hand.hero_position] += 1
                        self.rfi_opportunities[hand.hero_position] += 1

                    # 3bet (переделать)
                    if "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:

                        if hand.hero_position not in self.count_3bet.keys():
                            self.count_3bet[hand.hero_position] = dict()

                        if hand.hero_position not in self.opportunities_3bet.keys():
                            self.opportunities_3bet[hand.hero_position] = dict()

                        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")

                        if f"{hand.hero_position}vs{villain_pos}" not in self.count_3bet[hand.hero_position].keys():
                            self.count_3bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0
                        if f"{hand.hero_position}vs{villain_pos}" not in self.opportunities_3bet[hand.hero_position].keys():
                            self.opportunities_3bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

                        self.count_3bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
                        self.opportunities_3bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

                    # 4bet (переделать)
                    if "hero_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.count_4bet.keys():
                            self.count_4bet[hand.hero_position] = dict()

                        if hand.hero_position not in self.opportunities_4bet.keys():
                            self.opportunities_4bet[hand.hero_position] = dict()

                        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "3bet")

                        if f"{hand.hero_position}vs{villain_pos}" not in self.count_4bet[hand.hero_position].keys():
                            self.count_4bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0
                        if f"{hand.hero_position}vs{villain_pos}" not in self.opportunities_4bet[hand.hero_position].keys():
                            self.opportunities_4bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

                        self.count_4bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
                        self.opportunities_4bet[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
                    # 4bet в холодную
                    elif "hero_4bet" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.count_open_4bet.keys():
                            self.count_open_4bet[hand.hero_position] = 0
                        if hand.hero_position not in self.opportunities_open_4bet.keys():
                            self.opportunities_open_4bet[hand.hero_position] = 0

                        self.count_open_4bet[hand.hero_position] += 1
                        self.opportunities_open_4bet[hand.hero_position] += 1
                """Ситуации с фолдом(переделать)"""
                if "hero_folds" in hand.preflop_tags["Hero_action_tags"]:
                    # rfi
                    if "hero_folds_to_No_raise" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.rfi_opportunities.keys():
                            self.rfi_opportunities[hand.hero_position] = 0

                        self.rfi_opportunities[hand.hero_position] += 1
                    # 3bet
                    elif "hero_folds_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.opportunities_3bet.keys():
                            self.opportunities_3bet[hand.hero_position] = 0

                        self.opportunities_3bet[hand.hero_position] += 1

                        if hand.hero_position not in self.call_to_RFI_opportunities.keys():
                            self.call_to_RFI_opportunities[hand.hero_position] = dict()
                        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")
                        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_RFI_opportunities[hand.hero_position].keys():
                            self.call_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0
                        self.call_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

                    elif "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" not in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.opportunities_open_4bet.keys():
                            self.opportunities_open_4bet[hand.hero_position] = 0

                        self.opportunities_open_4bet[hand.hero_position] += 1

                    elif "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.opportunities_4bet.keys():
                            self.opportunities_4bet[hand.hero_position] = 0

                        self.opportunities_4bet[hand.hero_position] += 1

                """Ситуации с колом(доделать)"""
                if "hero_calls" in hand.preflop_tags["Hero_action_tags"]:

                    if "hero_calls_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.call_to_RFI_count.keys():
                            self.call_to_RFI_count[hand.hero_position] = dict()

                        if hand.hero_position not in self.call_to_RFI_opportunities.keys():
                            self.call_to_RFI_opportunities[hand.hero_position] = dict()

                        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")

                        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_RFI_count[hand.hero_position].keys():
                            self.call_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0
                        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_RFI_opportunities[hand.hero_position].keys():
                            self.call_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

                        self.call_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
                        self.call_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

        self.RFI = {hand: (self.rfi_count[hand] / self.rfi_opportunities[hand]) * 100 for hand in self.rfi_count.keys()}
        self.PFR = (self.pfr_count / self.data_len) * 100
        self.VPIP = (self.vpip_count / self.data_len) * 100
        self._3_bet = {hand: (self.count_3bet[hand] / self.opportunities_3bet[hand]) * 100 for hand in self.count_3bet.keys()}
        self._4_bet = {hand: (self.count_4bet[hand] / self.opportunities_4bet[hand]) * self.RFI[hand] for hand in
                       self.count_4bet.keys()}


        """потестил RFI, PFR, VPIP, _3bet, _4bet в целом все работает впередалах нормы, 
        но надо бы понять почему происходят отклонения вплоть до 1% причем практически везде
        (на пфре потому что я не учитываю изолейты и на 4бетах скорее всего по той же причине, что даже наверное правиленьее,
        потому что после моего изолейта меня 3бетят уже, соответственно и я должен 4бетить уже)
        Продолжать с этого момента"""

        """переделать с 0 3бет, 4бет и тд так что б было более детально(позиция против позиции), усреднить проще чем развернуть, так что надо изначально
        рассматривать более детально"""



        """
            elif j[1][0] == "folds":

                if open_raised:
                    self.hand_dict_3bet[hand][0] = np.round(self.hand_dict_3bet[hand][0] + hand.hero_results, 1)
                    self.hand_dict_3bet[hand][1] += 1
                else:
                    self.hand_dict_open_raise[hand][0] = np.round(
                        self.hand_dict_open_raise[hand][0] + hand.hero_results, 1)
                    self.hand_dict_open_raise[hand][1] += 1

                if hand.hero_position == "BB" and not _3betted and open_raised:
                    if hand.positions[raiser_name] not in self.BB_defend_opportunities.keys():
                        self.BB_defend_opportunities[hand.positions[raiser_name]] = 1
                    else:
                        self.BB_defend_opportunities[hand.positions[raiser_name]] += 1
                if hero_rfi:
                    self.fold_to_3bet += 1

            if _3betted and hero_rfi:
                self.fold_to_3bet_situations += 1

                if hand.hero_position in self.opportunities_4bet.keys():
                    self.opportunities_4bet[hand.hero_position] += 1
                else:
                    self.opportunities_4bet[hand.hero_position] = 1
            elif open_raised and not hero_rfi:
                if hand.hero_position in self.opportunities_3bet.keys():
                    self.opportunities_3bet[hand.hero_position] += 1
                else:
                    self.opportunities_3bet[hand.hero_position] = 1
            elif not open_raised:
                if hand.hero_position in self.rfi_opportunities.keys():
                    self.rfi_opportunities[hand.hero_position] += 1
                else:
                    self.rfi_opportunities[hand.hero_position] = 1

        if j[1][0] == "raises":
            if open_raised:
                _3betted = True
            open_raised = True
            raiser_name = j[0]

        self.RFI = {hand: (self.rfi_count[hand] / self.rfi_opportunities[hand]) * 100 for hand in self.rfi_count.keys()}
        self.PFR = (self.pfr_count / self.data_len) * 100
        self.BB_def_call = {hand: (self.BB_defend_count_call[hand] / self.BB_defend_opportunities[hand]) * 100 for hand in
                            self.BB_defend_count_call.keys()}
        self.BB_def_3bet = {hand: (self.BB_defend_count_3bet[hand] / self.BB_defend_opportunities[hand]) * 100 for hand in
                            self.BB_defend_count_3bet.keys()}
        self.VPIP = (self.vpip_count / self.data_len) * 100
        self._3_bet = {hand: (self.count_3bet[hand] / self.opportunities_3bet[hand]) * 100 for hand in self.count_3bet.keys()}
        self._4_bet = {hand: (self.count_4bet[hand] / self.opportunities_4bet[hand]) * self.RFI[hand] for hand in
                       self.count_4bet.keys()}
        self.Fold_to_3_bet = (self.fold_to_3bet / self.fold_to_3bet_situations) * 100
        """

    def villain_pos(self, action_tags, villain_action):
        for j in action_tags:
            if j.split("_")[-1] == villain_action and j.split("_")[0] != "hero":
                return j.split("_")[0]
    def pre_flop_stats_ret_upd(self):
        return {
            "VPIP%": self.VPIP,
            "PFR%": self.PFR,
            "RFI%": self.RFI,
            "3-bet%": self._3_bet,
            "4-bet%": self._4_bet,
            "call_to_RFI": self.call_to_RFI_count,
            "call_to_RFI_opp": self.call_to_RFI_opportunities
            }

    def pre_flop_stats_ret(self):
        return {
            "VPIP%": self.VPIP,
            "PFR%": self.PFR,
            "RFI%": self.RFI,
            "BB_def_call%": self.BB_def_call,
            "BB_def_3bet%": self.BB_def_3bet,
            "3-bet%": self._3_bet,
            "4-bet%": self._4_bet,
            "Fold to 3-bet%": self.Fold_to_3_bet
            }

    def ret_hand_matrix_value(self):

        return [self.hand_dict_open_raise, self.hand_dict_3bet]



"""Встроить в руку префлоп теги, что б иметь возможность их сортировать"""

"""Возможные префлоп теги: No_raise_pot, Limp_pot, SRP, 3bet, 4bet, 5bet, hero_in_post_flop, hero_3bet, hero_4bet, hero_RFI,
 hero_isolate, hero_folds_to_RFI, hero_folds_to_3bet, hero_calls_to_RFI, hero_calls_to_3bet, hero_folds_to_4bet, hero_calls_to_4bet,
 hero_5bet, hero_calls_to_5bet, hero_folds_to_5bet
 (возможно в процессе я ещё что нибудь придумаю)"""

"""Пока не знаю как но переделать подсчет матрицы что б он был не такой всратый(как по мне можно сделать более оопшно), то есть
что б он два раза запускал одну функцию для разных матриц дважды, а не в одной функции считал две разные матрицы
(для этого вероятно сначала предется доделать теги и уже основываясь на них делать матрицу)"""

"""Встроить в класс Statistics класс Hands, так что б все считалось при одном проходе через базу
(что б огромную базу рук не приходилось проходить по куче раз, оптимизация хуле)"""