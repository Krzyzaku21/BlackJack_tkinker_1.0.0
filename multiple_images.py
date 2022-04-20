from tkinter import *
from PIL import Image, ImageTk
from card import Card
import os
from deck import Deck
from game import Game
from player import Dealer, Human

root = Tk()
root.title('BLACKJACK GAME')
root.attributes('-topmost', True)
root.configure(background='green')
root.state('zoomed')


class TableWindow:

    def __init__(self, master):
        self.master = master
        self.human = Human()
        self.dealer = Dealer()
        self.box = []
        self.table = []
        self.frame = Frame(master)
        self.frame.grid()

        self.start_button = Button(master, text="Start Game", command=self.start_game)
        self.start_button.grid()

        self.button = Button(master, text="Show deck", command=self.show_deck)
        self.button.grid()

        self.button2 = Button(master, text="Show cards", command=self.show_cards_button)
        self.button2.grid()

        self.button3 = Button(master, text="Add Human deck", command=self.add_human_card)
        self.button3.grid()

    def start_game(self):
        game = Game()
        self.table = game.deck
        print('Something clicked')

    def take_player_cards(self, player):
        box = []
        card = player.player_take_card(self.table.get_card())
        for x in card:
            box.append(self.get_link(x))
        self.box = box
        return self.box

    def get_link(self, card):
        sign = None
        print(card.__dict__['rank'])
        if card.__dict__['rank'] is None:
            url = os.path.join(f'./static/None_of_None.png')
        else:
            if card.sign == '♣':
                sign = 'clubs'
            elif card.sign == '♠':
                sign = 'spades'
            elif card.sign == '♥':
                sign = 'hearts'
            else:
                sign = 'diamonds'
        url = os.path.join(f'./static/{card.rank}_of_{sign}.png')
        card_image = Image.open(url)
        card_scale = card_image.resize(((75, 125)))
        card_image = ImageTk.PhotoImage(card_scale)
        return card_image

    def show_deck(self):
        print(self.table)

        print('Something clicked')

    def add_human_card(self):
        self.take_player_cards(self.human)
        print(self.box)
        self.show_card(self.box)

    def show_cards_button(self):
        print(self.human.player_hand)

    def show_card(self, box):
        for index, x in enumerate(box):
            frame = Frame(self.master, padx=15, pady=15, bg="black")
            frame.grid(row=0, column=index)
            label = Label(frame, image=x)
            label.pack(side='bottom')


TableWindow(root)

root.mainloop()
