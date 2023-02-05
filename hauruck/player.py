import random


class Player:
    def __init__(self, name):
        self.name = name
        self.pile = []
        self.discard_pile = []

    def play_card(self):
        return self.pile.pop()

    def add_to_discard_pile(self, cards):
        self.discard_pile.extend(cards)

    def discard_to_pile(self):
        self.pile = random.sample(self.discard_pile, len(self.discard_pile))
        self.discard_pile = []

    def is_pile_empty(self):
        return not bool(self.pile)

    def has_no_cards(self):
        return not bool(self.pile or self.discard_pile)

    def __str__(self):
        return f"{self.name}:" \
               f" p:{len(self.pile)}, d:{len(self.discard_pile)}"
