from hauruck.game import Game
from hauruck.player import Player
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format=' %(message)s')


def log_players():
    for player in players:
        logging.debug(f"{player}")


if __name__ == '__main__':

    round = 10000
    round_count = [0] * round
    for i in range(round):
        if i % (round/10) == 0:
            logging.info(f"Round {i}")
        players = [Player("Player 1"), Player("Player 2")]
        game = Game(players)
        game.deal_cards_fair()
        for player in players:
            logging.debug(f"{player.pile}")
        rounds = 0
        while not game.is_game_over():
            log_players()
            rounds += 1
            game.play_round([])
        logging.debug(f"Game over after {rounds} rounds")
        round_count[i] = rounds

        for player in players:
            logging.debug(f"{player}")
    summed = {}
    round_count.sort()
    for single in round_count:
        if single in summed:
            summed[single] += 1
        else:
            summed[single] = 1
    keys = list(summed.keys())
    values = list(summed.values())

    # print the largest value in the dictionary and its key
    print(max(summed, key=summed.get), max(summed.values()))

    plt.bar(keys, values, color='blue', width=8)
    # Labeling the x and y axis
    plt.xlabel('Amount of rounds')
    plt.ylabel('Count of games')

    # Show the plot
    plt.show()
