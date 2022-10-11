import random

board = [0] * 40
board_history = []

blue = [39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12,
        11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
yellow = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20,
          19, 18, 17, 16, 15, 14, 13, 12, 11, 10]
green = [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30,
         29, 28, 27, 26, 25, 24, 23, 22, 21, 20]
red = [29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 39,
       38, 37, 36, 35, 34, 33, 32, 31, 30]


class Player:
    def __init__(self, name, color, offset, house):
        self.name = name
        self.color = color
        self.pieces = 0
        self.offset = offset
        self.house = house

    def update_pieces(self):
        self.pieces = board.count(self.color) + self.house.count(self.color)


def roll_dice(player):
    import random
    roll = random.randint(1, 6)
    # print(f"{player.name} rolled a {roll}")
    return roll


def print_board():
    round = board[0:10], board[10:20], board[20:30], board[30:40]
    print(round)
    print()


def place_piece_on_start(player):
    board[player.offset] = player.color
    player.update_pieces()


def true_next_index(index, dice):
    next_index = index + dice
    if next_index >= 40:
        next_index = next_index - 40
    return next_index


def get_best_move(valid_indexes, player):
    if not valid_indexes:
        return []
    best = 40
    if player.name == "Blue":
        for value in valid_indexes:
            if blue.index(value) < best:
                best = blue.index(value)
        return [blue[best]]
    elif player.name == "Yellow":
        for value in valid_indexes:
            if yellow.index(value) < best:
                best = yellow.index(value)
        return [yellow[best]]
    elif player.name == "Green":
        for value in valid_indexes:
            if green.index(value) < best:
                best = green.index(value)
        return [green[best]]
    elif player.name == "Red":
        for value in valid_indexes:
            if red.index(value) < best:
                best = red.index(value)
        return [red[best]]


def get_valid_moves(player, dice):
    house_indexes = []
    valid_indexes = [i for i, val in enumerate(board) if val == player.color]
    for index in valid_indexes:
        next_index = true_next_index(index, dice)
        if board[next_index] == player.color and not (index < player.offset <= next_index):
            valid_indexes.remove(index)
    # check if piece is in house which can be moved
    for index, color in enumerate(player.house):
        if color == player.color and index + dice <= 3 and player.house[index + dice] != player.color:
            house_indexes.append(index)
    return get_best_move(valid_indexes, player), house_indexes


# if you can hit a piece, do it
# if you have no valid move and didn't roll a 6, skip turn
# if you have a piece on the start, and you can move it , move it
# if you have no pieces on the start but rolled a 6, place a piece on the start
# if valid_indexes has only one element, move it
# if there are multiple valid moves, choose one
# if you rolled a 6, roll again
def move(player, dice):
    moved = False
    best_move, house_indexes = get_valid_moves(player, dice)
    # print(f"valid indexes: {valid_indexes}")
    # print(f"house indexes: {house_indexes}")
    for index in best_move:
        # if you can hit a piece, do it
        next_index = true_next_index(index, dice)
        if board[next_index] != player.color and board[next_index] != 0:
            move_piece(index, dice, player, False)
            moved = True
            break
    if not moved:
        player.update_pieces()
        # if you have no valid move and didn't roll a 6, skip turn
        if len(best_move) == 0 and len(house_indexes) == 0 and dice != 6:
            return
        # if you have a piece on the start, and you can move it , move it
        elif board[player.offset] == player.color and board[player.offset + dice] != player.color:
            move_piece(player.offset, dice, player, False)
        # if you have no pieces on the start but rolled a 6, place a piece on the start
        elif board[player.offset] != player.color and dice == 6 and player.pieces < 4:
            place_piece_on_start(player)
        # if only valid_indexes has valid moves, move it
        elif len(best_move) >= 1 and len(house_indexes) == 0:
            move_piece(best_move[0], dice, player, False)
        # of house_indexes has only one element, move it
        elif len(house_indexes) >= 1 and len(best_move) == 0:
            move_piece(house_indexes[0], dice, player, True)
        # if there are multiple valid moves, choose one
        elif len(best_move) >= 1 and len(house_indexes) >= 1:
            move_piece(house_indexes[0], dice, player, True)
    # print_board()
    # if you rolled a 6, roll again
    if dice == 6:
        next_dice = roll_dice(player)
        move(player, next_dice)


def move_piece(index, dice, player, inHouse):
    # move piece if place is empty
    if not inHouse:
        next_index = true_next_index(index, dice)
        if player.name == "Blue" and 34 <= index <= 39 and player.offset <= next_index <= player.offset + 3 and \
                player.house[next_index - player.offset] == 0:
            player.house[next_index - player.offset] = player.color
            board[index] = 0
        elif player.name == "Yellow" and 4 <= index <= 9 and player.offset <= next_index <= player.offset + 3 and \
                player.house[next_index - player.offset] == 0:
            player.house[next_index - player.offset] = player.color
            board[index] = 0
        elif player.name == "Green" and 14 <= index <= 19 and player.offset <= next_index <= player.offset + 3 and \
                player.house[next_index - player.offset] == 0:
            player.house[next_index - player.offset] = player.color
            board[index] = 0
        elif player.name == "Red" and 24 <= index <= 29 and player.offset <= next_index <= player.offset + 3 and \
                player.house[next_index - player.offset] == 0:
            player.house[next_index - player.offset] = player.color
            board[index] = 0
        else:
            board[next_index] = player.color
            board[index] = 0
    else:
        next_index = index + dice
        player.house[next_index] = player.color
        player.house[index] = 0


def initialize_players():
    blue = Player("Blue", "b", 0, [0] * 4)
    yellow = Player("Yellow", "y", 10, [0] * 4)
    green = Player("Green", "g", 20, [0] * 4)
    red = Player("Red", "r", 30, [0] * 4)
    # random player starts  but should maintain order
    options = [[blue, yellow, green, red], [yellow, green, red, blue], [green, red, blue, yellow],[red, blue, yellow, green]]
    return  options[random.randint(0,3)]


def gameloop():
    players = initialize_players()
    while True:
        # look for winner
        for player in players:
            if player.house.count(player.color) == 4:
                return player.name
        # play move for each player
        for player in players:
            for _ in range(3):
                dice = roll_dice(player)
                player.update_pieces()
                if dice == 6 or player.pieces > 0:
                    move(player, dice)
                    break


if __name__ == '__main__':
    blue_wins, yellow_wins, green_wins, red_wins = 0, 0, 0, 0
    for i in range(10000):
        if i % 10000 == 0:
            print(i)
        initialize_players()
        winner = gameloop()
        if winner == "Blue":
            blue_wins += 1
        elif winner == "Yellow":
            yellow_wins += 1
        elif winner == "Green":
            green_wins += 1
        elif winner == "Red":
            red_wins += 1
    print(f"blue wins: {blue_wins}")
    print(f"yellow wins: {yellow_wins}")
    print(f"green wins: {green_wins}")
    print(f"red wins: {red_wins}")
    print(f"total: {blue_wins + yellow_wins + green_wins + red_wins}")
    print(f"blue wins: {blue_wins / (blue_wins + yellow_wins + green_wins + red_wins) * 100}%")
    print(f"yellow wins: {yellow_wins / (blue_wins + yellow_wins + green_wins + red_wins) * 100}%")
    print(f"green wins: {green_wins / (blue_wins + yellow_wins + green_wins + red_wins) * 100}%")
    print(f"red wins: {red_wins / (blue_wins + yellow_wins + green_wins + red_wins) * 100}%")
