# python -m pytest -s -v test_game.py
"""Test Class Game"""
from game import Game
from card import Card


def test_deck_property():
    """test deck property"""
    game = Game()
    game.deck = ['Check property']
    assert game.deck != ['Check property']


def test_set_all_options_default():
    """test functions reset deck cards"""
    game = Game()
    for _ in range(30):
        game.human.player_take_card(game.deck.get_card())
    assert game.deck.len_deck() == 22
    game.set_all_options_default()
    assert game.deck.len_deck() == 52


def test_options_double_down():
    "functions test double down active"

    game = Game()
    game.dealer.deposit = 100
    game.human.player_take_card(Card(rank='A', sign='♣', point=11))
    game.human.player_take_card(Card(rank='2', sign='♠', point=2))
    game.dealer.player_take_card(Card(rank='5', sign='♠', point=5))
    game.options(game.dealer, game.human)
    assert game.OPTIONS['DOUBLE_DOWN'] is True


def test_options_split():
    "functions test split active"
    game = Game()
    game.dealer.deposit = 100
    game.human.player_take_card(Card(rank='A', sign='♣', point=11))
    game.human.player_take_card(Card(rank='A', sign='♠', point=11))
    game.dealer.player_take_card(Card(rank='2', sign='♠', point=2))
    game.options(game.dealer, game.human)
    assert game.OPTIONS['SPLIT'] is True


def test_options_insurance():
    "functions test insurance active"
    game = Game()
    game.dealer.deposit = 100
    game.human.player_take_card(Card(rank='5', sign='♣', point=5))
    game.human.player_take_card(Card(rank='6', sign='♠', point=6))
    game.dealer.player_take_card(Card(rank='A', sign='♠', point=11))
    game.dealer.player_take_card(Card())
    game.options(game.dealer, game.human)
    assert game.OPTIONS['INSURANCE'] is True


def test_status_game():
    """function test status_game"""
    game = Game()
    game.human.points = 21
    game.status_game(game.dealer, game.human)
    assert game.status is 'WIN'
    game.human.points = 25
    game.status_game(game.dealer, game.human)
    assert game.status is 'LOSE'
    game.dealer.points = 21
    game.status_game(game.dealer, game.human)
    assert game.status is 'LOSE'
    game.human.points = 20
    game.dealer.points = 19
    game.status_game(game.dealer, game.human)
    assert game.status is 'WIN'
    game.human.points = 18
    game.dealer.points = 20
    game.status_game(game.dealer, game.human)
    assert game.status is 'LOSE'
    game.human.points = 17
    game.dealer.points = 17
    game.status_game(game.dealer, game.human)
    assert game.status is 'DRAW'


def test_dealer_moves():
    """function test_dealer_moves"""
    game = Game()
    game.human.points = 19
    game.dealer.points = 18
    game.dealer_moves()
    assert game.human.points < game.dealer.points
