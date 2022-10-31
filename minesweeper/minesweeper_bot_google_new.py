import ctypes
from random import randint

import pyautogui as p


from minesweeper.minesweeper_bot import get_color

hidden = (170, 215, 81)
hidden2 = (162, 209, 73)
blank = (229, 194, 159)
blank2 = (215, 184, 153)
flag = (242, 54, 7)
one = (25, 118, 210)
two = (56, 142, 60)
three = (211, 47, 47)
four = (123, 31, 162)
five = (240, 174, 92)

color_list = [hidden, hidden2, blank, blank2, flag, one, two, three, four, five]

start_x = 673  # 650
start_y = 330  # 320
offset = 25
end_x = 673 + 23 * offset
end_y = 330 + 19 * offset
rows = 20
cols = 24
done = []
position_list = []
found = False
solved = False
ones, twos, threes, fours, fives = [], [], [], [], []


def get_colors(table):
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in done:
                x, y = get_coordinates((row, col))
                table[row][col] = get_color(x, y)
    return table


def get_coordinates(index):
    return position_list[index[0]][index[1]][0], position_list[index[0]][index[1]][1]


def initialize_position_list():
    for i in range(rows):
        position_list.append([])
        for j in range(cols):
            position_list[i].append((convert_index_to_coords((i, j))))


def is_bomb(table):
    for row in range(rows):
        for col in range(cols):
            if table[row][col] not in color_list:
                if near_five(table[row][col]):
                    continue
                if near_hidden(table[row][col]):
                    continue
                print(row, col)
                print(table[row][col])
                return True
    return False


def are_all_hidden(table):
    for row in range(rows):
        for col in range(cols):
            if table[row][col] != hidden and table[row][col] != hidden2:
                return False
    return True


def convert_index_to_coords(index):
    x = start_x + index[1] * offset
    y = start_y + index[0] * offset
    return x, y


def count_flags(index, table):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= index[0] + i < rows and 0 <= index[1] + j < cols:
                if table[index[0] + i][index[1] + j] == flag:
                    count += 1
    return count


def count_hidden(index, table):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= index[0] + i < rows and 0 <= index[1] + j < cols:
                if table[index[0] + i][index[1] + j] == hidden or table[index[0] + i][index[1] + j] == hidden2:
                    count += 1
    return count


def reveal_index(index, table):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= index[0] + i < rows and 0 <= index[1] + j < cols:
                if table[index[0] + i][index[1] + j] == hidden or table[index[0] + i][index[1] + j] == hidden2:
                    x, y = get_coordinates((index[0] + i, index[1] + j))
                    p.moveTo(x, y)
                    p.leftClick()
                    table[index[0] + i][index[1] + j] = get_color(x, y)
                    global found
                    found = True
    done.append(index)
    return table


def flag_index(index, table):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= index[0] + i < rows and 0 <= index[1] + j < cols:
                if table[index[0] + i][index[1] + j] == hidden or table[index[0] + i][index[1] + j] == hidden2:
                    x, y = get_coordinates((index[0] + i, index[1] + j))
                    p.moveTo(x, y)
                    p.rightClick()
                    table[index[0] + i][index[1] + j] = flag
                    global found
                    found = True
                    if get_color(x, y) == blank or get_color(x, y) == blank2:
                        done.append((index[0] + i, index[1] + j))
    done.append(index)
    return table


def get_random_hidden(table):
    while True:
        row = randint(0, rows - 1)
        col = randint(0, cols - 1)
        if table[row][col] == hidden or table[row][col] == hidden2:
            return row, col


def flag_or_reveal(i, index, table):
    flag_count = count_flags(index, table)
    hidden_count = count_hidden(index, table)
    if flag_count == i + 1:
        table = reveal_index(index, table)
    elif hidden_count + flag_count == i + 1:
        table = flag_index(index, table)
    return table


def near_hidden(color):
    if abs(color[0] - hidden[0]) < 10 and abs(color[1] - hidden[1]) < 10 and abs(color[2] - hidden[2]) < 10 and abs(
            color[0] - hidden2[0]) < 10 and abs(color[1] - hidden2[1]) < 10 and abs(color[2] - hidden2[2]) < 10:
        return True


def near_five(color):
    if abs(color[0] - five[0]) < 30 and abs(color[1] - five[1]) < 30 and abs(color[2] - five[2]) < 30:
        return True


def fill_number_indexes(table):
    global ones, twos, threes, fours, fives
    ones, twos, threes, fours, fives = [], [], [], [], []
    for i, row in enumerate(table):
        for j, color in enumerate(row):
            if color == one:
                ones.append((i, j))
            elif color == two:
                twos.append((i, j))
            elif color == three:
                threes.append((i, j))
            elif color == four:
                fours.append((i, j))
            elif near_five(color):
                fives.append((i, j))


def solve(table):
    fill_number_indexes(table)
    number = [ones, twos, threes, fours, fives]
    for i in range(len(number)):
        for index in number[i]:
            table = flag_or_reveal(i, index, table)
    global found
    if found:
        found = False
    else:
        x, y = get_coordinates(get_random_hidden(table))
        p.moveTo(x, y)
        p.leftClick()
        if get_color(x, y) not in color_list:
            print(get_color(x, y))
            print(x, y)
            global solved
            solved = True
        found = False


def main():
    global solved
    solved = False
    table = [[0 for _ in range(cols)] for _ in range(rows)]
    initialize_position_list()
    x, y = randint(start_x, end_x), randint(start_y, end_y)
    p.moveTo(x, y)
    p.leftClick()
    x, y = randint(start_x, end_x), randint(start_y, end_y)
    p.moveTo(x, y)
    p.leftClick()
    table = get_colors(table)
    while not solved:
        solve(table)
        # p.moveTo(300, 300)
        table = get_colors(table)


if __name__ == '__main__':
    #main()
    p.get
