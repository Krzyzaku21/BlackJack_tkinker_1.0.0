# %%
"""Class players"""
from deck import Deck
from abc import ABC, abstractmethod
from typing import List
from card import Card


class AbstractPlayer(ABC):
    """Abstract class player"""

    def __init__(self):
        """Constructor class AbstractPlayer"""
        self.player_hand = []
        self.points = 0

    @abstractmethod
    def player_take_card(self, card: Card) -> List:
        """Take a card"""

    @abstractmethod
    def player_points(self) -> int:
        """Return the number of points in deck"""


class Player(AbstractPlayer):
    """Class player"""

    def player_take_card(self, card: Card):
        self.player_hand.append(card)
        self.points = self.player_points()
        return self.player_hand

    def player_points(self):
        points = 0
        hand = self.player_hand[:]
        if hand[-1].point is None:
            hand[-1].point = 0
        hand.sort(key=lambda x: x.point)
        while sum(x.point for x in hand) > 21:
            if hand[-1].point != 11:
                break
            if hand[-1].point == 11:
                hand[-1].point = 1
            else:
                hand.sort(key=lambda x: x.point)
        points = sum(x.point for x in hand)
        return points


class Dealer(Player):
    """Constructor class Dealer"""

    def __init__(self):
        super().__init__()
        self.hidden_card = None
        self.deposit = 0

    def player_take_card(self, card: Card):
        if len(self.player_hand) == 1:
            self.hidden_card = card
            card = Card()
        elif len(self.player_hand) == 2:
            if self.player_hand[-1].rank is None:
                self.player_hand.pop()
                self.player_hand.append(self.hidden_card)
        return super().player_take_card(card)


class Human(Player):
    """Constructor class Human"""

    def __init__(self):
        super().__init__()
        self.chips = 1000
