from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import sys
from game import Game
import os
import datetime


class Panel:
    def __init__(self):
        self.human_card = []
        self.dealer_card = []
        self.hidden_card = None
        self.game = Game()
        self.panel_deck = self.game.deck

    def get_link(self, card):
        sign = None
        if card.__dict__["rank"] is None:
            url = os.path.join(f"./static/None_of_None.png")
        else:
            if card.sign == "♣":
                sign = "clubs"
            elif card.sign == "♠":
                sign = "spades"
            elif card.sign == "♥":
                sign = "hearts"
            else:
                sign = "diamonds"
        url = os.path.join(f"./static/{card.rank}_of_{sign}.png")
        card_image = Image.open(url)
        card_scale = card_image.resize(((75, 125)))
        card_image = ImageTk.PhotoImage(card_scale)
        return card_image

    def check_len_in_deck(self):
        if self.game.deck.len_deck() < 25:
            self.game.deck = self.game.deck_copy
            self.panel_deck = self.game.deck
        # card_len = self.panel_deck.len_deck()
        # print('card len', card_len)
        # print(self.game.deck)
        return self.panel_deck

    def take_card(self, player, deck):
        if len(player.player_hand) < 13:
            player.player_take_card(deck.get_card())
            if player.__class__.__name__ == "Dealer":
                self.dealer_card = [self.get_link(card) for card in player.player_hand]
            else:
                self.human_card = [self.get_link(card) for card in player.player_hand]

    def start(self):
        if (
            len(self.game.dealer.player_hand) < 2
            and len(self.game.human.player_hand) < 2
            and len(self.dealer_card) < 2
            and len(self.human_card) < 2
        ):
            self.take_card(self.game.dealer, self.panel_deck)
            self.take_card(self.game.dealer, self.panel_deck)
            self.take_card(self.game.human, self.panel_deck)
            self.take_card(self.game.human, self.panel_deck)

        print(len(self.game.dealer.player_hand))
        print(len(self.game.human.player_hand))
        print(len(self.dealer_card))
        print(len(self.human_card))


class DefaultFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)


class App(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.panel = Panel()
        self.title("BLACKJACK")
        self.configure(background="green")
        menubar = MenuBar(self, self.panel)
        self.config(menu=menubar)
        self.main_widgets()

    def start(self):
        self.panel.start()
        self.widget_frame_human = HumanFrame(self, self.panel)
        self.widget_frame_dealer = DealerFrame(self, self.panel)
        self.widget_frame_human.grid(row=1, column=0)
        self.widget_frame_dealer.grid(row=4, column=0)
        self.widget_frame_bet = BetFrame(self, self.panel)
        self.widget_frame_bet.grid(row=6, column=0)
        self.widget_frame_bet.bet_widget()
        # self.play()

    def check_blackjack_status(self):
        game = self.panel.game
        if game.dealer.deposit < 0:
            messagebox.showinfo("First you need bet some coins")
        else:
            self.widget_frame_bet.destroy()

    def play(self):
        pass

    def main_widgets(self):
        game = self.panel.game
        self.widget_title_human = tk.Label(
            self, text=f"{game.human.__class__.__name__}", bg="white", width=150
        )
        self.widget_title_human.grid(row=0, column=0)
        self.widget_score = GameScore(self, self.panel)
        self.widget_score.grid(row=2, column=0)
        self.widget_title_dealer = tk.Label(
            self, text=f"{game.dealer.__class__.__name__}", bg="white", width=150
        )
        self.widget_title_dealer.grid(row=3, column=0)
        self.widget_frame_options = OptionsFrame(self, self.panel)
        self.widget_frame_options.grid(row=5, column=0)


class GameScore(tk.Frame):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.panel = panel
        self.width = 50
        self.height = 2
        self.check_human_score()
        self.check_dealer_score()

        self.widget_scored = tk.Label(
            self,
            text="score",
            fg="white",
            bg="black",
            width=self.width - 1,
            height=self.height,
        )
        self.widget_scored.grid(row=0, column=1)

    def check_human_score(self):
        int_var = tk.IntVar()
        number = self.panel.game.human.points
        int_var.set(f"Human points: {number}")
        self.widget_human_score = tk.Label(
            self,
            textvariable=int_var,
            fg="white",
            bg="black",
            width=self.width,
            height=self.height,
        )
        self.widget_human_score.grid(row=0, column=0)
        self.parent.after(1000, self.check_human_score)

    def check_dealer_score(self):
        int_var = tk.IntVar()
        number = self.panel.game.dealer.points
        int_var.set(f"Dealer points: {number}")
        self.widget_dealer_score = tk.Label(
            self,
            textvariable=int_var,
            fg="white",
            bg="black",
            width=self.width,
            height=self.height,
        )
        self.widget_dealer_score.grid(row=0, column=2)
        self.parent.after(1000, self.check_dealer_score)


class MenuBar(tk.Menu):
    def __init__(self, parent, panel):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.panel = panel

        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Start", underline=1, command=self.start)
        fileMenu.add_command(label="Exit", underline=2, command=self.quit)

    def start(self):
        # print(self.panel.panel_deck)
        # print(self.panel.panel_deck.len_deck())
        # self.panel.start()
        self.parent.start()
        # print(self.panel.game.dealer.player_hand)
        # print(self.panel.game.human.player_hand)
        # print(self.panel.dealer_card)
        # print(self.panel.human_card)

    def quit(self):
        sys.exit(0)


class CardLabel(tk.Label):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.panel = panel

    def show_card(self, box):
        for index, x in enumerate(box):
            label = tk.Label(self, image=x)
            label.grid(row=1, column=index)

    def remove_card(self):
        game = Game()
        self.panel.panel_deck = game.deck
        self.panel.game.dealer.player_hand = []
        self.panel.game.human.player_hand = []
        self.panel.dealer_card = []
        self.panel.human_card = []
        self.destroy()

    def remove_human_card(self):
        self.panel.game.human.player_hand.pop()
        self.panel.human_card.pop()
        self.show_card(self.panel.human_card)
        self.grid()

    def get_card(self, player):
        self.panel.take_card(player, self.panel.panel_deck)


class HumanFrame(tk.Frame):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        button = tk.Button(self, text="add", command=self.get_human_card)
        button.grid(column=0, row=1)
        button = tk.Button(self, text="del", command=self.del_human_cards)
        button.grid(column=1, row=1)
        self.card_label = CardLabel(self, self.panel)
        self.card_label.show_card(self.panel.human_card)
        self.card_label.grid()

    def del_human_cards(self):
        self.card_label.remove_human_card()
        self.panel.check_len_in_deck()

    def get_human_card(self):
        self.card_label.get_card(self.panel.game.human)
        self.card_label.show_card(self.panel.human_card)
        print(self.panel.game.human.points)


class DealerFrame(tk.Frame):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        button = tk.Button(self, text="del", command=self.del_dealer_cards)
        button.grid(column=0, row=1)
        button = tk.Button(self, text="add", command=self.get_dealer_card)
        button.grid(column=1, row=1)
        self.card_label = CardLabel(self, self.panel)
        self.card_label.show_card(self.panel.dealer_card)
        self.card_label.grid()

    def del_dealer_cards(self):
        self.card_label.remove_card()

    def get_dealer_card(self):
        self.card_label.get_card(self.panel.game.dealer)
        self.card_label.show_card(self.panel.dealer_card)
        print(self.panel.game.dealer.points)


class OptionsFrame(tk.Frame):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        buttons = OptionsButtons(self, self.panel, width=80)
        buttons.grid(column=0, row=0)
        cards_left = tk.Label(self, text="CARDS LEFT", bg="yellow", width=63)
        cards_left.grid(column=1, row=0)
        options_label = tk.Label(self, bg="black", width=86)
        options_label.grid(column=0, rowspan=5)
        self.check_length_deck()

    def check_length_deck(self):
        len_int_var = tk.IntVar()
        number = self.panel.game.deck.len_deck()
        if number != 52:
            len_int_var.set(number)
            cards_left = tk.Label(
                self,
                textvariable=len_int_var,
                bg="black",
                width=63,
                fg="white",
            )
            cards_left.grid(column=1, row=1)
        self.parent.after(1000, self.check_length_deck)


class OptionsButtons(tk.Button):
    def __init__(self, parent, panel, width):
        tk.Frame.__init__(self, parent, bg="pink", width=width)
        self.parent = parent
        self.panel = panel
        self.width = width
        self.widgets()

    def options(self):
        game = self.panel.game
        # game.dealer.deposit = 100
        game.options(game.dealer, game.human)
        print(game.OPTIONS)

    def widgets(self):
        widgets_width = self.width // 5
        button_hit = tk.Button(
            self, bg="red", text="HIT", width=widgets_width, command=self.options
        )
        button_hit.grid(column=0, row=0)
        button_stand = tk.Button(self, bg="red", text="STAND", width=widgets_width)
        button_stand.grid(column=1, row=0)
        button_insurance = tk.Button(
            self, bg="red", text="INSURANCE", width=widgets_width
        )
        button_insurance.grid(column=2, row=0)
        button_doubledown = tk.Button(
            self, bg="red", text="DOUBLE_DOWN", width=widgets_width
        )
        button_doubledown.grid(column=3, row=0)
        button_split = tk.Button(self, bg="red", text="SPLIT", width=widgets_width)
        button_split.grid(column=4, row=0)


class BetFrame(tk.Frame):
    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="gray")
        self.parent = parent
        self.panel = panel
        # self.bet_widget()

    def bet_widget(self):
        game = self.panel.game
        coins_int_var = tk.IntVar()
        message_string_var = tk.StringVar()
        bet_options = [0, 100, 200, 500, 1000]

        def change():
            coins = tk.Entry(
                self, textvariable=coins_int_var, fg="black", bg="white", width=50
            )
            coins_get = coins_int_var.get()
            if game.human.chips >= 100:
                if coins_get in bet_options:
                    if game.human.chips > coins_get:
                        game.human.chips -= coins_get
                        game.dealer.deposit += coins_get
                        if game.human.chips == 100:
                            message_string_var.set(
                                f"You can't bet more chips {game.dealer.deposit}, bet over"
                            )
                        else:
                            message_string_var.set(
                                f"You bet {game.dealer.deposit} chips and still have {game.human.chips}"
                            )
                else:
                    elements = "".join(
                        filter(lambda x: x not in bet_options, bet_options)
                    )
                    message_string_var.set(
                        f"You can't bet {coins_get} here, you can only bet {elements}\nYou bet {game.dealer.deposit} chips and still have {game.human.chips}"
                    )
            message_get = message_string_var.get()
            message = tk.Label(
                self, textvariable=message_string_var, width=50, bg="gray"
            )
            print(coins_get)
            print(message_get)
            return coins, message

        button = tk.Button(self, command=change, bg="yellow", text="BET", width=50)
        coin, message = change()
        message.grid(column=0, row=0)
        coin.grid(column=1, row=0, sticky=tk.W, padx=20)
        button.grid(column=2, row=0)


def main():
    app = App(None)
    app.mainloop()


if __name__ == "__main__":
    main()
