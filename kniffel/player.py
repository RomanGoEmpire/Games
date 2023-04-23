import random


class Player:

    def __init__(self, name):
        self.name = name
        self.score_table = self.get_score_table()
        self.dices = [0] * 5
        self.stored = []
        self.scores = self.get_scores()

    def play(self):
        self.dices = [0] * 5
        self.stored = []
        print(self.name)
        for i in range(3):
            self.roll_dices()
            if i > 1:
                continue
            dices = self.decide_what_stones_to_keep()
            self.take_dice(dices)
            user_input = input("Score?")
            if user_input == "y":
                self.score_hand()
                print(self.score_table)
                return
        self.score_hand()
        print(self.score_table)

    def roll_dices(self):
        for i in range(len(self.dices)):
            self.dices[i] = random.randint(1, 6)
        self.dices.sort()

    def can_take_dices(self, arr):
        both = self.stored + self.dices
        for number in arr:
            if not number in both:
                return False
        return True

    def take_dice(self, arr):
        self.dices = [0] * (5 - len(arr))
        self.stored = arr

    def get_score_table(self):
        return {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
                "tripple": 0, "four": 0, "fullHouse": 0, "small": 0, "large": 0,
                "kniffel": 0, "chance": 0}

    def score_hand(self):
        self.stored += self.dices
        print(self.stored)
        options = self.get_options()
        if not options:
            remove_options = self.get_remove_option()
            self.remove_option(remove_options)
            return
        user_input = input(f"Your options are: {options}")
        if user_input in self.score_table:
            self.evaluate_hand(user_input)

    def remove_option(self, remove_options):
        user_input = input(f"You cant take anything. Which option do you want to remove: {remove_options}")
        if user_input in remove_options:
            self.score_table[user_input] = None
            return self.decide_what_stones_to_keep()
            return

    def evaluate_hand(self, user_input):
        self.score_table[user_input] = self.scores.get(user_input)

    def decide_what_stones_to_keep(self):
        print(self.dices)
        print(self.stored)
        user_input = input("What dices do you want to keep: ")
        str_arr = user_input.split()
        numbers = []
        for str in str_arr:
            numbers.append(int(str))
        if self.can_take_dices(numbers):
            return numbers
        return self.decide_what_stones_to_keep()

    def is_not_scored(self, type):
        return self.score_table.get(type) == 0

    def get_options(self):
        options = []
        for i in range(1, 7):
            if self.stored.count(i) > 0 and self.is_not_scored(f'{i}'):
                options.append(f"{i}")

        if self.tripple() and self.is_not_scored("tripple"):
            options.append("tripple")
        if self.four() and self.is_not_scored("four"):
            options.append("four")
        if self.fullhouse() and self.is_not_scored("fullHouse"):
            options.append("fullHouse")
        if self.small() and self.is_not_scored("small"):
            options.append("small")
        if self.large() and self.is_not_scored("large"):
            options.append("large")
        if self.kniffle() and self.is_not_scored("kniffel"):
            options.append("kniffel")
        if self.is_not_scored("chance"):
            options.append("chance")
        return options

    def tripple(self):
        set_stored = set(self.stored)
        stored = []
        for value in set_stored:
            stored.append(value)

        for number in stored:
            if self.stored.count(number) == 3:
                return True
        return False

    def four(self):
        stored = [set(self.stored)]
        for number in stored:
            if self.stored.count(number) == 4:
                return True
        return False

    def fullhouse(self):
        stored = list(set(self.stored))
        if len(stored) != 2:
            return False
        return self.stored.count(stored[0]) == 2 and self.stored.count(stored[1]) == 3 or \
            self.stored.count(stored[0]) == 3 and self.stored.count(stored[1]) == 2

    def small(self):
        return self.stored == [1, 2, 3, 4] \
            or self.stored == [2, 3, 4, 5] \
            or self.stored == [3, 4, 5, 6]

    def large(self):
        return self.stored == [1, 2, 3, 4, 5] or self.stored == [2, 3, 4, 5, 6]

    def kniffle(self):
        return len(set(self.stored)) == 1 and len(self.stored) == 5

    def get_remove_option(self):
        options = []
        for key, value in self.score_table.items():
            if value == 0:
                options.append(key)
        return options

    def get_scores(self):
        return {
            "1": self.stored.count(1) * 1,
            "2": self.stored.count(2) * 2,
            "3": self.stored.count(3) * 3,
            "4": self.stored.count(4) * 4,
            "5": self.stored.count(5) * 5,
            "6": self.stored.count(6) * 6,
            "tripple": sum(self.stored),
            "four": sum(self.stored),
            "chance": sum(self.stored),
            "fullHouse": 25,
            "small": 30,
            "large": 40,
            "kniffel": 50,
        }
