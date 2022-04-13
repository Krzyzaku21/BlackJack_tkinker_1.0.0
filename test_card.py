# %%
# python -m pytest -v -s test_card.py
"""Test class Card"""
import pytest
from card import Card
from exceptions import (
    InvalidCardPoint,
    InvalidCardSign,
    InvalidCardRank
)


def test_one_card():
    """Test class one card"""
    card = Card('2', '♣', 2)
    assert card.rank == '2'
    assert card.sign == '♣'
    assert card.point == 2


def test_invalid_rank():
    """Test invalid rank"""
    with pytest.raises(InvalidCardRank) as message:
        Card('1')
        assert message == "Invalid card rank"


def test_invalid_sign():
    """Test invalid sign"""
    with pytest.raises(InvalidCardSign) as message:
        Card('2', 'XXXX')
        assert message == "Invalid card sign"


def test_invalid_point():
    """Test invalid point"""
    with pytest.raises(InvalidCardPoint) as message:
        Card('2', '♣', 33)
        assert message == "Invalid card point"


def test_repr_card():
    """Test repr card"""
    card = Card('2', '♣', 2)
    assert repr(f'rank={card.rank}, sign={card.sign}, point={card.point}')

# %%
