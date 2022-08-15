from main import basics_decide_soft_total

for b in range(2, 10):
    for c in range(2, 12):
        player = [11, b]
        dealer = c

        print(player, dealer, basics_decide_soft_total(player, dealer))
