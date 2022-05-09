from deck import Deck
from card import Card
import pytest
from exceptions import InvalidCardsInDeckNumbers


def test_deck_have_52_cards():
    deck = Deck()
    deck.create_deck()
    assert len(deck.card_deck) == 52


def test_sign_from_deck():
    deck = Deck()
    deck.create_deck()
    # cards_signs = ["".join(item.sign for item in card) for card in deck.card_deck]
    # cards_heart = list(filter(lambda symbol: symbol == '♥', cards_signs))
    cards_signs = [card.sign for card in deck.card_deck]
    cards_heart = list(filter(lambda symbol: symbol == "♥", cards_signs))
    assert "♥" in cards_heart
    assert len(cards_heart) == 13


def test_shuffle_deck():
    deck = Deck()
    deck.create_deck()
    new_deck = deck.card_deck[:]
    deck.shuffle_deck(new_deck)
    assert new_deck != deck.card_deck


def test_get_card():
    deck = Deck()
    deck.create_deck()
    test_deck_card = deck.get_card()
    assert len(deck.card_deck) == 51
    assert test_deck_card not in deck.card_deck


def test_invalid_deck_in_create():
    with pytest.raises(InvalidCardsInDeckNumbers) as message:
        Card.SIGNS = {
            "spades": "♠",
            "hearts": "♥",
            "diamonds": "♦",
        }
        deck = Deck()
        deck.create_deck()
        assert message == f"Number of cards : {len(deck.card_deck)} is not 52"
