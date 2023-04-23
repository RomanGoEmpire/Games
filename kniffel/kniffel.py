from player import Player

ROUNDS = 13


class Game:

    def __init__(self, players):
        self.players = players

    def gameloop(self):
        for i in range(ROUNDS):
            for player in self.players:
                player.play()

        winner = None
        score = 0
        for player in self.players:
            if player.score() > score:
                winner = player
                score = player.score()
        print(winner)


if __name__ == '__main__':
    player1 = Player("1")
    player2 = Player("2")
    game = Game([player1, player2])
    game.gameloop()
