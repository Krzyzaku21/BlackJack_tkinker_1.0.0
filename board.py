"""Class Board BlackJack in Tkinter"""
import sys
import os
import time
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from game import Game


class Panel:
    """Class Panel"""

    def __init__(self):
        self.human_card = []
        self.dealer_card = []
        self.hidden_card = None
        self.game = Game()
        self.panel_deck = self.game.deck
        self.check_len_in_deck()
        self.flag_is_bet = False

    @staticmethod
    def get_link(card):
        """Method to get card png"""
        sign = None
        if card.__dict__["rank"] is None:
            url = os.path.join("./static/None_of_None.png")
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
        """Method check length cards in deck"""
        if self.game.deck.len_deck() < 25:
            self.game.deck = self.game.deck_copy
            self.panel_deck = self.game.deck
        return self.panel_deck

    def take_card(self, player, some_deck):
        """Method take a card from game deck and create two card lists with cards images"""
        if len(player.player_hand) < 13:
            player.player_take_card(some_deck.get_card())
            if player.__class__.__name__ == "Dealer":
                self.dealer_card = [self.get_link(card) for card in player.player_hand]
            else:
                self.human_card = [self.get_link(card) for card in player.player_hand]

    def start(self):
        """Method get cards to start game"""
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


class App(tk.Tk):
    """Class App create board"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.panel = Panel()
        self.title("BLACKJACK")
        self.configure(background="green")
        menubar = MenuBar(self, self.panel)
        self.config(menu=menubar)
        self.main_widgets()
        self.app_status = None
        self.play_game()
        self.end_game_flag = False

    def default_game(self):
        """method with default options"""
        game = self.panel.game
        game.OPTIONS = game.OPTIONS.fromkeys(game.OPTIONS.keys(), False)
        self.widget_frame_options.buttons.options_button_state()

        def func():
            """function slow update default function"""
            time.sleep(3)
            if self.end_game_flag is True:
                game.set_all_options_default()
                self.panel.human_card = []
                self.panel.dealer_card = []
                self.end_game_flag = False

        self.after(1000, func)
        self.panel.check_len_in_deck()

    def continue_game(self):
        """Method continue game"""
        self.widget_frame_bet.button["state"] = "normal"
        self.panel.start()

    def start_game(self):
        """Method start game"""
        self.panel.start()
        self.widget_frame_human = HumanFrame(self, self.panel)
        self.widget_frame_dealer = DealerFrame(self, self.panel)
        self.widget_frame_human.grid(row=1, column=0)
        self.widget_frame_dealer.grid(row=4, column=0)

    def game_status(self):
        """Method check status game"""
        game = self.panel.game
        game.status_game(game.dealer, game.human)
        self.app_status = game.status
        self.widget_frame_options.buttons.widgets()
        self.widget_frame_options.buttons.options_button_state()
        self.play_game()
        self.default_game()

    def play_game(self):
        """Method default play game"""
        game = self.panel.game
        self.app_status = game.status
        if self.app_status is None:
            self.widget_frame_bet = BetFrame(self, self.panel)
            self.widget_frame_bet.grid(row=6, column=0)
            self.widget_frame_bet.bet_widget()
        if self.app_status == "LOSE":
            game.dealer.deposit = 0
            if game.human.chips == 100:
                messagebox.showinfo(
                    title="Game info",
                    message="You lose and start again",
                )
                game.human.chips = 1000
                self.play_game()
            else:
                self.continue_game()
        if self.app_status == "DRAW":
            self.continue_game()
        if self.app_status == "WIN":
            game.human.chips += game.dealer.deposit * 2
            self.continue_game()

    def main_widgets(self):
        """Method print widgets"""
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
    """Class represents board information's on live"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.panel = panel
        self.width = 50
        self.height = 2
        self.check_human_score()
        self.check_dealer_score()
        self.human_show_chips()
        self.game_show_result()
        self.dealer_show_deposit()

    def human_show_chips(self):
        """Method shows actual human chips"""
        int_var = tk.IntVar()
        chips = self.panel.game.human.chips
        int_var.set(f"Human chips: {chips - 100}")
        self.widget_score_human_chips = tk.Label(
            self,
            textvariable=int_var,
            fg="white",
            bg="grey",
            width=(self.width - 3) // 3,
            height=self.height,
        )
        self.widget_score_human_chips.grid(row=0, column=1)
        self.parent.after(1000, self.human_show_chips)

    def game_show_result(self):
        """Method shows actual game result"""
        int_var = tk.IntVar()
        result = self.panel.game.status
        int_var.set(f"{result}")
        self.widget_game_result = tk.Label(
            self,
            textvariable=int_var,
            fg="white",
            bg="red",
            width=(self.width) // 3,
            height=self.height,
        )
        self.widget_game_result.grid(row=0, column=2)
        self.parent.after(1000, self.game_show_result)

    def dealer_show_deposit(self):
        """Method show actual deposit"""
        int_var = tk.IntVar()
        deposit = self.panel.game.dealer.deposit
        int_var.set(f"Deposit: {deposit}")
        self.widget_score_dealer_deposit = tk.Label(
            self,
            textvariable=int_var,
            fg="white",
            bg="grey",
            width=(self.width - 3) // 3,
            height=self.height,
        )
        self.widget_score_dealer_deposit.grid(row=0, column=3)
        self.parent.after(1000, self.dealer_show_deposit)

    def check_human_score(self):
        """Method check human actual score"""
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
        """Method check dealer actual score"""
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
        self.widget_dealer_score.grid(row=0, column=4)
        self.parent.after(1000, self.check_dealer_score)


class MenuBar(tk.Menu):
    """ "Class of Menu"""

    def __init__(self, parent, panel):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.panel = panel

        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Start", underline=1, command=self.start)
        fileMenu.add_command(label="Exit", underline=2, command=self.quit)

    def start(self):
        """Method start menu"""
        game = self.panel.game
        self.parent.end_game_flag = True
        game.human.chips = 1000
        game.dealer.deposit = 0

        self.parent.game_status()

        def menu_deck():
            """function check deck length > 52"""
            panel_deck2 = game.deck
            if game.deck.len_deck() < 52:
                game.deck = game.deck_copy
                panel_deck2 = game.deck
            return panel_deck2

        self.panel.panel_deck = menu_deck()
        self.widget_frame_human = HumanFrame(self, self.panel)
        self.widget_frame_dealer = DealerFrame(self, self.panel)
        self.widget_frame_human.grid(row=1, column=0)
        self.widget_frame_dealer.grid(row=4, column=0)

    def quit(self):
        """Method quit menu"""
        sys.exit(0)


class CardLabel(tk.Label):
    """Class representing cards layers"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.panel = panel

    def show_card(self, box):
        """Method generating cards on table"""
        for index, x in enumerate(box):
            label = tk.Label(self, image=x, bg="green")
            label.grid(row=1, column=index)

    def remove_card(self):
        """Method removed cards from table"""
        game = Game()
        self.panel.panel_deck = game.deck
        self.panel.game.dealer.player_hand = []
        self.panel.game.human.player_hand = []
        self.panel.dealer_card = []
        self.panel.human_card = []
        self.destroy()

    def remove_human_card(self):
        """Method removed human card from table"""
        self.panel.game.human.player_hand.pop()
        self.panel.human_card.pop()
        self.show_card(self.panel.human_card)
        self.grid()

    def get_card(self, player):
        """Method get card from table"""
        self.panel.take_card(player, self.panel.panel_deck)


class HumanFrame(tk.Frame):
    """Class representing human class layer"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        """Method generating widgets"""
        self.card_label = CardLabel(self, self.panel)
        self.card_label.show_card(self.panel.human_card)
        self.card_label.grid()

    def del_human_card(self):
        """Method delete human card"""
        self.card_label.remove_human_card()
        self.panel.check_len_in_deck()

    def get_human_card(self):
        """Method get human card"""
        self.card_label.get_card(self.panel.game.human)
        self.card_label.show_card(self.panel.human_card)


class DealerFrame(tk.Frame):
    """Class representing dealer class layer"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="green")
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        """Method generating widgets"""
        self.card_label = CardLabel(self, self.panel)
        self.card_label.show_card(self.panel.dealer_card)
        self.card_label.grid()

    def del_dealer_cards(self):
        """Method delete dealer cards"""
        self.card_label.remove_card()

    def get_dealer_card(self):
        """Method get dealer card"""
        self.card_label.get_card(self.panel.game.dealer)
        self.card_label.show_card(self.panel.dealer_card)


class OptionsFrame(tk.Frame):
    """Class representing OptionsFrame"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="white")
        self.parent = parent
        self.panel = panel
        self.widgets()

    def widgets(self):
        """Method generate layers"""
        self.buttons = OptionsButtons(self, self.panel, width=80)
        self.buttons.grid(column=0, row=0)
        self.cards_left = tk.Label(self, text="CARDS LEFT", bg="yellow", width=63)
        self.cards_left.grid(column=1, row=0)
        self.options_label = tk.Label(self, bg="black", width=86)
        self.options_label.grid(column=0, rowspan=5)
        self.check_length_deck()

    def check_length_deck(self):
        """Method check length od deck in live"""
        len_int_var = tk.IntVar()
        number = self.panel.panel_deck.len_deck()
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
    """Class representing options buttons"""

    def __init__(self, parent, panel, width):
        tk.Frame.__init__(self, parent, width=width, bg="white")
        self.parent = parent
        self.panel = panel
        self.width = width

    def options(self):
        """Method run game options method"""
        game = self.panel.game
        game.options(game.dealer, game.human)

    def widgets(self):
        """method generate widgets"""
        self.options()
        widgets_width = self.width // 5
        self.button_hit = tk.Button(
            self,
            bg="red",
            text="HIT",
            width=widgets_width,
            command=self.hit,
            state="disabled",
        )
        self.button_stand = tk.Button(
            self,
            bg="red",
            text="STAND",
            width=widgets_width,
            command=self.stand,
            state="disabled",
        )
        self.button_insurance = tk.Button(
            self,
            bg="red",
            text="INSURANCE",
            width=widgets_width,
            command=self.insurance,
            state="disabled",
        )
        self.button_doubledown = tk.Button(
            self,
            bg="red",
            text="DOUBLE_DOWN",
            width=widgets_width,
            command=self.double_down,
            state="disabled",
        )
        self.button_split = tk.Button(
            self,
            bg="red",
            text="SPLIT",
            width=widgets_width,
            command=self.split,
            state="disabled",
        )
        self.button_hit.grid(column=0, row=0)
        self.button_stand.grid(column=1, row=0)
        self.button_insurance.grid(column=2, row=0)
        self.button_doubledown.grid(column=3, row=0)
        self.button_split.grid(column=4, row=0)

    def options_button_state(self):
        """Method check buttons state"""
        game = self.panel.game
        for key, value in game.OPTIONS.items():
            if key == "HIT":
                if value is True:
                    self.button_hit["state"] = "normal"
                else:
                    self.button_hit["state"] = "disabled"
            if key == "STAND":
                if value is True:
                    self.button_stand["state"] = "normal"
                else:
                    self.button_stand["state"] = "disabled"

            if key == "INSURANCE":
                if value is True:
                    self.button_insurance["state"] = "normal"
                else:
                    self.button_insurance["state"] = "disabled"
            if key == "DOUBLE_DOWN":
                if value is True:
                    self.button_doubledown["state"] = "normal"
                else:
                    self.button_doubledown["state"] = "disabled"
            if key == "SPLIT":
                if value is True:
                    self.button_split["state"] = "normal"
                else:
                    self.button_split["state"] = "disabled"

    def hit(self):
        """Method hit on table"""
        parent = self.parent.parent.widget_frame_human
        parent.get_human_card()
        if self.panel.game.human.points >= 21:
            self.stand()

    def stand(self):
        """Method stand on table"""
        self.parent.parent.end_game_flag = True
        parent = self.parent.parent.widget_frame_dealer
        if self.panel.game.human.points < 21:
            while self.panel.game.dealer.points < self.panel.game.human.points:
                parent.get_dealer_card()
        self.parent.parent.game_status()

    def insurance(self):
        """Method insurance on table"""
        game = self.panel.game
        parent = self.parent.parent.widget_frame_dealer
        parent.get_dealer_card()
        new_chips = game.dealer.deposit // 2
        game.dealer.deposit = game.dealer.deposit + new_chips
        self.button_insurance["state"] = "disabled"
        self.parent.parent.end_game_flag = True
        self.parent.parent.game_status()

    def double_down(self):
        """Method double_down on table"""
        game = self.panel.game
        game.dealer.deposit = game.dealer.deposit * 2
        self.button_doubledown["state"] = "disabled"
        if self.panel.game.human.points >= 21:
            self.stand()

    def split(self):
        """Method split on table"""
        parent = self.parent.parent.widget_frame_human
        parent.del_human_card()
        parent.get_human_card()
        self.button_split["state"] = "disabled"
        self.parent.parent.end_game_flag = True
        self.parent.parent.game_status()


class BetFrame(tk.Frame):
    """Class representing bet methods"""

    def __init__(self, parent, panel):
        tk.Frame.__init__(self, parent, bg="gray")
        self.parent = parent
        self.panel = panel
        self.start_flag = True

    def bet_widget(self):
        """Method get coins from human"""
        game = self.panel.game
        coins_int_var = tk.IntVar()
        message_string_var = tk.StringVar()
        bet_options = [0, 100, 200, 500, 1000]

        def change():
            """function to change chips on live"""
            coins = tk.Entry(
                self, textvariable=coins_int_var, fg="black", bg="white", width=50
            )
            coins_get = coins_int_var.get()
            if game.human.chips >= 0:
                if coins_get in bet_options:
                    if coins_get == 0:
                        if self.start_flag == False:
                            messagebox.showinfo(
                                title="Chips info",
                                message="First you need bet some coins",
                            )
                        else:
                            self.start_flag = False
                    else:

                        if game.human.chips > coins_get:
                            game.human.chips -= coins_get
                            game.dealer.deposit += coins_get
                            if coins_get == 0:
                                self.button_flag = True
                            if game.human.chips == 100:
                                message_string_var.set(
                                    f"You can't bet more chips {game.dealer.deposit}, bet over"
                                )
                            else:
                                message_string_var.set(
                                    f"You bet {game.dealer.deposit} chips "
                                    + "\n"
                                    + f"and still have {game.human.chips}"
                                )
                else:
                    element = ", ".join(str(x) for x in bet_options[1:])
                    chips = game.human.chips
                    message_string_var.set(
                        f"You can't bet {coins_get} here, you can only bet {element}"
                        + "\n"
                        + f"You bet {game.dealer.deposit} chips and still have {chips -100}",
                    )
            message = tk.Label(
                self, textvariable=message_string_var, width=50, bg="gray"
            )
            return coins, message

        def change_bet_button():
            """function to accept game status"""
            if self.panel.game.dealer.deposit != 0:
                self.button["state"] = "disable"
                self.parent.start_game()
                self.parent.widget_frame_options.buttons.widgets()
                self.parent.widget_frame_options.buttons.options_button_state()

        self.button = tk.Button(self, command=change, bg="yellow", text="BET", width=24)
        self.button2 = tk.Button(
            self, command=change_bet_button, bg="red", text="START", width=24
        )
        self.coin, self.message = change()
        self.methods_bet()

    def create_bet(self):
        """method create bet layers"""

        self.message.grid(column=0, row=0)
        self.coin.grid(column=1, row=0, sticky=tk.W, padx=20)
        self.button.grid(column=2, row=0)
        self.button2.grid(column=3, row=0)

    def methods_bet(self):
        """ "method after create layers"""
        game = self.panel.game
        if game.dealer.deposit == 0:
            self.create_bet()
        self.parent.after(1000, self.methods_bet)


def main():
    """function executed code"""
    app = App(None)
    app.mainloop()


if __name__ == "__main__":
    main()
