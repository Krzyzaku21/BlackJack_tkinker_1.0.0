# %%
"""Class Deck"""
import random
from card import Card
from exceptions import (
    InvalidCardsInDeckNumbers
)


class Deck():
    """Class of Deck"""

    @classmethod
    def __repr__(cls):
        return f'{cls.card_deck}'

    @classmethod
    def create_deck(cls):
        """create parameter card_deck"""
        cls.card_deck = [Card(rank=rank, sign=sign, point=point) for rank, point in zip(
            Card.RANKS, Card.POINTS) for sign in Card.SIGNS.values()]
        if len(cls.card_deck) != 52:
            raise InvalidCardsInDeckNumbers(f'Number of cards : {len(cls.card_deck)} is not 52')
        return cls.card_deck

    @staticmethod
    def shuffle_deck(deck):
        """method shuffle deck"""
        return random.shuffle(deck)

    @classmethod
    def get_card(cls):
        """method get card from card_deck"""
        card = cls.card_deck.pop()
        return card

    @classmethod
    def len_deck(cls):
        return len(cls.card_deck)
