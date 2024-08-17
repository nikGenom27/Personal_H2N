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
                    self.hand_matrix[card1 + card2] = dict()
                elif card2 + card1 + "s" in self.hand_matrix.keys():
                    self.hand_matrix[card2 + card1 + "o"] = dict()
                else:
                    self.hand_matrix[card1 + card2 + "s"] = dict()

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

        if matrix_type not in self.hand_matrix[self.cur_cards].keys():
            self.hand_matrix[self.cur_cards][matrix_type] = {
                "count": 1,
                "value": value
            }
        else:
            self.hand_matrix[self.cur_cards][matrix_type]["count"] += 1
            self.hand_matrix[self.cur_cards][matrix_type]["value"] += value