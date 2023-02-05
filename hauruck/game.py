import logging
import random


class Game:
    def __init__(self, players):
        self.players = players
        self.cards = [0] * len(self.players)

    def make_deck(self):
        deck = []
        for i in range(1, 14):
            for j in range(4):
                deck.append(i)
        random.shuffle(deck)
        return deck

    def deal_cards(self):  # random deal
        deck = self.make_deck()
        cards_per_player = len(deck) // len(self.players)
        for player in self.players:
            player.pile = deck[:cards_per_player]
            deck = deck[cards_per_player:]

    def deal_cards_fair(self):  # fair deal
        for player in self.players:
            player.pile = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]
            random.shuffle(player.pile)

    def play_round(self, last_round_cards):
        for index,player in enumerate(self.players):
            if player.is_pile_empty():
                player.discard_to_pile()
            self.cards[index] = player.play_card()
        if self.cards.count(max(self.cards)) > 1:
            logging.debug("same card")
            logging.debug(f"cards: {self.cards}\n")
            # if a player has no cards left, he can't play anymore
            if self.is_game_over():
                logging.debug("Player has no cards left. Game over.")
                return
            self.play_round(self.cards + last_round_cards)
        else:
            winner = self.players[self.cards.index(max(self.cards))]
            winner.add_to_discard_pile(self.cards + last_round_cards)
            logging.debug(f"cards: {self.cards}\n")

    def is_game_over(self):
        for player in self.players:
            if player.has_no_cards():
                return True
        return False

