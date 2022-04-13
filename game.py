# %%
"""Class Game"""
from abc import ABC, abstractmethod
from typing import List
import sys
from deck import Deck
from player import Human, Dealer, Player
from game_decorator import who_deck


class AbstractGame(ABC):
    """Constructor of AbstractGame class"""

    def __init__(self):
        self.deck = None
        self.human = None
        self.dealer = None
        self.status = None

    @property
    @abstractmethod
    def deck(self):
        """abstractmethod of create deck"""

    @abstractmethod
    def options(self, dealer: Player, human: Player):
        """Check methods in blackjack"""

    @abstractmethod
    def print_cards(self, deck: List) -> str:
        """Print cards in deck"""

    @abstractmethod
    def new_game(self, human: Player, dealer: Player, deck: List) -> None:
        """create new game"""

    @abstractmethod
    def continue_game(self, human: Player, dealer: Player):
        """Create continue game"""

    @abstractmethod
    def hit(self):
        """Method HIT"""

    @abstractmethod
    def stand(self):
        """Method STAND"""

    @abstractmethod
    def double_down(self):
        """Method DOUBLE_DOWN"""

    @abstractmethod
    def split(self):
        """Method SPLIT"""

    @abstractmethod
    def insurance(self):
        """Method INSURANCE"""

    @abstractmethod
    def bet_chips(self):
        """Method create deposit game for player chips"""

    @abstractmethod
    def set_all_options_default(self):
        """Method set all options defaults"""

    @abstractmethod
    def show_cards_points(self, player: Player):
        """Method print cards styles and players points"""
    @abstractmethod
    def select_option(self):
        """Selected options from OPTIONS"""

    @abstractmethod
    def status_game(self, dealer: Player, human: Player):
        """Check human and dealer points and return status game win or draw or lose"""

    @abstractmethod
    def play(self):
        """Method start game"""

    @abstractmethod
    def dealer_moves(self):
        """Method moves dealer card get when player end draw"""


class Game(AbstractGame):
    """Class Game"""

    OPTIONS = {
        'INSURANCE': False,
        'DOUBLE_DOWN': False,
        'HIT': False,
        'STAND': False,
        'SPLIT': False,
    }

    def __init__(self):
        super().__init__()
        self.human = Human()
        self.dealer = Dealer()
        self.deck_copy = self.deck

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, value):
        value = Deck()
        value.create_deck()
        value.shuffle_deck(value.card_deck)
        self._deck = value

    def set_all_options_default(self):
        self.human.player_hand = []
        self.dealer.player_hand = []
        self.human.points = 0
        self.dealer.points = 0
        self.dealer.deposit = 0
        self.OPTIONS = self.OPTIONS.fromkeys(self.OPTIONS.keys(), False)
        if self.deck.len_deck() < 25:
            self.deck = self.deck_copy

    def options(self, dealer, human):
        if self.dealer.deposit > 0:
            if human.points < 21:
                self.OPTIONS['HIT'] = True
                self.OPTIONS['STAND'] = True
                human_rank_hand = [
                    card.rank for card in human.player_hand]
                dealer_rank_hand = [
                    card.rank for card in dealer.player_hand if card.rank is not None]
                if len(human_rank_hand) == 2:
                    if human.points == 9 and dealer.points in list(map(int, range(3, 7))) or \
                            human.points == 10 and \
                        dealer.points in list(map(int, range(2, 10))) or \
                        human.points == 11 and dealer.points in list(map(int, range(2, 11))) or \
                            all(x in human_rank_hand for x in ['A', '2']) and \
                            any(x in dealer_rank_hand for x in ['5', '6']) or \
                            all(x in human_rank_hand for x in ['A', '3']) and \
                            any(x in dealer_rank_hand for x in ['5', '6']) or \
                            all(x in human_rank_hand for x in ['A', '4']) and \
                            any(x in dealer_rank_hand for x in ['4', '5', '6']) or \
                            all(x in human_rank_hand for x in ['A', '5']) and \
                            any(x in dealer_rank_hand for x in ['4', '5', '6']) or \
                            all(x in human_rank_hand for x in ['A', '6']) and \
                            any(x in dealer_rank_hand for x in ['3', '4', '5', '6']) or \
                            all(x in human_rank_hand for x in ['A', '7']) and \
                            any(x in dealer_rank_hand for x in ['3', '4', '5', '6']) or \
                            human_rank_hand == ['5', '5']:
                        if self.human.chips >= self.dealer.deposit//2:
                            self.OPTIONS['DOUBLE_DOWN'] = True
                    elif all(x in ['A'] for x in human_rank_hand) and \
                        any(x in list(map(str, range(2, 11))) for x in dealer_rank_hand) or \
                        all(x in ['2'] for x in human_rank_hand) and \
                            any(x in list(map(str, range(2, 7))) for x in dealer_rank_hand) or \
                        all(x in ['3'] for x in human_rank_hand) and \
                            any(x in list(map(str, range(2, 7))) for x in dealer_rank_hand) or \
                        all(x in ['4'] for x in human_rank_hand) and \
                            any(x in list(map(str, range(4, 6))) for x in dealer_rank_hand) or \
                        all(x in ['6'] for x in human_rank_hand) and \
                            any(x in list(map(str, range(2, 6))) for x in dealer_rank_hand) or \
                        all(x in ['7'] for x in human_rank_hand) and \
                            any(x in list(map(str, range(2, 7))) for x in dealer_rank_hand) or \
                        all(x in ['8'] for x in human_rank_hand) and \
                            any(x in dealer_rank_hand for x in list(map(str, range(2, 9)))) or \
                        all(x in ['9'] for x in human_rank_hand) and \
                            any(x in (list(map(str, range(2, 6))) +
                                list(map(str, range(7, 9)))) for x in dealer_rank_hand):
                        self.OPTIONS['SPLIT'] = True
                    elif dealer_rank_hand[0] == 'A' and dealer.player_hand[1].rank is None:
                        self.OPTIONS['INSURANCE'] = True
            elif human.points == 21:
                print('BLACKJACK')
                self.status = 'WIN'
            else:
                self.status = 'LOSE'

    @who_deck
    def show_cards_points(self, player):
        self.print_cards(player.player_hand)
        print(f'{player.__class__.__name__} points was {player.points}')

    def select_option(self):
        your_option = None
        while your_option != 'STAND' and self.human.points < 22 and \
                your_option != 'INSURANCE' or self.human.points == 21:
            good_list = []
            for key, val in self.OPTIONS.items():
                if val is True:
                    good_list.append(key)
            if self.human.points != 21:
                print(f'Your options is {", ".join(x for x in good_list)}')
                your_option = str(input(""))
                if your_option == 'HIT':
                    self.hit()
                elif your_option == 'STAND':
                    self.stand()
                elif your_option == 'SPLIT':
                    self.split()
                    self.OPTIONS['SPLIT'] = False
                elif your_option == 'DOUBLE_DOWN':
                    self.double_down()
                    self.OPTIONS['DOUBLE_DOWN'] = False
                elif your_option == 'INSURANCE':
                    self.insurance()
                    self.OPTIONS['INSURANCE'] = False
                self.show_cards_points(self.human)
                self.show_cards_points(self.dealer)
            else:
                print('BLACKJACK')
                break
        self.status_game(self.dealer, self.human)

    def status_game(self, dealer, human):
        if human.points < 21:
            if human.points > dealer.points:
                self.status = 'WIN'
            elif human.points == dealer.points:
                self.status = 'DRAW'
            else:
                if dealer.points > 21:
                    self.status = 'WIN'
                else:
                    self.status = 'LOSE'
        elif human.points == 21:
            self.status = 'WIN'
        elif dealer.points == 21:
            self.status = 'LOSE'
        else:
            self.status = 'LOSE'

    def print_cards(self, deck):
        return [card.print_card() for card in deck]

    def new_game(self, human, dealer, deck):
        human.chips -= 100
        dealer.deposit += 100
        print('Dealer take 100 chips to deposit next game start')
        print(f'Now your coins you can bet : {human.chips} left')
        self.bet_chips()
        for _ in range(2):
            human.player_take_card(deck.get_card())
        self.show_cards_points(self.human)
        for _ in range(2):
            dealer.player_take_card(deck.get_card())
        self.show_cards_points(self.dealer)
        self.options(self.dealer, self.human)
        self.select_option()

    def continue_game(self, human, dealer):
        human.chips -= 100
        dealer.deposit += 100
        print('Dealer take 100 chips to deposit next game start')
        print(f'Now your coins you can bet : {human.chips} left')
        self.options(dealer, human)
        self.select_option()

    def play(self):
        print(f'Your coins : {self.human.chips}')
        while True:
            if self.status == 'WIN':
                print('YOU WIN')
                self.human.chips += self.dealer.deposit * 2
                self.set_all_options_default()
                self.new_game(self.human, self.dealer, self.deck)
            elif self.status == 'LOSE':
                print('YOU LOSE')
                if self.human.chips == 0 and self.dealer.deposit != 0:
                    print('YOU WANT START NEW GAME OR END')
                    decision = input('Take START or END ')
                    if decision == 'END':
                        sys.exit(0)
                    elif decision == 'START':
                        print('START NEW GAME')
                        self.human.chips = 1000
                        self.set_all_options_default()
                        self.new_game(self.human, self.dealer, self.deck)
                    else:
                        decision = input('Take START or END')
                else:
                    self.set_all_options_default()
                    self.new_game(self.human, self.dealer, self.deck)

            elif self.status == 'DRAW':
                print('YOU DRAW')
                self.human.chips += self.dealer.deposit
                self.set_all_options_default()
                self.new_game(self.human, self.dealer, self.deck)
            elif self.status is None:
                print('YOU NEW GAME')
                self.set_all_options_default()
                self.new_game(self.human, self.dealer, self.deck)
            print(f'cards in deck left: {self.deck.len_deck()}')

    def bet_chips(self):
        """Get chips from human and add it to deposit"""
        bet_options = [0, 100, 200, 500, 1000]
        choice = None
        try:
            while ((choice := int(input(f'Set one of options in '
                                        f'{", ".join(map(str,bet_options[1:]))}'
                                        f' or select 0 to stop '))) != 0):
                if choice in bet_options:
                    if self.human.chips > choice:
                        self.human.chips -= choice
                        self.dealer.deposit += choice
                        print(f'You still have {self.human.chips} and bet {choice}')
                    else:
                        print(f'you don\'t have so much chips {choice}')
                else:
                    print(f'You can\'t bet {choice} here.')
                print(f'You bet {self.dealer.deposit} chips and still have {self.human.chips}')
            print(f'You finally bet {self.dealer.deposit} coins')
        except:
            print('Bad value')
            self.bet_chips()

    def dealer_moves(self):
        if self.human.points <= 21:
            while self.dealer.points < self.human.points:
                self.dealer.player_take_card(self.deck.get_card())
        else:
            while self.dealer.points < 16:
                self.dealer.player_take_card(self.deck.get_card())

    def hit(self):
        self.human.player_take_card(self.deck.get_card())

    def stand(self):
        self.dealer_moves()

    def double_down(self):
        self.dealer.deposit = self.dealer.deposit * 2

    def split(self):
        self.human.player_hand.pop()
        self.human.player_take_card(self.deck.get_card())

    def insurance(self):
        self.dealer.player_take_card(self.deck.get_card())
        new_chips = self.dealer.deposit // 2
        self.dealer.deposit = self.dealer.deposit + new_chips
