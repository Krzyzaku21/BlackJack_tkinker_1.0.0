from tkinter import *
from PIL import Image, ImageTk
from card import Card
import os
from game import Game
from player import Dealer, Human

root = Tk()
root.title('BLACKJACK GAME')
root.attributes('-topmost', True)
root.configure(background='green')
root.state('zoomed')


class TableWindow:
    def __init__(self):
        self.game = Game()

    def take_card_url_deck(self, player):
        pack = []
        for _ in range(2):
            player.player_take_card(self.game.deck.get_card())

        print(player.player_hand)
        for card in player.player_hand:
            pack.append(self.get_link(card))
        return pack

    def get_link(self, card):
        print(card.__dict__['rank'])
        if card.__dict__['rank'] is None:
            url = os.path.join(f'./static/None_of_None.png')
        else:
            if card.sign:
                for key, value in card.SIGNS.items():
                    if value == '♣':
                        card.sign = key
                    elif value == '♠':
                        card.sign = key
                    elif card.sign == '♥':
                        card.sign = key
                    else:
                        card.sign = key
            url = os.path.join(f'./static/{card.rank}_of_{card.sign}.png')
        card_image = Image.open(url)
        card_scale = card_image.resize(((100, 200)))
        card_image = ImageTk.PhotoImage(card_scale)
        return card_image


tw = TableWindow()
human, dealer = Human(), Dealer()
h = tw.take_card_url_deck(human)
d = tw.take_card_url_deck(dealer)


def render_deck(who):
    for x in who:
        # print(x)
        frame = Frame(root, width=10, height=20, padx=5, pady=5)
        frame.pack()
        # frame.place(anchor='center', relx=0.5, rely=0.5)

        label = Label(frame, image=x)
        label.pack()


render_deck(h)
render_deck(d)
root.mainloop()
