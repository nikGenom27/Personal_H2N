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

        self.hand_lst = hand_lst
        self.data_len = len(self.hand_lst)

        self.VPIP = float()
        self.RFI = float()
        self.PFR = float()

        self.pfr_count = int()  # переменная отвечающая за кол-во раздач в которых hero играл рейзом на префлопе
        self.vpip_count = int()  # переменная отвечающая за кол-во раздач в которых hero участвовал

        self.rfi_count = dict()  # словарь, который ведет подсчет фактических rfi(разделяя по позициям)
        self.rfi_opportunities = dict()  # словарь, который ведет подсчет возможностей rfi(разделяя по позициям)

        # Список действий после RFI(call, 3bet)
        self.action_to_RFI_opportunities = dict()  # переменная отвечающая за кол-во раздач в которых можно было совершить действие после чьего-то RFI
        self._3bet_to_RFI_count = dict()
        self.call_to_RFI_count = dict()  # переменная отвечающая за кол-во раздач в которых фактически был сыгран 3-bet

        # Списиок действий после 3bet(call, 4bet)
        self.action_to_3bet_opportunities = dict()  # переменная отвечающая за кол-во раздач в которых можно было совершить действие после чьего-то 3bet
        self._4bet_to_3bet_count = dict()
        self.call_to_3bet_count = dict()  # переменная отвечающая за кол-во раздач в которых фактически был сыгран 3-bet

        # Возможность за 4бетить в холодную(тк рейнджи 4бета в холодную максимально заужены и со всех пощ +- одинаковые можно не дробить)
        self.opportunities_open_4bet = dict()
        self.count_open_4bet = dict()

        # Списиок действий после 4bet(call, 4bet)
        self.action_to_4bet_opportunities = dict()  # переменная отвечающая за кол-во раздач в которых можно было совершить действие после чьего-то 3bet
        self._5bet_to_4bet_count = dict()
        self.call_to_4bet_count = dict()  # переменная отвечающая за кол-во раздач в которых фактически был сыгран 3-bet

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

    def pre_flop_stats_upd(self):

        for hand in self.hand_lst:

            """Подсчет vpip"""
            if "hero_raises" in hand.preflop_tags["Hero_action_tags"] or "hero_calls" in hand.preflop_tags["Hero_action_tags"]:
                self.vpip_count += 1

            """Подсчет pfr"""
            """добавить"""

            """Статистика бордов на которых не было лимпа"""
            if "limped" not in hand.preflop_tags["Hero_action_tags"]:


                if "hero_raises" in hand.preflop_tags["Hero_action_tags"]:

                    if "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.rfi_count.keys():
                            self.rfi_count[hand.hero_position] = 0
                        if hand.hero_position not in self.rfi_opportunities.keys():
                            self.rfi_opportunities[hand.hero_position] = 0

                        self.rfi_count[hand.hero_position] += 1
                        self.rfi_opportunities[hand.hero_position] += 1

                    if "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:

                        self.action_to_rfi_opportunities_add(hand)
                        self._3bet_to_rfi_count_add(hand)

                    if "hero_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_3bet_opportunities_add(hand)
                        self._4bet_to_3bet_count_add(hand)

                    elif "hero_4bet" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.count_open_4bet.keys():
                            self.count_open_4bet[hand.hero_position] = 0
                        if hand.hero_position not in self.opportunities_open_4bet.keys():
                            self.opportunities_open_4bet[hand.hero_position] = 0

                        self.count_open_4bet[hand.hero_position] += 1
                        self.opportunities_open_4bet[hand.hero_position] += 1

                    if "hero_5bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_4bet_opportunities_add(hand)
                        self._5bet_to_4bet_count_add(hand)

                if "hero_folds" in hand.preflop_tags["Hero_action_tags"]:

                    if "hero_folds_to_No_raise" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.rfi_opportunities.keys():
                            self.rfi_opportunities[hand.hero_position] = 0

                        self.rfi_opportunities[hand.hero_position] += 1

                    if "hero_folds_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_rfi_opportunities_add(hand)

                    if "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_3bet_opportunities_add(hand)

                    elif "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.opportunities_open_4bet.keys():
                            self.opportunities_open_4bet[hand.hero_position] = 0

                        self.opportunities_open_4bet[hand.hero_position] += 1

                    if "hero_folds_to_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_4bet_opportunities_add(hand)

                if "hero_calls" in hand.preflop_tags["Hero_action_tags"]:

                    if "hero_calls_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_rfi_opportunities_add(hand)
                        self.call_to_rfi_count_add(hand)

                    if "hero_calls_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_3bet_opportunities_add(hand)
                        self.call_to_3bet_count_add(hand)

                    elif "hero_calls_to_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        if hand.hero_position not in self.opportunities_open_4bet.keys():
                            self.opportunities_open_4bet[hand.hero_position] = 0

                        self.opportunities_open_4bet[hand.hero_position] += 1

                    if "hero_calls_to_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.action_to_4bet_opportunities_add(hand)
                        self.call_to_4bet_count_add(hand)

    """
    по идее это все, что идет ниже можно переделать так что б это была одна функция
    (например сделать из нескольких словарей один, и уже все эти словари в него запихнуть), но вот вопрос надо ли?
    по идее читаемость кода упадет хотя хз, над этим ещё надо подумать
    """
    def action_to_rfi_opportunities_add(self, hand):
        if hand.hero_position not in self.action_to_RFI_opportunities.keys():
            self.action_to_RFI_opportunities[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")

        if f"{hand.hero_position}vs{villain_pos}" not in self.action_to_RFI_opportunities[hand.hero_position].keys():
            self.action_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.action_to_RFI_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
    
    def _3bet_to_rfi_count_add(self, hand):
        if hand.hero_position not in self._3bet_to_RFI_count.keys():
            self._3bet_to_RFI_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")

        if f"{hand.hero_position}vs{villain_pos}" not in self._3bet_to_RFI_count[hand.hero_position].keys():
            self._3bet_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0
            
        self._3bet_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1
        
    def call_to_rfi_count_add(self, hand):
        if hand.hero_position not in self.call_to_RFI_count.keys():
            self.call_to_RFI_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "RFI")

        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_RFI_count[hand.hero_position].keys():
            self.call_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.call_to_RFI_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def action_to_3bet_opportunities_add(self, hand):
        if hand.hero_position not in self.action_to_3bet_opportunities.keys():
            self.action_to_3bet_opportunities[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "3bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self.action_to_3bet_opportunities[hand.hero_position].keys():
            self.action_to_3bet_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.action_to_3bet_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def _4bet_to_3bet_count_add(self, hand):
        if hand.hero_position not in self._4bet_to_3bet_count.keys():
            self._4bet_to_3bet_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "3bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self._4bet_to_3bet_count[hand.hero_position].keys():
            self._4bet_to_3bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self._4bet_to_3bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def call_to_3bet_count_add(self, hand):
        if hand.hero_position not in self.call_to_3bet_count.keys():
            self.call_to_3bet_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "3bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_3bet_count[hand.hero_position].keys():
            self.call_to_3bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.call_to_3bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def action_to_4bet_opportunities_add(self, hand):
        if hand.hero_position not in self.action_to_4bet_opportunities.keys():
            self.action_to_4bet_opportunities[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "4bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self.action_to_4bet_opportunities[hand.hero_position].keys():
            self.action_to_4bet_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.action_to_4bet_opportunities[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def _5bet_to_4bet_count_add(self, hand):
        if hand.hero_position not in self._5bet_to_4bet_count.keys():
            self._5bet_to_4bet_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "4bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self._5bet_to_4bet_count[hand.hero_position].keys():
            self._5bet_to_4bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self._5bet_to_4bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def call_to_4bet_count_add(self, hand):
        if hand.hero_position not in self.call_to_4bet_count.keys():
            self.call_to_4bet_count[hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], "4bet")

        if f"{hand.hero_position}vs{villain_pos}" not in self.call_to_4bet_count[hand.hero_position].keys():
            self.call_to_4bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = 0

        self.call_to_4bet_count[hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] += 1

    def villain_pos(self, action_tags, villain_action):
        for j in action_tags:
            if j.split("_")[-1] == villain_action and j.split("_")[0] != "hero":
                return j.split("_")[0]

    def pre_flop_stats_ret_upd(self):
        rfi = {i: self.rfi_count[i] / self.rfi_opportunities[i] for i in self.rfi_count.keys()}

        _call_to_RFI = {i: {j: self.call_to_RFI_count[i][j] / self.action_to_RFI_opportunities[i][j] for j in
                            self.call_to_RFI_count[i].keys()} for i in self.call_to_RFI_count.keys()}
        _3bet_to_RFI = {i: {j: self._3bet_to_RFI_count[i][j] / self.action_to_RFI_opportunities[i][j] for j in
                            self._3bet_to_RFI_count[i].keys()} for i in self._3bet_to_RFI_count.keys()}
        _call_to_3bet = {i: {j: self.call_to_3bet_count[i][j] / self.action_to_3bet_opportunities[i][j] * rfi[i] for j in
                             self.call_to_3bet_count[i].keys()} for i in self.call_to_3bet_count.keys()}

        avg_3bet = {i: sum(_3bet_to_RFI[i].values())/len(_3bet_to_RFI[i].values()) for i in _3bet_to_RFI.keys()}

        _4bet_to_3bet = {i: {j: self._4bet_to_3bet_count[i][j] / self.action_to_3bet_opportunities[i][j] * rfi[i] for j in
                             self._4bet_to_3bet_count[i].keys()} for i in self._4bet_to_3bet_count.keys()}
        _call_to_4bet = {i: {j: self.call_to_4bet_count[i][j] / self.action_to_4bet_opportunities[i][j] * avg_3bet[i] for j in
                             self.call_to_4bet_count[i].keys()} for i in self.call_to_4bet_count.keys()}
        _5bet_to_4bet = {i: {j: self._5bet_to_4bet_count[i][j] / self.action_to_4bet_opportunities[i][j] * avg_3bet[i] for j in
                             self._5bet_to_4bet_count[i].keys()} for i in self._5bet_to_4bet_count.keys()}

        return {
            "VPIP%": self.VPIP,
            "PFR%": self.PFR,
            "RFI%": rfi,
            "call_to_RFI": _call_to_RFI,
            "3bet_to_RFI": _3bet_to_RFI,
            "call_to_3bet": _call_to_3bet,
            "4bet_to_3bet": _4bet_to_3bet,
            "call_to_4bet": _call_to_4bet,
            "5bet_to_4bet": _5bet_to_4bet
            }

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