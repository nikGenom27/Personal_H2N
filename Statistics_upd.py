import matplotlib.pyplot as plt
import Hand_matrix as hm


class Stats:

    def __init__(self, hand_lst):

        self.hand_lst = hand_lst
        self.data_len = len(self.hand_lst)

        self.preflop_stats = {
            "PFR": float(),
            "VPIP": float(),
            "against_NoAction": dict(),
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
            "result": self.hero_results[-1],
            "data_len": self.data_len
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
                    if "NoAction" in tag_:
                        self.add_to_hand_matrix(hand, tag_[1], "_".join([tag_[2], tag_[3]]))
                    elif "Limp" not in hand.preflop_tags["Position_action_tags"].keys():
                        if tag_[-1] == "3bet" and hand.preflop_tags["Position_action_tags"]["RFI"] != hand.hero_position:
                            self.add_to_hand_matrix(hand, tag_[1], "against_3bet_noRaiseYet")
                        elif tag_[-1] == "4bet" and hand.preflop_tags["Position_action_tags"]["4bet"] != hand.preflop_tags["Position_action_tags"]["RFI"]:
                            self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "against_4bet_cold", tag_[3])
                        else:
                            self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "_".join([tag_[2], tag_[3]]), tag_[3])
                    else:
                        """В лимпы нужно запихнуть статистику изолейтов, 3бетов против изолейтов, колов 3бетов в изолах"""
                        self.add_to_hand_matrix_taking_into_account_opponent_pos(hand, tag_[1], "_".join([tag_[2], tag_[3]]), tag_[3])

        self.preflop_stats["VPIP"] = (self.preflop_stats["VPIP"] / self.data_len) * 100

        self.preflop_stats["PFR"] = (self.preflop_stats["PFR"] / self.data_len) * 100

    def add_to_hand_matrix(self, hand, matrix_type, stat_type):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = dict()
            self.preflop_stats[stat_type][hand.hero_position]["Avg"] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position]["Avg"].add(hand.hero_cards, matrix_type, hand.hero_results)

    def add_to_hand_matrix_taking_into_account_opponent_pos(self, hand, matrix_type, stat_type, villain_action):
        if hand.hero_position not in self.preflop_stats[stat_type].keys():
            self.preflop_stats[stat_type][hand.hero_position] = dict()
            self.preflop_stats[stat_type][hand.hero_position]["Avg"] = hm.HandMatrix()

        self.preflop_stats[stat_type][hand.hero_position]["Avg"].add(hand.hero_cards, matrix_type, hand.hero_results)

        villain_pos = hand.preflop_tags["Position_action_tags"][villain_action]

        if f"{hand.hero_position}vs{villain_pos}" not in self.preflop_stats[stat_type][hand.hero_position].keys():
            self.preflop_stats[stat_type][hand.hero_position][f"vs{villain_pos}"] = hm.HandMatrix()
        self.preflop_stats[stat_type][hand.hero_position][f"vs{villain_pos}"].add(hand.hero_cards, matrix_type, hand.hero_results)

    def pre_flop_stats_ret_upd(self):
        return {"preflop_stats": self.preflop_stats}
