import numpy as np


class HandMatrix:

    def __init__(self):

        self.hand_matrix = dict()
        self.alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]  # данный порядок крайне важен
        self.cur_cards = str()
        self.matrix_creation()

    def matrix_creation(self):
        for card1 in self.alph_lst:
            for card2 in self.alph_lst:
                if card1 == card2:
                    self.hand_matrix[card1 + card2] = {'raises': {"count": 0, "value": 0},
                                                       'calls': {"count": 0, "value": 0},
                                                       'folds': {"count": 0, "value": 0}}
                elif card2 + card1 + "s" in self.hand_matrix.keys():
                    self.hand_matrix[card2 + card1 + "o"] = {'raises': {"count": 0, "value": 0},
                                                             'calls': {"count": 0, "value": 0},
                                                             'folds': {"count": 0, "value": 0}}
                else:
                    self.hand_matrix[card1 + card2 + "s"] = {'raises': {"count": 0, "value": 0},
                                                             'calls': {"count": 0, "value": 0},
                                                             'folds': {"count": 0, "value": 0}}

    def hand_transform(self, cards):
        self.cur_cards = str()
        self.cur_cards = sorted([self.alph_lst.index(cards[0][0]), self.alph_lst.index(cards[1][0])])
        self.cur_cards = self.alph_lst[self.cur_cards[0]] + self.alph_lst[self.cur_cards[1]]
        if self.cur_cards[0] != self.cur_cards[1]:
            if cards[0][1] == cards[1][1]:
                self.cur_cards += "s"
            else:
                self.cur_cards += "o"

    def add(self, cards, matrix_type, value):

        self.hand_transform(cards)

        self.hand_matrix[self.cur_cards][matrix_type]["count"] += 1
        self.hand_matrix[self.cur_cards][matrix_type]["value"] += value

    def overall_count_return(self):
        count_ = dict()
        percentages_ = dict()
        value_ = dict()
        value_per_hand = dict()
        for cards in self.hand_matrix.keys():
            for type_ in self.hand_matrix[cards].keys():
                if type_ not in count_.keys():
                    count_[type_] = int()
                    percentages_[type_] = float()
                    value_[type_] = float()
                count_[type_] += self.hand_matrix[cards][type_]["count"]
                value_[type_] += self.hand_matrix[cards][type_]["value"]
        for type_ in percentages_.keys():
            percentages_[type_] = count_[type_] / sum(count_.values()) * 100
            value_per_hand[type_] = 0
            if count_[type_] != 0:
                value_per_hand[type_] = np.round(value_[type_] / count_[type_] * 100, 1)

        return {"hand_count": count_, "percentages": percentages_,
                "total_value": value_, "value_per_100_hand": value_per_hand}

    def hand_matrix_return(self):
        return self.hand_matrix

    @staticmethod
    def ret_overall_keys():
        return ["hand_count", "percentages",
                "total_value", "value_per_100_hand"]