import Hand as hd
import Hand_matrix as hdm
import Statistics_upd as stat
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from accessify import private, protected


class MainWindow:

    def __init__(self):

        self.alph_lst = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

        self.inf_lst = list()
        self.hand_lst = list()
        self.opened_hands = list()

        self.root = Tk()
        self.root.title("Main")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)

        self.__hand_listbox_init()
        self.__menu_init()

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.root.mainloop()

    @protected
    def __hand_listbox_init(self):
        self.list_box = Listbox(self.root, height=30, width=50)
        self.list_box.grid(column=0, row=0, sticky=(N, W, E, S))
        self.scroll_bar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.list_box.yview)
        self.scroll_bar.grid(column=1, row=0, sticky=(N, S))
        self.list_box['yscrollcommand'] = self.scroll_bar.set
        ttk.Label(self.root, text="Список раздач", anchor=(W)).grid(column=0, columnspan=2, row=1, sticky=(W, E))
        self.list_box.bind('<Double-1>', lambda e: self.__hand_description_window_open(self.list_box.curselection()))

    @protected
    def __menu_init(self):
        self.menubar = Menu(self.root)
        self.root['menu'] = self.menubar
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='Файл')
        self.menu_file.add_command(label='Импортировать раздачи', command=self.__hand_import)

    def __add_hand_to_listbox(self, hand):

        text = str()
        text += self.card_sort(hand.hero_cards) +f' | Результат: {hand.hero_results}бб | '

        if hand.flop_exist:
            text += f'Флоп: {' '.join(hand.flop_board)}'

        self.list_box.insert('end', text)

    def __hand_import(self):
        hand_lst = list()
        direct = filedialog.askdirectory()
        lst_f = os.listdir(direct)
        for f in lst_f:
            with open(f"{direct}/{f}", 'r') as hand_info:
                inf = hand_info.read().split("\n\n\n")

            for hand_inf in inf:
                if hd.data_can_be_processed(hand_inf):
                    hand = hd.Hand(hand_inf)
                    self.hand_lst.append(hand)
                    self.__add_hand_to_listbox(hand)

    def __hand_description_window_open(self, indexes):
        if indexes[0] not in self.opened_hands:
            self.opened_hands.append(indexes[0])
            win = Toplevel(self.root)
            winframe = ttk.Frame(win, padding="3 3 12 12")
            winframe.grid(column=0, row=0)
            win.protocol("WM_DELETE_WINDOW", lambda: self.__hand_description_window_destroy(indexes[0], win))
            hero_cards_text = ttk.Label(win, text="Hero cards:", font=("Arial", 14))
            hero_position_text = ttk.Label(win, text="Hero position:", font=("Arial", 14))
            hero_result_text = ttk.Label(win, text="Hero result:", font=("Arial", 14))

            cards_text = self.card_sort(self.hand_lst[indexes[0]].hero_cards).split()
            card_one_label = ttk.Label(win, text=f"{cards_text[0]}", font=("Arial", 14),
                                       foreground=self.card_color_choose(cards_text[0]))
            card_two_label = ttk.Label(win, text=f"{cards_text[1]}", font=("Arial", 14),
                                       foreground=self.card_color_choose(cards_text[1]))
            hero_position_label = ttk.Label(win, text=f"{self.hand_lst[indexes[0]].hero_position}", font=("Arial", 14))
            hero_result_label = ttk.Label(win, text=f"{self.hand_lst[indexes[0]].hero_results}bb", font=("Arial", 14))
            board_text = ttk.Label(win, text="Board:", font=("Arial", 14))

            hero_cards_text.grid(column=0, row=0, sticky=(W), ipadx=5)
            card_one_label.grid(column=1, row=0, sticky=(W), ipadx=40)
            card_two_label.grid(column=1, row=0, sticky=(W), padx=25)
            hero_position_text.grid(column=0, row=1, sticky=(W), ipadx=5)
            hero_position_label.grid(column=1, row=1, sticky=(W))
            hero_result_text.grid(column=0, row=2, sticky=(W), ipadx=5)
            hero_result_label.grid(column=1, row=2, sticky=(W))
            board_text.grid(column=3, row=0, sticky=(W), ipadx=10)
            if self.hand_lst[indexes[0]].flop_exist:
                flop_board = self.hand_lst[indexes[0]].flop_board
                flop_board_card_one = ttk.Label(win, text=f"{flop_board[0]}",
                                                font=("Arial", 14), foreground=self.card_color_choose(flop_board[0]))
                flop_board_card_one.grid(column=3, row=1, sticky=(W))
                flop_board_card_two = ttk.Label(win, text=f"{flop_board[1]}",
                                                font=("Arial", 14), foreground=self.card_color_choose(flop_board[1]))
                flop_board_card_two.grid(column=3, row=1)
                flop_board_card_three = ttk.Label(win, text=f"{flop_board[2]}",
                                                font=("Arial", 14), foreground=self.card_color_choose(flop_board[2]))
                flop_board_card_three.grid(column=3, row=1, sticky=(E))
                if self.hand_lst[indexes[0]].turn_exist:
                    turn_card = self.hand_lst[indexes[0]].turn_card
                    turn_card_label = ttk.Label(win, text=f"{turn_card}",
                                                    font=("Arial", 14),
                                                    foreground=self.card_color_choose(turn_card))
                    turn_card_label.grid(column=4, row=1, sticky=(W))
                    if self.hand_lst[indexes[0]].river_exist:
                        river_card = self.hand_lst[indexes[0]].river_card
                        river_card_label = ttk.Label(win, text=f"{turn_card}",
                                                        font=("Arial", 14),
                                                        foreground=self.card_color_choose(river_card))
                        river_card_label.grid(column=5, row=1, sticky=(W))

    def __hand_description_window_destroy(self, index, win):
        self.opened_hands.pop(self.opened_hands.index(index))
        win.destroy()

    def card_sort(self, cards):
        alph_card_idx = sorted(
            [self.alph_lst.index(cards[0][0]), self.alph_lst.index(cards[1][0])])
        if cards[0][0] == self.alph_lst[alph_card_idx[0]]:
            return f'{self.alph_lst[alph_card_idx[0]]}{cards[0][1]} {self.alph_lst[alph_card_idx[1]]}{cards[1][1]}'
        else:
            return f'{self.alph_lst[alph_card_idx[0]]}{cards[1][1]} {self.alph_lst[alph_card_idx[1]]}{cards[0][1]}'

    @staticmethod
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
    MainWindow()
