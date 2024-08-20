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

        self.preflop_stats = {
            "PFR": float(),
            "VPIP": float(),
            "openAction": dict(),
            "against_Limp": dict(),
            "against_Isolate": dict(),
            "against_RFI": dict(),
            "against_3bet": dict(),
            "against_3bet_noRaiseYet": dict(),
            "against_4bet": dict(),
            "against_4bet_cold": dict(),
            "against_5bet": dict()
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
            if len(hand.preflop_tags["Hero_action_tags"]) != 0:
                """Статистика бордов на которых не было лимпа"""
                if "calls" in hand.preflop_tags["Hero_action_tags"][0] or "raises" in hand.preflop_tags["Hero_action_tags"][0]:
                    self.preflop_stats["VPIP"] += 1

                for tag in hand.preflop_tags["Hero_action_tags"]:
                    tag_ = tag.split("_")
                    if tag_[1] == "raises":
                        self.preflop_stats["PFR"] += 1
                    if "against" not in tag_:
                        self.add_to_hand_matrix(hand, tag_[1], "openAction")
                    elif "Limp" not in hand.preflop_tags["Position_action_tags"].keys():
                        if tag_[-1] == "3bet" and hand.preflop_tags["Position_action_tags"]["RFI"] != hand.hero_position:
                            self.add_to_hand_matrix(hand, tag_[1], "against_3bet_noRaiseYet")
                        elif tag_[-1] == "4bet" and hand.preflop_tags["Position_action_tags"]["4bet"] != hand.preflop_tags["Position_action_tags"]["RFI"]:
                            self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "against_4bet_cold", tag_[3])
                        else:
                            self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "_".join([tag_[2], tag_[3]]), tag_[3])
                    else:
                        """В лимпы нужно запихнуть статистику изолейтов, 3бетов против изолейтов, колов 3бетов в изолах"""
                        if "against" not in tag_:
                            self.add_to_hand_matrix(hand, tag_[1], "Limp")
                        elif tag_[-1] == "Limp" or tag_[-1] == "Isolate":
                            self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "_".join([tag_[2], tag_[3]]), tag_[3])

        self.preflop_stats["VPIP"] = (self.preflop_stats["VPIP"] / self.data_len) * 100

        self.preflop_stats["PFR"] = (self.preflop_stats["PFR"] / self.data_len) * 100

    def add_to_hand_matrix(self, hand, matrix_type, stat_type):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position].add(hand.hero_cards, matrix_type, hand.hero_results)

    def add_to_hand_matrix_taking_into_account_opponent_pos(self, hand, matrix_type, stat_type, villain_action):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = dict()

        villain_pos = hand.preflop_tags["Position_action_tags"][villain_action]

        if f"{hand.hero_position}vs{villain_pos}" not in self.preflop_stats[stat_type][hand.hero_position].keys():
            self.preflop_stats[stat_type][hand.hero_position][f"{hand.hero_position}vs{villain_pos}"] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position][f"{hand.hero_position}vs{villain_pos}"].add(hand.hero_cards, matrix_type, hand.hero_results)

    def pre_flop_stats_ret_upd(self):
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