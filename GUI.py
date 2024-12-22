import numpy as np

import Hand as hd
from HandSorting import HandList
import Hand_matrix as hdm
import Statistics_upd as stat
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from accessify import private, protected


class GUI:

    def __init__(self):
        self.main_win = MainWin()
        self.main_win.mainloop()


class MainWin(Tk):

    def __init__(self):
        super().__init__()
        self.title("Main")
        self.hand_list = HandList()
        self.minsize(width=700, height=400)

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(row=0, column=0, sticky=(N, S, E, W))

        self.hand_listbox = HandListBoxFrame(self.mainframe)
        self.hand_listbox.grid(column=0, row=0, sticky=(N, S, E, W))
        self.hand_sort = HandSortingFrame(self.mainframe, self.filter_btn_funk, self.reset_btn_funk)
        self.hand_sort.grid(column=1, row=0, sticky=(N, S, E, W))
        self.last_filter_preset = dict()

        self.main_menu = MainMenu(self)
        self.main_menu_creation()
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def main_menu_creation(self):
        self.main_menu.create_cascade('Файл')
        self.main_menu.create_menu_sub_button('Файл',
                                              'Импортировать раздачи', self.menu_hand_import_funk)

    def menu_hand_import_funk(self):
        direct = filedialog.askdirectory()
        lst_f = os.listdir(direct)
        for f in lst_f:
            with open(f"{direct}/{f}", 'r') as hand_info:
                inf = hand_info.read().split("\n\n\n")

            for hand_inf in inf:
                if hd.data_can_be_processed(hand_inf):
                    hand = hd.Hand(hand_inf)
                    self.hand_listbox.add_hand_to_listbox(hand)
                    self.hand_list.append(hand)

    def filter_btn_funk(self):
        filters = self.hand_sort.ret_selected_filters()

        if filters == self.last_filter_preset:
            return

        if filters['pot_size_min'] is None and filters['pot_size_max'] is None:
            return

        self.hand_listbox.delete_all_hands()
        filtered_list = self.hand_list.ret_pot_size_filtered(filters['pot_size_min'], filters['pot_size_max'])
        if filters['hero_in_postflop']:
            filtered_list = filtered_list.ret_hero_in_post_flop_filtered()

        filtered_list = filtered_list.ret_hero_position_filtered([i for i in filters['hero_positions'].keys() if filters['hero_positions'][i]])
        if filters['advanced_filters']:
            filtered_list = filtered_list.ret_hero_preflop_action_filtered([i for i in filters['hero_preflop_action_tags'].keys() if filters['hero_preflop_action_tags'][i]])

        for i in filtered_list:
            self.hand_listbox.add_hand_to_listbox(i)

        self.last_filter_preset = filters

    def reset_btn_funk(self):
        self.last_filter_preset = dict()
        if len(self.hand_listbox.hand_list) != len(self.hand_list):
            self.hand_listbox.delete_all_hands()
            for i in self.hand_list:
                self.hand_listbox.add_hand_to_listbox(i)


class MainMenu(Menu):

    def __init__(self, root):
        super().__init__(root)
        root['menu'] = self
        self.menu_buttons = dict()

    def create_cascade(self, menu_cascade_name):
        self.menu_buttons[menu_cascade_name] = Menu(self)
        self.add_cascade(menu=self.menu_buttons[menu_cascade_name], label=menu_cascade_name)

    def create_menu_sub_button(self, menu_cascade_name, sub_button_name, button_funk):
        self.menu_buttons[menu_cascade_name].add_command(label=sub_button_name, command=button_funk)


class HandListBoxFrame(ttk.Frame):

    def __init__(self, root):
        self.hand_list = HandList()
        super().__init__(root)
        self.hand_listbox = Listbox(self, height=30, width=10)
        self.hand_listbox.grid(column=0, row=0, sticky=(N, W, E, S))
        self.scroll_bar = ttk.Scrollbar(self, orient=VERTICAL, command=self.hand_listbox.yview)
        self.scroll_bar.grid(column=1, row=0, sticky=(N, S))
        self.hand_listbox['yscrollcommand'] = self.scroll_bar.set

        self.stat_btn_frame = ttk.Frame(self)
        self.statistics_button = ttk.Button(self.stat_btn_frame, text="Рассчитать статистику", command=self.calculate_stats)
        self.statistics_button.grid(column=1, row=0, sticky=(E))
        self.stat_btn_frame.grid(column=0, row=1, columnspan=2, sticky=(W))
        self.hand_listbox.bind('<Double-1>', lambda e: self.open_hand_description_window(self.hand_listbox.curselection()))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.opened_hands = list()

    def open_hand_description_window(self, indexes):
        if len(indexes) != 0:
            if indexes[0] not in self.opened_hands:
                self.opened_hands.append(indexes[0])
                hand_description_window = Toplevel(self)
                hand_description_frame = HandDescriptionFrame(hand_description_window, self.hand_list[indexes[0]])
                hand_description_frame.grid(column=0, row=0)
                hand_description_window.columnconfigure(0, weight=1)
                hand_description_window.rowconfigure(0, weight=1)
                hand_description_window.protocol("WM_DELETE_WINDOW", lambda: self.destroy_hand_description_window(indexes[0], hand_description_window))

    def destroy_hand_description_window(self, index, win):
        self.opened_hands.pop(self.opened_hands.index(index))
        win.destroy()

    def add_hand_to_listbox(self, hand):
        self.hand_list.append(hand)
        text = str()
        text += card_sort(hand.hero_cards) + f' | Результат: {hand.hero_results}бб | Размер пота: {hand.river_pot_size}'

        self.hand_listbox.insert('end', text)

    def delete_all_hands(self):
        self.hand_list = HandList()
        self.hand_listbox.delete(0, "end")

    def calculate_stats(self):
        statistics = stat.Stats(self.hand_list)
        statistics.pre_flop_stats_upd()
        stats_inf = statistics.pre_flop_stats_ret_upd()
        statistics.result_stats()
        stats_inf['data_result_stats'] = statistics.result_stats_ret()

        statistics_window = Toplevel(self)
        statistics_window.minsize(width=1200, height=400)

        preflop_stat_level = PreflopStatisticFrame(statistics_window, stats_inf)
        preflop_stat_level.pack(fill=BOTH,expand=1)


class PreflopStatisticFrame(ttk.Frame):

    def __init__(self, root, stats):
        self.positions = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']
        super().__init__(root)

        self.stats_canvas = my_canvas = Canvas(self)
        self.stats_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.y_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=my_canvas.yview)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        self.stats_canvas.configure(yscrollcommand=self.y_scrollbar.set)
        root.bind("<MouseWheel>", lambda e: self.stats_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.stats_canvas.bind("<Configure>", lambda e: self.stats_canvas.config(scrollregion=self.stats_canvas.bbox(ALL)))

        self.canvas_frame = Frame(my_canvas)
        self.stats_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.general_info_frame = ttk.Frame(self.canvas_frame)
        self.general_info_frame.grid(row=0, column=0, sticky=(W))
        self.data_len_label = ttk.Label(self.general_info_frame, text=f"Количество раздач:",
                                   font=("Arial", 12))
        self.data_len_value = ttk.Label(self.general_info_frame, text=f"{np.round(stats['data_result_stats']['data_len'], 1)}",
                                       font=("Arial", 12))
        self.data_results_label = ttk.Label(self.general_info_frame, text=f"Результаты в бб:",
                                       font=("Arial", 12))
        self.data_results_value = ttk.Label(self.general_info_frame, text=f"{np.round(stats['data_result_stats']['result'], 1)}",
                                       font=("Arial", 12))
        self.data_expected_label = ttk.Label(self.general_info_frame, text=f"Ожидание в бб/100:",
                                        font=("Arial", 12))
        self.data_expected_value = ttk.Label(self.general_info_frame, text=f"{np.round(stats['data_result_stats']['bb/100'], 1)}",
                                        font=("Arial", 12))
        self.data_len_label.grid(row=0, column=0, sticky=(W))
        self.data_len_value.grid(row=0, column=1, sticky=(W))
        self.data_results_label.grid(row=1, column=0, sticky=(W))
        self.data_results_value.grid(row=1, column=1, sticky=(W))
        self.data_expected_label.grid(row=2, column=0, sticky=(W))
        self.data_expected_value.grid(row=2, column=1, sticky=(W))
        keys_lst = list(stats['preflop_stats'].keys())
        self.all_actions_frame = ttk.Frame(self.canvas_frame)
        self.all_actions_frame.grid(row=3, column=0, sticky=(W))
        for i, act_key in list(enumerate(keys_lst))[2:]:
            if len(stats['preflop_stats'][act_key]):
                action_frame = ttk.Frame(self.all_actions_frame)
                action_frame.grid(row=i, column=0, sticky=(W), pady=7)
                ttk.Label(action_frame, text=f"{act_key}", font=("Arial", 13)).grid(row=0, column=0, sticky=(W))
                position_keys_lst = list(stats['preflop_stats'][act_key].keys())
                content_action_frame = ttk.Frame(action_frame)
                content_action_frame.grid(row=1, column=0, sticky=(W))
                all_pos_frame = ttk.Frame(content_action_frame)
                all_pos_frame.grid(row=0, column=1, sticky=(W))
                info_frame = ttk.Frame(content_action_frame)
                info_frame.grid(row=0, column=0, sticky=(W, S))

                for j, key in enumerate(hdm.HandMatrix().ret_overall_keys(), start=1):
                    ttk.Label(info_frame, text=f"{key}", font=("Arial", 10)).grid(row=j, column=0, sticky=(W))

                common_frame = ttk.Frame(all_pos_frame)
                common_frame.grid(row=1, column=0, padx=8)
                self.position_action_visual(common_frame, stats['preflop_stats'][act_key]['Avg'], 'Common')

                for j, key in enumerate(self.positions, start=1):
                    if key in position_keys_lst:
                        pos_frame = ttk.Frame(all_pos_frame)
                        pos_frame.grid(row=1, column=j, padx=8)
                        self.position_action_visual(pos_frame, stats['preflop_stats'][act_key][key]['Avg'], key)

    @staticmethod
    def position_action_visual(frame, act_pos_stat, pos):
        stats = act_pos_stat.overall_count_return()
        pos_label_frame = ttk.Frame(frame)
        pos_label_frame.grid(row=0, column=0, sticky=(W), padx=2)
        ttk.Label(pos_label_frame, text=f"{pos}", font=("Arial", 11)).grid(row=0, column=0, sticky=(W), padx=2)
        hm_win = HandMatrixVisualisation(frame, act_pos_stat)
        ttk.Button(pos_label_frame, text="mat", command=hm_win.show_hand_matrix_window).grid(row=0, column=1, sticky=(W), padx=2)
        content_frame = ttk.Frame(frame)
        content_frame.grid(row=1, column=0)
        for i, act_type in enumerate(stats[list(stats.keys())[0]].keys()):
            ttk.Label(content_frame, text=f"{act_type}", font=("Arial", 10)).grid(row=0, column=i, sticky=(W), padx=2)
        for i, key in enumerate(stats.keys()):
            for j, act_type in enumerate(stats[key].keys()):
                ttk.Label(content_frame, text=f"{np.round(stats[key][act_type], 2)}", font=("Arial", 10)).grid(row=i+1, column=j, sticky=(W), padx=2)


class HandMatrixVisualisation:

    def __init__(self, root, hand_matrix):
        self.root = root
        self.hand_matrix = hand_matrix
        self.hand_matrix_window_flag = False
        self.particular_hand_stats = None
        self.win = None
        self.hand_matrix_frame = None
        self.matrix_buttons_dict = dict()

    def show_hand_matrix_window(self):
        if not self.hand_matrix_window_flag:
            self.hand_matrix_window_flag = True
            self.win = Toplevel(self.root)
            self.win.minsize(height=590, width=1120)
            self.hand_matrix_frame = ttk.Frame(self.win)
            self.hand_matrix_frame.grid(column=0, row=0)
            self.build_matrix_frame()
            self.win.protocol("WM_DELETE_WINDOW", lambda: self.destroy_hand_matrix_window())

    def destroy_hand_matrix_window(self):
        self.hand_matrix_window_flag = False
        self.win.destroy()

    def build_matrix_frame(self):
        for i, hand in enumerate(self.hand_matrix.hand_matrix.keys()):
            hand_value = {j: self.hand_matrix.hand_matrix[hand][j]['value'] for j in self.hand_matrix.hand_matrix[hand].keys()}
            hand_count = {j: self.hand_matrix.hand_matrix[hand][j]['count'] for j in self.hand_matrix.hand_matrix[hand].keys()}
            hand_frame = ttk.Frame(self.hand_matrix_frame)
            hand_frame.grid(row=i // 13, column=i % 13, sticky=(W), padx=2)
            self.build_matrix_hand_button(hand_frame, hand, hand_value, hand_count)
            color = 'red' if sum(hand_value.values()) < 0 else 'green'
            color = 'gray' if sum(hand_value.values()) == 0 else color
            ttk.Label(hand_frame, text=f"{np.round(sum(hand_value.values()), 2)}", font=("Arial", 10), background=color).grid(row=1, column=0, sticky=(W, E), padx=2)

    def build_matrix_hand_button(self, hand_frame, hand, hand_value, hand_count):
        ttk.Button(hand_frame, text=f"{hand}", width=7,
                   command=lambda: self.build_particular_hand_frame(hand_value,
                                                                    hand_count, hand)).grid(row=0, column=0, sticky=(W),
                                                                                            padx=2)

    def build_particular_hand_frame(self, hand_value, hand_count, hand):
        if self.particular_hand_stats is None:
            self.particular_hand_stats = ttk.Frame(self.win)
            self.particular_hand_stats.grid(column=1, row=0)
            self.show_particular_hand(hand_value, hand_count, hand)
        else:
            self.particular_hand_stats.destroy()
            self.particular_hand_stats = ttk.Frame(self.win)
            self.particular_hand_stats.grid(column=1, row=0)
            self.show_particular_hand(hand_value, hand_count, hand)

    def show_particular_hand(self, hand_value, hand_count, hand):
        hand_label = ttk.Label(self.particular_hand_stats, font=("Arial", 13), text=hand)
        hand_label.grid(column=0, row=0)
        hand_count_ = ttk.Label(self.particular_hand_stats, font=("Arial", 10), text=f"{sum(hand_count.values())}")
        hand_count_.grid(column=1, row=0)
        hand_common_value = ttk.Label(self.particular_hand_stats, font=("Arial", 10),
                                      text=f"{np.round(sum(hand_value.values()), 2)}bb")
        hand_common_value.grid(column=2, row=0)
        for i, key in enumerate(hand_value.keys(), start=1):
            value_frame = ttk.Frame(self.particular_hand_stats)
            value_frame.grid(column=0, row=i, padx=4)
            percent_frame = ttk.Frame(self.particular_hand_stats)
            percent_frame.grid(column=1, row=i, padx=4)
            exp_value_frame = ttk.Frame(self.particular_hand_stats)
            exp_value_frame.grid(column=2, row=i, padx=4)
            hand_action_value_lbl = ttk.Label(value_frame, font=("Arial", 10), text=f"{key}_value")
            hand_action_value = ttk.Label(value_frame, font=("Arial", 10), text=f"{np.round(hand_value[key], 2)}bb")
            hand_action_value_lbl.grid(row=0, column=0, sticky=(W))
            hand_action_value.grid(row=1, column=0, sticky=(W))
            hand_action_percentage_lbl = ttk.Label(percent_frame, font=("Arial", 10),
                                                   text=f"{key}_percent")
            hand_action_percentage = ttk.Label(percent_frame, font=("Arial", 10),
                                               text=f"{np.round(hand_count[key] / sum(hand_count.values()), 2)}")
            hand_action_percentage_lbl.grid(row=0, column=0, sticky=(W))
            hand_action_percentage.grid(row=1, column=0, sticky=(W))
            hand_action_exp_value_lbl = ttk.Label(exp_value_frame, font=("Arial", 10),
                                                  text=f"{key}_exp_value(bb/100)")
            exp_value = np.round(hand_value[key] / hand_count[key] * 100, 2) if hand_count[key] != 0 else 0
            hand_action_exp_value = ttk.Label(exp_value_frame, font=("Arial", 10),
                                              text=f"{exp_value}")
            hand_action_exp_value_lbl.grid(row=0, column=0, sticky=(W))
            hand_action_exp_value.grid(row=1, column=0, sticky=(W))


class HandSortingFrame(ttk.Frame):
    def __init__(self, root, filter_btn_funk, reset_btn_funk):
        super().__init__(root)

        self.filter_by_pot_size_frame = FilterByPotSizeFrame(self)
        self.hero_in_postflop_frame = HeroInFrame(self)
        self.filter_by_pos = FilterByHeroPositionFrame(self)

        self.more_filters_frame = ttk.Frame(self)
        self.filter_by_hero_preflop_action = FilteredByHeroPreflopActionsFrame(self.more_filters_frame)
        self.filter_by_hero_preflop_action.grid(row=0, column=0)
        self.more_filters_frame.grid(row=0, column=1, rowspan=4)
        self.more_filters_frame.grid_remove()

        self.hero_in_postflop_frame.grid(row=2, column=0, sticky=(N, W))
        self.filter_by_pot_size_frame.grid(row=0, column=0, sticky=(N, W))
        self.filter_by_pos.grid(row=1, column=0, sticky=(N, W))

        self.buttons_frame = ttk.Frame(self)
        self.filter_button = ttk.Button(self.buttons_frame, text="Фильтр", command=filter_btn_funk)
        self.reset_button = ttk.Button(self.buttons_frame, text="Сброс", command=reset_btn_funk)

        self.more_filters_flag = False
        self.more_filters_button = ttk.Button(self.buttons_frame, text='Расширить', command=self.more_filters_funk)
        self.filter_button.grid(row=0, column=0)
        self.reset_button.grid(row=0, column=1)
        self.more_filters_button.grid(row=0, column=2)
        self.buttons_frame.grid(row=4, column=0, columnspan=10)

    def more_filters_funk(self):
        if self.more_filters_flag:
            self.more_filters_button['text'] = 'Расширить'
            self.more_filters_frame.grid_remove()
            self.more_filters_flag = False
        else:
            self.more_filters_button['text'] = 'Свернуть'
            self.more_filters_frame.grid()
            self.more_filters_flag = True

    def ret_selected_filters(self):
        minimum, maximum = self.filter_by_pot_size_frame.ret_min_max_pot_sizes()
        filtered_dct = {
            'advanced_filters': self.more_filters_flag,
            'pot_size_min': minimum,
            'pot_size_max': maximum,
            'hero_in_postflop': self.hero_in_postflop_frame.ret_hero_in_enabled(),
            'hero_positions': self.filter_by_pos.ret_hero_in_enabled(),
            'hero_preflop_action_tags': self.filter_by_hero_preflop_action.ret_action_tag_enabled()
        }
        return filtered_dct


class FilterByPotSizeFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root, padding="3 3 3 3")
        self.filter_by_pot_size_label = ttk.Label(self, text="Фильтр по размеру пота", font=("Arial", 10))
        self.minimum_pot_size_label = ttk.Label(self, text="Минимум", font=("Arial", 9), padding="3 3 3 3")
        self.maximum_pot_size_label = ttk.Label(self, text="Максимум", font=("Arial", 9), padding="3 3 3 3")
        self.minimum_pot_size = ttk.Entry(self)
        self.maximum_pot_size = ttk.Entry(self)
        self.filter_by_pot_size_label.grid(row=0, column=0, columnspan=2)
        self.minimum_pot_size_label.grid(row=1, column=0, sticky=(W))
        self.maximum_pot_size_label.grid(row=2, column=0, sticky=(W))
        self.minimum_pot_size.grid(row=1, column=1, sticky=(W))
        self.maximum_pot_size.grid(row=2, column=1, sticky=(W))

    def ret_min_max_pot_sizes(self):
        minimum = 0
        maximum = 1000000

        try:
            minimum = float(self.minimum_pot_size.get())
        except ValueError:
            if self.minimum_pot_size.get() != '':
                minimum = None

        try:
            maximum = float(self.maximum_pot_size.get())
        except ValueError:
            if self.maximum_pot_size.get() != '':
                maximum = None
        return minimum, maximum


class HeroInFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root, padding="3 3 3 3")
        self.enabled = IntVar()
        self.hero_in_checkbox = ttk.Checkbutton(self, text='Только Hero in postflop раздачи', variable=self.enabled)
        self.hero_in_checkbox.grid(row=0, column=0)

    def ret_hero_in_enabled(self):
        return bool(self.enabled.get())


class FilterByHeroPositionFrame(ttk.Frame):
    def __init__(self, root):
        self.positions = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']
        super().__init__(root, padding="3 3 3 3")
        self.enabled = [IntVar() for i in range(6)]
        self.hero_position_label = ttk.Label(self, text="Фильтр по позиции Hero", font=("Arial", 10))
        self.hero_position_label.grid(row=0, column=0, columnspan=2)
        for i in range(3):
            for j in range(2):
                self.hero_in_checkbox = ttk.Checkbutton(self, text=self.positions[i+(j*3)], variable=self.enabled[i+(j*3)])
                self.hero_in_checkbox.invoke()
                self.hero_in_checkbox.grid(row=i+1, column=j, sticky=('W'))

    def ret_hero_in_enabled(self):
        filtered = {self.positions[i]: float(self.enabled[i].get()) for i in range(len(self.positions))}
        return filtered


"""
Не дописано, дописать
"""


class FilteredByHeroPreflopActionsFrame(ttk.Frame):

    def __init__(self, root):
        super().__init__(root, padding="3 3 3 3")
        self.hero_actions = ['against_NoAction', 'against_Limp', 'against_Isolate',
                             'against_RFI', 'against_3bet', 'against_4bet',
                             'against_5bet']
        self.enabled = [IntVar() for i in range(len(self.hero_actions))]
        self.selection_enabled = IntVar()
        self.hero_action_label = ttk.Label(self, text="Фильтр по действиям Hero на префлопе", font=("Arial", 10))
        self.hero_action_label.grid(row=0, column=0, columnspan=2)
        for i in range(len(self.hero_actions)):
            self.hero_action_checkbox = ttk.Checkbutton(self, text=self.hero_actions[i], variable=self.enabled[i])
            self.hero_action_checkbox.invoke()
            self.hero_action_checkbox.grid(row=i+1, column=0, sticky=('W'))

    def ret_action_tag_enabled(self):
        filtered = {self.hero_actions[i]: float(self.enabled[i].get()) for i in range(len(self.hero_actions))}
        return filtered


class HandDescriptionFrame(ttk.Frame):

    def __init__(self, root, hand):
        self.hand = hand
        super().__init__(root)

        self.hero_cards_text = None
        self.card_one_label = None
        self.card_two_label = None

        self.hero_position_text = None
        self.hero_position_label = None

        self.hero_result_text = None
        self.hero_result_label = None

        self.board_text = ttk.Label(self, text="Board:", font=("Arial", 14))
        self.first_flop_board_card_one = ttk.Label(self, font=("Arial", 14))
        self.first_flop_board_card_two = ttk.Label(self, font=("Arial", 14))
        self.first_flop_board_card_three = ttk.Label(self, font=("Arial", 14))
        self.first_turn_card_label = ttk.Label(self, font=("Arial", 14))
        self.first_river_card_label = ttk.Label(self, font=("Arial", 14))
        self.second_flop_board_card_one = ttk.Label(self, font=("Arial", 14))
        self.second_flop_board_card_two = ttk.Label(self, font=("Arial", 14))
        self.second_flop_board_card_three = ttk.Label(self, font=("Arial", 14))
        self.second_turn_card_label = ttk.Label(self, font=("Arial", 14))
        self.second_river_card_label = ttk.Label(self, font=("Arial", 14))

        self.action_frame = None
        self.street_buttons = None
        self.action_listbox = None
        self.action_scroll_bar = None
        self.pot_size_text = None
        self.pot_size_label = None
        self.pre_flop_button = None
        self.flop_button = None
        self.turn_button = None
        self.river_button = None

        self.stack_sizes_frame = None
        self.position_stack_texts_labels = list()
        self.position_stack_values_labels = list()

        self.hero_cards_visualisation()
        self.hero_position_visualisation()
        self.hero_result_visualisation()
        self.board_visualisation()
        self.action_frame_visual()

    def hero_cards_visualisation(self):
        cards_text = card_sort(self.hand.hero_cards).split()
        self.hero_cards_text = ttk.Label(self, text="Hero cards:", font=("Arial", 14))
        self.card_one_label = ttk.Label(self, text=f"{cards_text[0]}", font=("Arial", 14),
                                        foreground=card_color_choose(cards_text[0]))
        self.card_two_label = ttk.Label(self, text=f"{cards_text[1]}", font=("Arial", 14),
                                        foreground=card_color_choose(cards_text[1]))
        self.hero_cards_text.grid(column=0, row=0, sticky=(W), ipadx=5)
        self.card_one_label.grid(column=1, row=0, sticky=(W))
        self.card_two_label.grid(column=2, row=0, sticky=(W), ipadx=20)

    def hero_position_visualisation(self):
        self.hero_position_text = ttk.Label(self, text="Hero position:", font=("Arial", 14))
        self.hero_position_label = ttk.Label(self, text=f"{self.hand.hero_position}", font=("Arial", 14))
        self.hero_position_text.grid(column=0, row=1, sticky=(W), ipadx=5)
        self.hero_position_label.grid(column=1, row=1, columnspan=2, sticky=(W))

    def hero_result_visualisation(self):
        self.hero_result_text = ttk.Label(self, text="Hero result:", font=("Arial", 14))
        self.hero_result_label = ttk.Label(self, text=f"{self.hand.hero_results}bb", font=("Arial", 14))
        self.hero_result_text.grid(column=0, row=2, sticky=(W), ipadx=5)
        self.hero_result_label.grid(column=1, row=2, columnspan=2, sticky=(W))

    def board_visualisation(self):
        self.board_text.grid(column=3, row=0, columnspan=5, sticky=(W), ipadx=10)
        if self.hand.flop_exist:
            self.card_visualisation(self.first_flop_board_card_one, self.hand.flop_board[0])
            self.first_flop_board_card_one.grid(column=3, row=1, sticky=(W))
            self.card_visualisation(self.first_flop_board_card_two, self.hand.flop_board[1])
            self.first_flop_board_card_two.grid(column=4, row=1, sticky=(W))
            self.card_visualisation(self.first_flop_board_card_three, self.hand.flop_board[2])
            self.first_flop_board_card_three.grid(column=5, row=1, sticky=(W))
            if self.hand.turn_exist:
                self.card_visualisation(self.first_turn_card_label, self.hand.turn_card)
                self.first_turn_card_label.grid(column=6, row=1, sticky=(W))
                if self.hand.river_exist:
                    self.card_visualisation(self.first_river_card_label, self.hand.river_card)
                    self.first_river_card_label.grid(column=7, row=1, sticky=(W))
                else:
                    self.card_visualisation(self.first_river_card_label, self.hand.first_river)
                    self.first_river_card_label.grid(column=7, row=1, sticky=(W))
                    self.card_visualisation(self.second_river_card_label, self.hand.second_river)
                    self.second_river_card_label.grid(column=7, row=2, sticky=(W))
            else:
                self.card_visualisation(self.first_turn_card_label, self.hand.first_turn)
                self.first_turn_card_label.grid(column=6, row=1, sticky=(W))
                self.card_visualisation(self.second_turn_card_label, self.hand.second_turn)
                self.second_turn_card_label.grid(column=6, row=2, sticky=(W))

                self.card_visualisation(self.first_river_card_label, self.hand.first_river)
                self.first_river_card_label.grid(column=7, row=1, sticky=(W))
                self.card_visualisation(self.second_river_card_label, self.hand.second_river)
                self.second_river_card_label.grid(column=7, row=2, sticky=(W))
        elif len(self.hand.first_flop) != 0:
            self.card_visualisation(self.first_flop_board_card_one, self.hand.first_flop[0])
            self.first_flop_board_card_one.grid(column=3, row=1, sticky=(W))
            self.card_visualisation(self.first_flop_board_card_two, self.hand.first_flop[1])
            self.first_flop_board_card_two.grid(column=4, row=1, sticky=(W))
            self.card_visualisation(self.first_flop_board_card_three, self.hand.first_flop[2])
            self.first_flop_board_card_three.grid(column=5, row=1, sticky=(W))
            self.card_visualisation(self.second_flop_board_card_one, self.hand.second_flop[0])
            self.second_flop_board_card_one.grid(column=3, row=1, sticky=(W))
            self.card_visualisation(self.second_flop_board_card_two, self.hand.second_flop[1])
            self.second_flop_board_card_two.grid(column=4, row=1, sticky=(W))
            self.card_visualisation(self.second_flop_board_card_three, self.hand.second_flop[2])
            self.second_flop_board_card_three.grid(column=5, row=1, sticky=(W))

            self.card_visualisation(self.first_turn_card_label, self.hand.first_turn)
            self.first_turn_card_label.grid(column=6, row=1, sticky=(W))
            self.card_visualisation(self.second_turn_card_label, self.hand.second_turn)
            self.second_turn_card_label.grid(column=6, row=2, sticky=(W))

            self.card_visualisation(self.first_river_card_label, self.hand.first_river)
            self.first_river_card_label.grid(column=7, row=1, sticky=(W))
            self.card_visualisation(self.second_river_card_label, self.hand.second_river)
            self.second_river_card_label.grid(column=7, row=2, sticky=(W))

    @staticmethod
    def card_visualisation(card_label, card):
        card_label['text'] = card
        card_label['foreground'] = card_color_choose(card)

    def action_frame_visual(self):
        self.action_frame = ttk.Frame(self)
        self.street_buttons = ttk.Frame(self.action_frame)
        self.stack_sizes_frame = ttk.Frame(self.action_frame)

        self.action_listbox = Listbox(self.action_frame)
        self.action_scroll_bar = ttk.Scrollbar(self.action_frame, orient=VERTICAL, command=self.action_listbox.yview)
        self.pot_size_text = ttk.Label(self.action_frame, text='Pot size:', font=("Arial", 14))
        self.pot_size_label = ttk.Label(self.action_frame, font=("Arial", 14))

        self.pre_flop_button = ttk.Button(self.street_buttons, text="Preflop",
                                     command=lambda: self.action_listbox_add(self.hand.preflop_action,
                                                                             self.hand.stack_sizes
                                                                             ))
        self.pre_flop_button.grid(column=0, row=0)

        self.flop_button = ttk.Button(self.street_buttons, text="Flop",
                                 command=lambda: self.action_listbox_add(self.hand.flop_action,
                                                                         self.hand.end_of_preflop_stack_sizes,
                                                                         self.hand.preflop_pot_size,
                                                                         self.hand.end_of_preflop_players_in))
        self.flop_button.grid(column=1, row=0)

        self.turn_button = ttk.Button(self.street_buttons, text="Turn",
                                 command=lambda: self.action_listbox_add(self.hand.turn_action,
                                                                         self.hand.end_of_flop_stack_sizes,
                                                                         self.hand.flop_pot_size,
                                                                         self.hand.end_of_flop_players_in))
        self.turn_button.grid(column=2, row=0)

        self.river_button = ttk.Button(self.street_buttons, text="River",
                                  command=lambda: self.action_listbox_add(self.hand.river_action,
                                                                          self.hand.end_of_turn_stack_sizes,
                                                                          self.hand.turn_pot_size,
                                                                          self.hand.end_of_turn_players_in))
        self.river_button.grid(column=3, row=0)
        self.pot_size_text.grid(column=1, row=0)
        self.pot_size_label.grid(column=1, row=1, sticky=(N))

        self.action_listbox.grid(column=0, row=1, sticky=(N, W, E, S))
        self.action_scroll_bar.grid(column=0, row=1, sticky=(N, S, E))
        self.action_listbox['yscrollcommand'] = self.action_scroll_bar.set

        self.street_buttons.grid(column=0, row=0)
        self.stack_sizes_frame.grid(column=0, row=2, columnspan=10, sticky=(N, W, E, S))
        self.action_frame.grid(column=0, row=3, columnspan=10)

    def action_listbox_add(self, action, stack_sizes, pot_size='', players_in=None):
        sixmax_pos_order = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']
        for i in self.position_stack_texts_labels:
            i.destroy()
        for i in self.position_stack_values_labels:
            i.destroy()

        self.position_stack_texts_labels = list()
        self.position_stack_values_labels = list()

        self.action_listbox.delete(0, 'end')
        self.pot_size_label['text'] = str(pot_size)
        for i in action:
            text = ' '.join(list(map(str, i[1])))
            self.action_listbox.insert('end', f'{self.hand.positions[i[0]]}: {text}')
        for i in self.hand.positions.keys():
            if players_in is None:
                self.position_stack_texts_labels.append(ttk.Label(self.stack_sizes_frame, text=f'{self.hand.positions[i]}:', font=("Arial", 14)))
                self.position_stack_values_labels.append(ttk.Label(self.stack_sizes_frame, text=f'{stack_sizes[i]}', font=("Arial", 14)))
                self.position_stack_texts_labels[-1].grid(column=sixmax_pos_order.index(self.hand.positions[i]), row=2)
                self.position_stack_values_labels[-1].grid(column=sixmax_pos_order.index(self.hand.positions[i]), row=3)
            elif players_in[i]:
                self.position_stack_texts_labels.append(
                    ttk.Label(self.stack_sizes_frame, text=f'{self.hand.positions[i]}:', font=("Arial", 14)))
                self.position_stack_values_labels.append(
                    ttk.Label(self.stack_sizes_frame, text=f'{stack_sizes[i]}', font=("Arial", 14)))
                self.position_stack_texts_labels[-1].grid(column=sixmax_pos_order.index(self.hand.positions[i]), row=2)
                self.position_stack_values_labels[-1].grid(column=sixmax_pos_order.index(self.hand.positions[i]), row=3)


def card_sort(cards):
    alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    alph_card_idx = sorted(
        [alph_lst.index(cards[0][0]), alph_lst.index(cards[1][0])])
    if cards[0][0] == alph_lst[alph_card_idx[0]]:
        return f'{alph_lst[alph_card_idx[0]]}{cards[0][1]} {alph_lst[alph_card_idx[1]]}{cards[1][1]}'
    else:
        return f'{alph_lst[alph_card_idx[0]]}{cards[1][1]} {alph_lst[alph_card_idx[1]]}{cards[0][1]}'


def card_color_choose(card):
    if len(card) == 0:
        return
    if card[-1] == 's':
        return 'black'
    elif card[-1] == 'h':
        return 'red'
    elif card[-1] == 'd':
        return 'blue'
    elif card[-1] == 'c':
        return 'green'


if __name__ == '__main__':
    GUI()
