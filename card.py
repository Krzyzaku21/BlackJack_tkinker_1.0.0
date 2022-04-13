# %%
"""class Card"""
from abc import ABC, abstractmethod
from exceptions import (
    InvalidCardPoint,
    InvalidCardSign,
    InvalidCardRank
)
import colorama
COLORS = {
    'red': colorama.Fore.RED,
    'black': colorama.Fore.BLACK,
    'white': colorama.Back.WHITE,
    'green': colorama.Back.GREEN,
}


class AbstractCard(ABC):
    """Default card creator"""

    @abstractmethod
    def __init__(self, rank: str, sign: str, point: int) -> None:
        self.rank = self.rank_options(rank)
        self.sign = self.sign_options(sign)
        self.point = self.point_options(point)
        """
        Constructor
        Args:
            rank (str): func card_rank return rank
            sign (str): func card_sign return sign
            point (int): func card_point return point
        """
    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation"""

    @abstractmethod
    def print_card(self) -> str:
        """Printed card"""

    @abstractmethod
    def rank_options(self, value: str) -> str:
        """Check rank is valid"""

    @abstractmethod
    def sign_options(self, value: str) -> str:
        """Check sign is valid"""

    @abstractmethod
    def point_options(self, value: int) -> int:
        """Check point is valid"""


class Card(AbstractCard):
    """Card class"""
    RANKS = [*[str(i) for i in range(2, 11)], 'J', 'Q', 'K', 'A']
    POINTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    SIGNS = {
        'clubs': '♣',
        'spades': '♠',
        'hearts': '♥',
        'diamonds': '♦',
    }

    def __init__(self, rank=None, sign=None, point=None):
        super().__init__(rank, sign, point)

    def __repr__(self) -> str:
        return f"({self.rank}{self.sign}, point={self.point})"

    def rank_options(self, value):
        if value not in Card.RANKS and value is not None:
            raise InvalidCardRank(f'Invalid {value} not in {", ".join(map(str, Card.RANKS))}')
        return value

    def sign_options(self, value):
        if value not in Card.SIGNS.values() and value is not None:
            raise InvalidCardSign(f'Invalid {value} not in \
                {", ".join(list(x for x in Card.SIGNS.values()))}')
        return value

    def point_options(self, value):
        if value not in Card.POINTS and value is not None and value != 1:
            raise InvalidCardPoint(f'Invalid {value} not in {", ".join(map(str, Card.POINTS))}')
        return value

    @staticmethod
    def card_logo(item, rank, sign):
        """Print card sharp"""
        element_in_list = [
            '┌───────┐',
            f'| {rank}     |',
            '|       |',
            f'|   {sign}   |',
            '|       |',
            f'|    {rank}  |',
            '└───────┘'
        ]
        colorama.init(autoreset=True)
        for elem in element_in_list:
            print(item + elem)

    def print_card(self) -> str:
        rank, sign = self.rank, self.sign
        # fully = ""
        if self.sign in ('♦', '♥'):
            pass
            fully = COLORS["red"] + COLORS["white"]
        elif self.sign in ('♣', '♠'):
            pass
            fully = COLORS["black"] + COLORS["white"]
        else:
            fully = COLORS["white"] + COLORS["green"]
            rank, sign = 'X', 'X'
        return self.card_logo(fully, rank, sign)
