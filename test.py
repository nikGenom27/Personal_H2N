import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Statistics_upd as stat
import os
import Hand as hnd

# path = 'NLH 0.02-0.05 01.04.24-30.04.24'
# path = 'NLH 0.05-0.10 01.05.24-31.05.24'


inf_lst = list()
hand_inf_lst = list()
value = list()

folders = ['NLH 0.02-0.05 01.04.24-30.04.24', 'NLH 0.05-0.10 01.05.24-31.05.24', ]

for l in folders:
    lst_dr = os.listdir(l)
    for f in lst_dr:
        with open(f"{l}/{f}", 'r') as hand_info:
            inf = hand_info.read().split("\n\n\n")

        for hand in inf:
            if hnd.data_can_be_processed(hand):
                hand_inf = hnd.Hand(hand)
                hand_inf_lst.append(hand)
                inf_lst.append(hand_inf)
                try:
                    value.append(hand_inf.hero_results + value[-1])
                except IndexError:
                    value.append(hand_inf.hero_results)

stats_upd = stat.Stats(inf_lst)
stats_upd.pre_flop_stats_upd()
stats_inf = stats_upd.pre_flop_stats_ret_upd()
for stat in stats_inf["preflop_stats"]:
    print(stat)
    for pos in stats_inf["preflop_stats"][stat].keys():
        if type(stats_inf["preflop_stats"][stat][pos]) is not dict:
            count, percentages, value = stats_inf["preflop_stats"][stat][pos].overall_count_return()
            print(pos, percentages, count, value)
        else:
            for HeroPos_vs_OppPos in stats_inf["preflop_stats"][stat][pos].keys():
                count, percentages, value = stats_inf["preflop_stats"][stat][pos][HeroPos_vs_OppPos].overall_count_return()
                print(HeroPos_vs_OppPos, percentages, count, value)
    print()
    '''
    for j in ["UTG", "HJ", "CO", "BTN", "SB", "BB"]:
        for k in stats_inf'''

stats_upd.result_stats()
result = stats_upd.result_stats_ret()
for hand in result:
    print(hand, result[hand])
"""
hand_dct = stats.ret_hand_matrix_value()
alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
for hand in alph_lst:

    value_lst = list()
    for j in alph_lst:
        if hand+j in hand_dct[0].keys():
            print(hand+j, end="\t\t")
            value_lst.append(np.round(hand_dct[0][hand+j][2]/hand_dct[0][hand+j][1], 1))
        elif hand+j+"s" in hand_dct[0].keys():
            print(hand+j+"s", end="\t\t")
            value_lst.append(np.round(hand_dct[0][hand+j+"s"][2]/hand_dct[0][hand+j+"s"][1], 1))
        else:
            print(j+hand+"o", end="\t\t")
            value_lst.append(np.round(hand_dct[0][j+hand+"o"][2]/hand_dct[0][j+hand+"o"][1], 1))
    print()
    print(" \t".join(list(map(str, value_lst))))
    print()

for hand in alph_lst:

    value_lst = list()
    for j in alph_lst:
        if hand + j in hand_dct[1].keys():
            print(hand + j, end="\t\t")
            value_lst.append(np.round(hand_dct[1][hand + j][2] / hand_dct[1][hand + j][1], 1))
        elif hand + j + "s" in hand_dct[1].keys():
            print(hand + j + "s", end="\t\t")
            value_lst.append(np.round(hand_dct[1][hand + j + "s"][2] / hand_dct[1][hand + j + "s"][1], 1))
        else:
            print(j + hand + "o", end="\t\t")
            value_lst.append(np.round(hand_dct[1][j + hand + "o"][2] / hand_dct[1][j + hand + "o"][1], 1))
    print()
    print(" \t".join(list(map(str, value_lst))))
    print()"""

# stats.show_result_plot()