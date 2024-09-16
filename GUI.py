import Hand as hd
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

        self.hand_listbox = HandListBoxFrame(self)
        self.hand_listbox.grid(column=0, row=0, sticky=(N, S, E, W))

        self.main_menu = MainMenu(self)
        self.main_menu_creation()

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
        self.hand_list = list()
        super().__init__(root)
        self.hand_listbox = Listbox(self, height=30, width=50)
        self.hand_listbox.grid(column=0, row=0, sticky=(N, W, E, S))
        self.scroll_bar = ttk.Scrollbar(self, orient=VERTICAL, command=self.hand_listbox.yview)
        self.scroll_bar.grid(column=1, row=0, sticky=(N, S))
        self.hand_listbox['yscrollcommand'] = self.scroll_bar.set
        ttk.Label(self, text="Список раздач", anchor=(W), font=('Arial', 10)).grid(column=0, columnspan=2, row=1, sticky=(W, E))
        self.hand_listbox.bind('<Double-1>', lambda e: self.open_hand_description_window(self.hand_listbox.curselection()))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.opened_hands = list()

    def open_hand_description_window(self, indexes):
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
        text += card_sort(hand.hero_cards) + f' | Результат: {hand.hero_results}бб | '

        if hand.flop_exist:
            text += f'Флоп: {' '.join(hand.flop_board)}'

        self.hand_listbox.insert('end', text)


class HandDescriptionFrame(ttk.Frame):

    def __init__(self, root, hand):
        self.hand = hand
        super().__init__(root)

        self.hero_cards_visualisation()
        self.hero_position_visualisation()
        self.hero_result_visualisation()
        self.board_visualisation()

    def hero_cards_visualisation(self):
        hero_cards_text = ttk.Label(self, text="Hero cards:", font=("Arial", 14))
        cards_text = card_sort(self.hand.hero_cards).split()
        card_one_label = ttk.Label(self, text=f"{cards_text[0]}", font=("Arial", 14),
                                   foreground=card_color_choose(cards_text[0]))
        card_two_label = ttk.Label(self, text=f"{cards_text[1]}", font=("Arial", 14),
                                   foreground=card_color_choose(cards_text[1]))
        hero_cards_text.grid(column=0, row=0, sticky=(W), ipadx=5)
        card_one_label.grid(column=1, row=0, sticky=(W), ipadx=40)
        card_two_label.grid(column=1, row=0, sticky=(W), padx=30)

    def hero_position_visualisation(self):
        hero_position_text = ttk.Label(self, text="Hero position:", font=("Arial", 14))
        hero_position_label = ttk.Label(self, text=f"{self.hand.hero_position}", font=("Arial", 14))
        hero_position_text.grid(column=0, row=1, sticky=(W), ipadx=5)
        hero_position_label.grid(column=1, row=1, sticky=(W))

    def hero_result_visualisation(self):
        hero_result_text = ttk.Label(self, text="Hero result:", font=("Arial", 14))
        hero_result_label = ttk.Label(self, text=f"{self.hand.hero_results}bb", font=("Arial", 14))
        hero_result_text.grid(column=0, row=2, sticky=(W), ipadx=5)
        hero_result_label.grid(column=1, row=2, sticky=(W))

    def board_visualisation(self):
        board_text = ttk.Label(self, text="Board:", font=("Arial", 14))
        board_text.grid(column=3, row=0, sticky=(W), ipadx=10)
        if self.hand.flop_exist:
            flop_board = self.hand.flop_board
            flop_board_card_one = ttk.Label(self, text=f"{flop_board[0]}",
                                            font=("Arial", 14), foreground=card_color_choose(flop_board[0]))
            flop_board_card_one.grid(column=3, row=1, sticky=(W))
            flop_board_card_two = ttk.Label(self, text=f"{flop_board[1]}",
                                            font=("Arial", 14), foreground=card_color_choose(flop_board[1]))
            flop_board_card_two.grid(column=3, row=1)
            flop_board_card_three = ttk.Label(self, text=f"{flop_board[2]}",
                                              font=("Arial", 14), foreground=card_color_choose(flop_board[2]))
            flop_board_card_three.grid(column=3, row=1, sticky=(E))
            if self.hand.turn_exist:
                turn_card = self.hand.turn_card
                turn_card_label = ttk.Label(self, text=f"{turn_card}",
                                            font=("Arial", 14),
                                            foreground=card_color_choose(turn_card))
                turn_card_label.grid(column=4, row=1, sticky=(W))
                if self.hand.river_exist:
                    river_card = self.hand.river_card
                    river_card_label = ttk.Label(self, text=f"{turn_card}",
                                                 font=("Arial", 14),
                                                 foreground=card_color_choose(river_card))
                    river_card_label.grid(column=5, row=1, sticky=(W))


def card_sort(cards):
    alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    alph_card_idx = sorted(
        [alph_lst.index(cards[0][0]), alph_lst.index(cards[1][0])])
    if cards[0][0] == alph_lst[alph_card_idx[0]]:
        return f'{alph_lst[alph_card_idx[0]]}{cards[0][1]} {alph_lst[alph_card_idx[1]]}{cards[1][1]}'
    else:
        return f'{alph_lst[alph_card_idx[0]]}{cards[1][1]} {alph_lst[alph_card_idx[1]]}{cards[0][1]}'


def card_color_choose(card):
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
