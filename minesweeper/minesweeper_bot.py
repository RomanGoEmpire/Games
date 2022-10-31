# Website https://minesweeper.online/de
# size 38
import time
from random import random, randint

import pyautogui as p

# minesweeper.online
blank = (198, 198, 198)
flag = (0, 0, 0)
white = (255, 255, 255)

color_one = (0, 0, 255)
color_two = (0, 128, 0)
color_three = (255, 0, 0)
color_four = (0, 0, 128)
color_five = (128, 0, 0)
color_six = (49, 145, 145)
color_bomb = (37, 41, 36)

start_x = 521
start_y = 406
end_x = 1623
end_y = 996
offset = 38
o = 18
rows = 16
cols = 30

done = []
changes = False


def initialize_colors():
    colors = []
    for i in range(rows):
        colors.append([])
        for j in range(cols):
            colors[i].append(0)
    print("Initialized colors")
    return colors


def get_index_of_color(colors, number_color):
    numbers = []
    for i in range(rows):
        for j in range(cols):
            if colors[i][j] == number_color:
                numbers.append((i, j))
    return numbers


def get_color(x, y):
    return p.pixel(x, y)


def convert_index_to_coords(index):
    x = start_x + index[1] * offset
    y = start_y + index[0] * offset
    return x, y


def count_hidden(index, colors):
    row, col = index
    count = 0
    if 0 < row - 1 < rows and 0 < col - 1 < cols:
        if is_hidden((row - 1, col - 1), colors):
            count += 1
    if 0 < row - 1 < rows:
        if is_hidden((row - 1, col), colors):
            count += 1
    if 0 < row - 1 < rows and 0 < col + 1 < cols:
        if is_hidden((row - 1, col + 1), colors):
            count += 1
    if 0 < col + 1 < cols:
        if is_hidden((row, col + 1), colors):
            count += 1
    if 0 < row + 1 < rows and 0 < col + 1 < cols:
        if is_hidden((row + 1, col + 1), colors):
            count += 1
    if 0 < row + 1 < rows:
        if is_hidden((row + 1, col), colors):
            count += 1
    if 0 < row + 1 < rows and 0 < col - 1 < cols:
        if is_hidden((row + 1, col - 1), colors):
            count += 1
    if 0 < col - 1 < cols:
        if is_hidden((row, col - 1), colors):
            count += 1
    return count


def convert_color_to_number(color):
    if color == color_one:
        return 1
    elif color == color_two:
        return 2
    elif color == color_three:
        return 3
    elif color == color_four:
        return 4
    elif color == color_five:
        return 5
    elif color == color_six:
        return 6
    else:
        return "Error"


def is_hidden(index, colors):
    row, col = index
    x, y = convert_index_to_coords(index)
    if colors[row][col] == blank and get_color(x - o, y - o) == white:
        return True
    return False


def flag_neighbors(index, colors):
    x, y = convert_index_to_coords(index)
    row, col = index
    if 0 <= row - 1 < rows and 0 <= col - 1 < cols:
        if colors[row - 1][col - 1] == blank:
            p.moveTo(x - offset, y - offset)
            p.rightClick()
            colors[row - 1][col - 1] = flag

    if 0 <= row - 1 < rows:
        if colors[row - 1][col] == blank:
            p.moveTo(x, y - offset)
            p.rightClick()
            colors[row - 1][col] = flag
    if 0 <= row - 1 < rows and 0 <= col + 1 < cols:
        if colors[row - 1][col + 1] == blank:
            p.moveTo(x + offset, y - offset)
            p.rightClick()
            colors[row - 1][col + 1] = flag

    if 0 <= col + 1 < cols:
        if colors[row][col + 1] == blank:
            p.moveTo(x + offset, y)
            p.rightClick()
            colors[row][col + 1] = flag

    if 0 <= row + 1 < rows and 0 <= col + 1 < cols:
        if colors[row + 1][col + 1] == blank:
            p.moveTo(x + offset, y + offset)
            p.rightClick()
            colors[row + 1][col + 1] = flag

    if 0 <= row + 1 < rows:
        if colors[row + 1][col] == blank:
            p.moveTo(x, y + offset)
            p.rightClick()
            colors[row + 1][col] = flag

    if 0 <= row + 1 < rows and 0 <= col - 1 < cols:
        if colors[row + 1][col - 1] == blank:
            p.moveTo(x - offset, y + offset)
            p.rightClick()
            colors[row + 1][col - 1] = flag

    if 0 <= col - 1 < cols:
        if colors[row][col - 1] == blank:
            p.moveTo(x - offset, y)
            p.rightClick()
            colors[row][col - 1] = flag
    return colors


def flag_numbers(index, color, colors):
    hidden = count_hidden(index, colors)
    flags = count_flags(index, colors)
    number = convert_color_to_number(color)
    if hidden + flags == number and hidden != 0:
        colors = flag_neighbors(index, colors)
    return colors


def reveal_numbers(index, colors):
    x, y = convert_index_to_coords(index)
    flags = count_flags(index, colors)
    number = convert_color_to_number(get_color(x, y))
    if flags == number:
        p.moveTo(x, y)
        p.leftClick()
        done.append(index)
    return


def count_flags(index, colors):
    count = 0
    row, col = index
    if 0 <= row - 1 < rows and 0 <=col - 1 < cols:
        if colors[row - 1][col - 1] == flag:
            count += 1
    if 0 <= row - 1 < rows:
        if colors[row - 1][col] == flag:
            count += 1
    if 0 <= row - 1 < rows and 0 <= col + 1 < cols:
        if colors[row - 1][col + 1] == flag:
            count += 1
    if 0 <= col + 1 < cols:
        if colors[row][col + 1] == flag:
            count += 1
    if 0 <= row + 1 < rows and 0 <= col + 1 < cols:
        if colors[row + 1][col + 1] == flag:
            count += 1
    if 0 <= row + 1 < rows:
        if colors[row + 1][col] == flag:
            count += 1
    if 0 <= row + 1 < rows and 0 <= col - 1 < cols:
        if colors[row + 1][col - 1] == flag:
            count += 1
    if 0 <= col - 1 < cols:
        if colors[row][col - 1] == flag:
            count += 1
    return count


def solve(colors):
    colors = update_colors(colors)
    print("Done updating colors")
    ones = get_index_of_color(colors, color_one)
    twos = get_index_of_color(colors, color_two)
    threes = get_index_of_color(colors, color_three)
    fours = get_index_of_color(colors, color_four)
    fives = get_index_of_color(colors, color_five)
    sixes = get_index_of_color(colors, color_six)
    bombs = get_index_of_color(colors, color_bomb)
    if len(bombs) > 0:
        print("You lost")
        return
    colors = look_at_number(colors, ones, color_one)
    colors = look_at_number(colors, twos, color_two)
    colors = look_at_number(colors, threes, color_three)
    colors = look_at_number(colors, fours, color_four)
    colors = look_at_number(colors, fives, color_five)
    colors = look_at_number(colors, sixes, color_six)

    if len(ones) == 0 and len(twos) == 0 and len(threes) == 0 and len(fours) == 0 and len(fives) == 0 and len(
            sixes) == 0:
        print("You won")
        return
    elif len(bombs) > 0:
        print("You lost")
        return
    else:
        solve(colors)
    return


def look_at_number(colors, list_number, color):
    if len(list_number) > 0:
        print(f"Looking at {convert_color_to_number(color)}")
        for index in list_number:
            if index not in done:
                colors = flag_numbers(index, color, colors)
                reveal_numbers(index, colors)
    return colors


def update_colors(colors):
    for i in range(rows):
        for j in range(cols):
            x, y = convert_index_to_coords((i, j))
            colors[i][j] = get_color(x, y)
    return colors


def main():
    colors = initialize_colors()
    # time.sleep(2)
    # for i in range(10):
    #     x = randint(start_x, end_x)
    #     y = randint(start_y, end_y)
    #     p.moveTo(x, y)
    #     p.leftClick()
    # colors = update_colors(colors)
    # if len(get_index_of_color(colors, color_bomb)) == 0:
    #     print("No bombs")
    solve(colors)
    # else:
    #     p.moveTo(1050, 350)
    #     p.leftClick()
    #     main()


if __name__ == '__main__':

    main()
