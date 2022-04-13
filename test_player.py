from player import Human, Dealer, Player
from card import Card


def test_one_ace():
    card = Card(rank='A', sign='♣', point=11)
    card2 = Card(rank='2', sign='♣', point=2)
    player = Player()
    player.player_take_card(card)
    player.player_take_card(card2)
    assert player.points == 13


def test_two_aces():
    card = Card(rank='A', sign='♣', point=11)
    card2 = Card(rank='A', sign='♠', point=11)
    player = Player()
    player.player_take_card(card)
    player.player_take_card(card2)
    assert player.points == 12


def test_more_than_two_aces():
    card = Card(rank='A', sign='♣', point=11)
    card2 = Card(rank='A', sign='♠', point=11)
    card3 = Card(rank='A', sign='♠', point=11)
    player = Player()
    player.player_take_card(card)
    player.player_take_card(card2)
    player.player_take_card(card3)
    assert player.points == 13
