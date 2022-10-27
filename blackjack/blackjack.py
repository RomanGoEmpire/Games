import math
import random
import matplotlib.pyplot as plt

# deck
deck = []
# player balance
player_balance_start = 1000
player_balance = player_balance_start
player_balance_history = []
# player stats
player_stats = [0, 0, 0]
# bets
bet_size = 10
bet = [0]
# card counting
running_count = 0
played_cards = 0
true_count = 0
true_above_five = 0


# create card deck
def create_card_deck():
    global deck
    current = []
    for _ in range(6):
        for i in range(2, 10):
            current += [i] * 4
        current += [10] * 16
        current += [11] * 4
    deck += current
    random.shuffle(deck)
    global running_count
    running_count = 0


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


# player turn
def print_balance():
    print(f"Bet: {bet}")
    print(f"Balance: {player_balance}")


# checks if player can split
def can_split(player):
    if player[0] == player[1]:
        return True
    else:
        return False


def change_bet(choice, index):
    global bet
    global player_balance
    if choice == "d":
        player_balance -= bet[index]
        bet[index] *= 2
    elif choice == "sur":
        bet[index] /= 2
        player_balance += bet[index]

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
            choice = basics_decide_totals(hand, dealer[0])
            if choice == "h":
                hand.append(get_new_card())
                if sum(hand) == 21:
                    break
                if sum(hand) > 21 and 11 in hand:
                    hand[hand.index(11)] = 1
                elif sum(hand) > 21:
                    break
            elif choice == "s":
                break
            elif choice == "sur":
                change_bet("sur", index)
                hand = [0]
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


def basics_decide_to_split(player, dealer):
    if player == [11, 11] or player == [8, 8]:
        return "y"
    elif player == [10, 10] or player == [5, 5]:
        return "n"
    elif player == [9, 9]:
        if dealer == 7 or dealer == 10 or dealer == 11:
            return "n"
    elif player == [7, 7]:
        if dealer >= 8:
            return "n"
    elif player == [6, 6]:
        if dealer >= 7:
            return "n"
    elif player == [4, 4]:
        if dealer == 4 or dealer == 5:
            return "y"
        else:
            return "n"
    elif player == [3, 3] or player == [2, 2]:
        if dealer >= 8:
            return "n"
    return "y"


def basics_decide_totals(hand, dealer):
    if hand.count(11) == 1:
        return basics_decide_soft_total(hand, dealer)
    else:
        return basics_decide_hard_total(hand, dealer)


soft_total_table = [["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "s", "s", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],
                    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"]]
hard_total_table = [["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],
                    ["d", "d", "d", "d", "d", "d", "d", "d", "h", "h"],
                    ["d", "d", "d", "d", "d", "d", "d", "d", "d", "d"],
                    ["h", "h", "s", "s", "s", "h", "h", "h", "h", "h"],
                    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"]]


def basics_decide_soft_total(player, dealer):
    sum_player = sum(player)
    return soft_total_table[sum_player - 13][dealer - 2]


def basics_decide_hard_total(hand, dealer):
    player_count = sum(hand)
    if player_count == 16 and len(hand) == 2 and (9 <= dealer <= 11):
        return "sur"
    if player_count == 15 and len(hand) == 2 and dealer == 10:
        return "sur"
    if player_count <= 8:
        return "h"
    elif player_count >= 17:
        return "s"
    elif 13 <= player_count <= 16:
        return hard_total_table[4][dealer - 2]
    else:
        return hard_total_table[player_count - 9][dealer - 2]


# determine winner
def declare_winner(player, dealer):
    global player_balance
    update_running_count(player, dealer)
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


def update_running_count(player, dealer):
    global running_count
    global played_cards
    global true_count
    cards = []
    for hand in player:
        for card in hand:
            cards.append(card)
    for card in dealer:
        cards.append(card)
    for card in cards:
        if card <= 6:
            running_count += 1
        if card >= 10:
            running_count -= 1
    played_cards += len(cards)
    true_count = math.floor(running_count / (len(deck) / 52))
    if true_count >= 5:
        global true_above_five
        true_above_five += 1


# play game
def reset():
    global player_balance
    global player_balance_history
    global player_stats
    global bet_size
    global bet
    global deck
    global true_above_five
    player_balance = 1000
    player_balance_history = []
    # player stats
    player_stats = [0, 0, 0]
    bet_size = 10
    bet = [0]
    deck = []
    true_above_five = 0


# players win_rate
def print_win_rate(rounds):
    print("Rounds played: ", rounds)
    print("Wins:   ", player_stats[0])
    print("Losses: ", player_stats[1])
    print("Ties:   ", player_stats[2])
    print(f"Win-rate: {str((player_stats[0] / (player_stats[0] + player_stats[1])) * 100)} %")
    print(f"Tie-rate: {str((player_stats[2] / sum(player_stats)) * 100)} %")
    print(f"Balance Start: {player_balance_start}")
    print(f"Balance: {player_balance}")
    print("True:", true_above_five / rounds)
    print("Loss per game: ", (player_balance - player_balance_start) / rounds)


def play_game(rounds, balance):
    global player_balance_start
    global player_balance
    player_balance_start = balance
    player_balance = balance
    create_card_deck()
    counter = 0  # counter for number of games played
    while counter < rounds and player_balance > 2:
        you, bank = create_player_and_dealer()
        you, bank = deal_cards(you, bank)
        if not sum(bank) == 21:
            you = player_turn(you, bank)
            bank = dealer_turn(bank)
        declare_winner(you, bank)
        if len(deck) < random.randint(50, 100):
            create_card_deck()
        counter += 1
        if counter == rounds:
            break
    print_win_rate(counter)
    plt.plot(player_balance_history)
    plt.show()
    reset()


if __name__ == '__main__':
    play_game(1_000_000, 10000)
