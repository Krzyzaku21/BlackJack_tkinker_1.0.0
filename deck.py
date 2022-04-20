# %%
"""Class Deck"""
from abc import ABC, abstractmethod
from typing import List
import random
from card import Card
from exceptions import (
    InvalidCardsInDeckNumbers
)


class AbstractDeck(ABC):
    """Abstract Class Deck"""

    @abstractmethod
    def __repr__(self):
        """Represents card deck"""
    @abstractmethod
    def create_deck(self) -> List:
        """Create deck from cards"""
    @abstractmethod
    def get_card(self) -> Card:
        """Method to get card from deck"""
    @abstractmethod
    def len_deck(self) -> int:
        """Method return actual length deck"""


class Deck(AbstractDeck):
    """Class of Deck"""
    card_deck = []

    def __repr__(self):
        return f'{self.card_deck}'

    def create_deck(self):
        self.card_deck = [Card(rank=rank, sign=sign, point=point) for rank, point in zip(
            Card.RANKS, Card.POINTS) for sign in Card.SIGNS.values()]
        if len(self.card_deck) != 52:
            raise InvalidCardsInDeckNumbers(f'Number of cards : {len(self.card_deck)} is not 52')
        return self.card_deck

    @staticmethod
    def shuffle_deck(deck):
        """method shuffle deck"""
        return random.shuffle(deck)

    def get_card(self):
        card = self.card_deck.pop()
        return card

    def len_deck(self):
        return len(self.card_deck)
