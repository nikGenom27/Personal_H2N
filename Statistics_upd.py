import numpy as np
import matplotlib.pyplot as plt
import Hand_matrix as hm

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

        self.pfr_count = int()  # переменная отвечающая за кол-во раздач в которых hero играл рейзом на префлопе
        self.vpip_count = int()  # переменная отвечающая за кол-во раздач в которых hero участвовал\

        self.preflop_stats = {
            "rfi": dict(),
            "against_rfi": dict(),
            "against_3bet": dict(),
            "open_4bet": dict(),
            "against_4bet": dict()
        }

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
            matrix_type = str()

            """Подсчет vpip"""
            if "hero_raises" in hand.preflop_tags["Hero_action_tags"] or "hero_calls" in hand.preflop_tags["Hero_action_tags"]:
                self.vpip_count += 1

            """Подсчет pfr"""
            if "hero_raises" in hand.preflop_tags["Hero_action_tags"]:
                if "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                    self.pfr_count += 1

                if "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                    self.pfr_count += 1

                if "hero_4bet" in hand.preflop_tags["Hero_action_tags"]:
                    self.pfr_count += 1

                if "hero_5bet" in hand.preflop_tags["Hero_action_tags"]:
                    self.pfr_count += 1

            """Статистика бордов на которых не было лимпа"""
            if "limped" not in hand.preflop_tags["Hero_action_tags"]:

                if "hero_raises" in hand.preflop_tags["Hero_action_tags"]:
                    matrix_type = "raise"
                    if "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix(hand, matrix_type, "rfi")

                    if "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_rfi", "RFI")

                    if "hero_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_3bet", "3bet")

                    elif "hero_4bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix(hand, matrix_type, "open_4bet")

                    if "hero_5bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_4bet", "4bet")

                if "hero_folds" in hand.preflop_tags["Hero_action_tags"]:
                    matrix_type = "fold"
                    if "hero_folds_to_No_raise" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix(hand, matrix_type, "rfi")

                    if "hero_folds_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_rfi", "RFI")

                    if "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_3bet", "3bet")

                    elif "hero_folds_to_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix(hand, matrix_type, "open_4bet")

                    if "hero_folds_to_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_4bet", "4bet")

                if "hero_calls" in hand.preflop_tags["Hero_action_tags"]:
                    matrix_type = "call"
                    if "hero_calls_to_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_rfi", "RFI")

                    if "hero_calls_to_3bet" in hand.preflop_tags["Hero_action_tags"] and "hero_RFI" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_3bet", "3bet")

                    elif "hero_calls_to_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix(hand, matrix_type, "open_4bet")

                    if "hero_calls_to_4bet" in hand.preflop_tags["Hero_action_tags"] and "hero_3bet" in hand.preflop_tags["Hero_action_tags"]:
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, matrix_type, "against_4bet", "4bet")
            else:
                """В лимпы нужно запихнуть статистику изолейтов, 3бетов против изолейтов, колов 3бетов в изолах"""
                pass

    def add_to_hand_matrix(self, hand, matrix_type, stat_type):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position].add(hand.hero_cards, matrix_type, hand.hero_results)

    def add_to_hand_matrix_taking_into_account_opponent_pos(self, hand, matrix_type, stat_type, villain_action):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = dict()

        villain_pos = self.villain_pos(hand.preflop_tags["Hero_action_tags"], villain_action)

        if f"{hand.hero_position}vs{villain_pos}" not in self.preflop_stats[stat_type][hand.hero_position].keys():
            self.preflop_stats[stat_type][hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position][f"{hand.hero_position}vs{villain_pos}"].add(hand.hero_cards, matrix_type, hand.hero_results)

    @staticmethod
    def villain_pos(action_tags, villain_action):
        for j in action_tags:
            if j.split("_")[-1] == villain_action and j.split("_")[0] != "hero":
                return j.split("_")[0]
        return 0

    def pre_flop_stats_ret_upd(self):
        vpip = (self.vpip_count / self.data_len) * 100

        pfr = (self.pfr_count / self.data_len)*100

        """"VPIP%": vpip,
        "PFR%": pfr,"""
        return {
            "preflop_stats": self.preflop_stats
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