import random

import matplotlib.pyplot as plt

# player balance

player_balance = 1000
player_balance_history = []
# player stats
player_stats = [0, 0, 0]
bet_size = 1
bet = [0]
surrender_count = 0
deck = []


# create card deck
def create_card_deck():
    global deck
    current = []
    for _ in range(1):
        for i in range(2, 10):
            current += [i] * 4
        current += [10] * 16
        current += [11] * 4
    deck += current
    random.shuffle(deck)


# create player and dealer
def create_player_and_dealer():
    player = []
    dealer = []
    return player, dealer


# get new card from deck
def get_new_card():
    global deck
    if len(deck) == 0:
        create_card_deck()
    return deck.pop()


# deal cards to player and dealer
def deal_cards(player, dealer):
    player_hand = []
    for i in range(2):
        player_hand.append(get_new_card())
        dealer.append(get_new_card())
    player.append(player_hand)
    global bet
    global player_balance
    bet = [bet_size]
    player_balance -= bet_size
    return player, dealer


# # print cards
def print_cards(player, dealer):
    pass
    print("Player: ", player[0])
    print("Dealer: ", dealer[0])


# checks if player can split
def can_split(player):
    if player[0] == player[1]:
        return True
    else:
        return False


# player turn
def print_balance():
    print(f"Bet: {bet}")
    print(f"Balance: {player_balance}")


def change_bet(choice, index):
    global bet
    global player_balance
    if choice == "d":
        player_balance -= bet[index]
        bet[index] *= 2
    else:
        bet.append(bet[index])
        player_balance -= bet[index]


def pay_out(hand, player_won, index):
    global player_balance
    if player_won is None:
        # bet is return to player
        player_balance += bet[index]
    if player_won and sum(hand) == 21 and len(hand) == 2:
        # player wins blackjack 3:2
        player_balance += bet[index] * 2.5
    elif player_won:
        # player wins normal
        player_balance += bet[index] * 2
    player_balance_history.append(player_balance)


bust_count = 0


def player_turn(player, dealer):
    for index, hand in enumerate(player):
        if can_split(hand):
            choice = basics_decide_to_split(hand, dealer[0])
            if choice == "y":
                new_hand = [hand.pop()]
                hand.append(get_new_card())
                new_hand.append(get_new_card())
                player.append(new_hand)
                change_bet("split", index)
        if sum(hand) == 21:
            continue
        while True:
            choice = basics_decide_totals(hand, player, dealer[0])
            if choice == "h":
                hand.append(get_new_card())
                if sum(hand) == 21:
                    break
                if sum(hand) > 21 and 11 in hand:
                    hand[hand.index(11)] = 1
                elif sum(hand) > 21:
                    global bust_count
                    bust_count += 1
                    break
            elif choice == "s":
                break
            elif choice == "d":
                hand.append(get_new_card())
                change_bet("d", index)
                break
    return player


# dealer turn
def dealer_turn(dealer):
    while True:
        if sum(dealer) < 17:
            dealer.append(get_new_card())
        # change here to make dealer hit on soft 17
        elif sum(dealer) > 21 and 11 in dealer:
            dealer[dealer.index(11)] = 1
            dealer.append(get_new_card())
        else:
            break
    return dealer


# determine winner
def declare_winner(player, dealer):
    global player_balance
    for index, hand in enumerate(player):
        if sum(hand) > 21 or sum(hand) == 0:
            add_loss()
            pay_out(hand, False, index)
        elif sum(dealer) > 21:
            add_win()
            pay_out(hand, True, index)
        elif sum(hand) > sum(dealer):
            add_win()
            pay_out(hand, True, index)
        elif sum(hand) < sum(dealer):
            add_loss()
            pay_out(hand, False, index)
        else:
            add_tie()
            pay_out(hand, None, index)


# add win to player stats
def add_win():
    player_stats[0] += 1


# add loss to player stats
def add_loss():
    player_stats[1] += 1


# add tie to player stats
def add_tie():
    player_stats[2] += 1


def basics_decide_to_split(player, dealer):
    if player == [11, 11] or player == [8, 8]:
        return "y"
    elif player == [10, 10] or player == [5, 5]:
        return "n"
    elif player == [9, 9]:
        if dealer == 7 or dealer == 10 or dealer == 11:
            return "n"
    elif player == [7, 7]:
        if dealer > 7:
            return "n"
    elif player == [6, 6]:
        if dealer > 6 or dealer ==2:
            return "n"
    elif player == [4, 4]:
        # if dealer != 4 or dealer != 5:
        return "n"
    elif player == [3, 3] or player == [2, 2]:
        if dealer > 7 or dealer == 2 or dealer == 3:
            return "n"
    return "y"


soft_total_table = [["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "s", "s", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],
                    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"]]


def basics_decide_soft_total(player, dealer):
    sum_player = sum(player)
    return soft_total_table[sum_player - 13][dealer - 2]


hard_total_table = [["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["d", "d", "d", "d", "d", "d", "d", "d", "h", "h"],
                    ["d", "d", "d", "d", "d", "d", "d", "d", "d", "d"],
                    ["h", "h", "s", "s", "s", "h", "h", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"]]


def basics_decide_hard_total(hand, dealer):
    player_count = sum(hand)
    if player_count <= 8:
        return "h"
    elif player_count >= 17:
        return "s"
    elif 13 <= player_count <= 16:
        return hard_total_table[4][dealer - 2]
    else:
        return hard_total_table[player_count - 9][dealer - 2]


def basics_decide_totals(hand, player, dealer):
    if hand.count(11) == 1:
        return basics_decide_soft_total(hand, dealer)
    else:
        return basics_decide_hard_total(hand, dealer)


# players win_rate
def win_rate():
    print("Wins:   ", player_stats[0])
    print("Losses: ", player_stats[1])
    print("Ties:   ", player_stats[2])
    print(f"Winrate: {str((player_stats[0] / (player_stats[0] + player_stats[1])) * 100)} %")
    print(f"Tierate: {str((player_stats[2] / sum(player_stats)) * 100)} %")
    print(f"Surrender count: {surrender_count / sum(player_stats) * 100} %")
    print(f"Saved losses: {surrender_count / 2}")
    print(f"Balance: {player_balance}")
    print(f"Busted count: {bust_count}")


# play game
def play_game(rounds):
    create_card_deck()
    counter = 0  # counter for number of games played
    while counter < rounds:
        you, bank = create_player_and_dealer()
        you, bank = deal_cards(you, bank)
        # print_cards(you, bank)
        if not sum(bank) == 21:
            you = player_turn(you, bank)
            bank = dealer_turn(bank)
        declare_winner(you, bank)
        if len(deck) < random.randint(10, 30):
            create_card_deck()
        counter += 1
        if counter == rounds:
            win_rate()
            break
    win_rate()
    print("Rounds played: ", counter)
    plt.plot(player_balance_history)
    plt.show()


if __name__ == '__main__':
    play_game(1_000_000)
