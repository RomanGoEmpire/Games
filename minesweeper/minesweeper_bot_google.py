# Website https://www.google.com/search?client=firefox-b-d&q=minesweeper+
# size 40
import collections
import time
from random import random, randint

import pyautogui as p

tiles_x = collections.deque([])
tiles_y = collections.deque([])

# google minesweeper
hidden = (170, 215, 81)
hidden2 = (162, 209, 73)
mouse_on_hidden = (185, 221, 119)
mouse_on_hidden2 = (191, 225, 125)
blank = (229, 194, 159)
blank2 = (215, 184, 153)
flag = (242, 54, 7)
one = (30, 118, 210)
two = (58, 143, 61)
three = (211, 51, 51)
four = (123, 31, 162)
five = (240, 174, 92)
start_x = 673  # 650
start_y = 330  # 320
offset = 25
end_x = 673 + 23 * offset
end_y = 330 + 19 * offset


def initialize_tiles():
    for j in range(20):
        for i in range(24):
            tiles_x.append(start_x + i * offset)
            tiles_y.append(start_y + j * offset)


def get_color(x, y):
    return p.pixel(int(x), int(y))


def count_flags(x, y):
    result = 0
    if get_color(x - offset, y - offset) == flag:
        result += 1
    if get_color(x - offset, y) == flag:
        result += 1
    if get_color(x, y - offset) == flag:
        result += 1
    if get_color(x - offset, y + offset) == flag:
        result += 1
    if get_color(x, y + offset) == flag:
        result += 1
    if get_color(x + offset, y + offset) == flag:
        result += 1
    if get_color(x + offset, y) == flag:
        result += 1
    if get_color(x + offset, y - offset) == flag:
        result += 1
    return result


def reveal(x, y):
    if is_hidden(x - offset, y - offset):
        p.moveTo(x - offset, y - offset)
        p.leftClick()
    if is_hidden(x - offset, y):
        p.moveTo(x - offset, y)
        p.leftClick()
    if is_hidden(x, y - offset):
        p.moveTo(x, y - offset)
        p.leftClick()
    if is_hidden(x - offset, y + offset):
        p.moveTo(x - offset, y + offset)
        p.leftClick()
    if is_hidden(x, y + offset):
        p.moveTo(x, y + offset)
        p.leftClick()
    if is_hidden(x + offset, y + offset):
        p.moveTo(x + offset, y + offset)
        p.leftClick()
    if is_hidden(x + offset, y):
        p.moveTo(x + offset, y)
        p.leftClick()
    if is_hidden(x + offset, y - offset):
        p.moveTo(x + offset, y - offset)
        p.leftClick()
    p.moveTo(x, y)


def count_hidden(x, y):
    result = 0
    if is_hidden(x - offset, y - offset):
        result += 1
    if is_hidden(x - offset, y):
        result += 1
    if is_hidden(x, y - offset):
        result += 1
    if is_hidden(x - offset, y + offset):
        result += 1
    if is_hidden(x, y + offset):
        result += 1
    if is_hidden(x + offset, y + offset):
        result += 1
    if is_hidden(x + offset, y):
        result += 1
    if is_hidden(x + offset, y - offset):
        result += 1
    return result


def mark_hidden(x, y):
    if is_hidden(x - offset, y - offset):
        p.moveTo(x - offset, y - offset)
        p.rightClick()
    if is_hidden(x - offset, y):
        p.moveTo(x - offset, y)
        p.rightClick()
    if is_hidden(x, y - offset):
        p.moveTo(x, y - offset)
        p.rightClick()
    if is_hidden(x - offset, y + offset):
        p.moveTo(x - offset, y + offset)
        p.rightClick()
    if is_hidden(x, y + offset):
        p.moveTo(x, y + offset)
        p.rightClick()
    if is_hidden(x + offset, y + offset):
        p.moveTo(x + offset, y + offset)
        p.rightClick()
    if is_hidden(x + offset, y):
        p.moveTo(x + offset, y)
        p.rightClick()
    if is_hidden(x + offset, y - offset):
        p.moveTo(x + offset, y - offset)
        p.rightClick()
    p.moveTo(x, y)


def done_tile(x, y):
    if is_hidden(x - offset, y - offset):
        return False
    if is_hidden(x - offset, y):
        return False
    if is_hidden(x, y - offset):
        return False
    if is_hidden(x - offset, y + offset):
        return False
    if is_hidden(x, y + offset):
        return False
    if is_hidden(x + offset, y + offset):
        return False
    if is_hidden(x + offset, y):
        return False
    if is_hidden(x + offset, y - offset):
        return False
    return True


def is_in_bounds(x, y):
    return start_x <= x <= end_x and start_y <= y <= end_y


def is_number(x, y):
    if compare_colors(x, y, one):
        return True
    if compare_colors(x, y, two):
        return True
    if compare_colors(x, y, three):
        return True
    if compare_colors(x, y, four):
        return True
    if compare_colors(x, y, five):
        return True

    return False


def is_flag(x, y):
    return compare_colors(x, y, flag)


def solve():
    if len(tiles_x) > 0:
        x, y = tiles_x.popleft(), tiles_y.popleft()
        p.moveTo(x, y)
    else:
        print("No more Tiles")
        return True
    if is_mouse_on_hidden(x, y):
        tiles_x.append(x)
        tiles_y.append(y)
        return False
    if is_blank(x, y) or is_flag(x, y) or is_mouse_on_hidden(x, y):
        return False

    if compare_colors(x, y, one):
        number = 1
    elif compare_colors(x, y, two):
        number = 2
    elif compare_colors(x, y, three):
        number = 3
    elif compare_colors(x, y, four):
        number = 4
    elif compare_colors(x, y, five):
        number = 5
    else:
        print(get_difference(x, y, one))
        print(get_difference(x, y, two))
        print(get_difference(x, y, three))
        print(get_difference(x, y, four))
        print(get_difference(x, y, five))
        print(get_color(x, y))
        return True
    flag_counted = count_flags(x, y)
    hidden_count = count_hidden(x, y)
    # print(f"number: {number},flags: {flag_counted},hidden:  {hidden_count}")
    # time.sleep(10)
    if flag_counted == number:
        reveal(x, y)
    if hidden_count + flag_counted == number:
        mark_hidden(x, y)
    # if not done_tile(x, y):
    #     tiles_x.append(x)
    #     tiles_y.append(y)
    return False


def compare_colors(a, b, color):
    r, g, b = get_color(a, b)
    # if difference is less than 10, then it is the same color
    if abs(r - color[0]) < 30 and abs(g - color[1]) < 30 and abs(b - color[2]) < 30:
        return True


def get_difference(a, b, color):
    r, g, b = get_color(a, b)
    return abs(r - color[0]), abs(g - color[1]), abs(b - color[2])


def is_hidden(a, b):
    return get_color(a, b) == hidden or get_color(a, b) == hidden2


def is_mouse_on_hidden(x, y):
    return get_color(x, y) == mouse_on_hidden or get_color(x, y) == mouse_on_hidden2


def is_blank(x, y):
    return get_color(x, y) == blank or get_color(x, y) == blank2


def main():
    free = True
    tiles_left = len(tiles_x)
    initialize_tiles()
    for i in range(5):
        p.moveTo(tiles_x[randint(0, len(tiles_x) - 1)], tiles_y[randint(0, len(tiles_y) - 1)])
        p.leftClick()
        x, y = p.position()
        if is_blank(x, y):
            break
    found = False
    while not found:
        x, y = tiles_x.popleft(), tiles_y.popleft()
        p.moveTo(x, y)
        if not is_hidden(x, y):
            found = True
    while free:
        if solve():
            free = False
        else:
            if len(tiles_x) != tiles_left:
                tiles_left = len(tiles_x)
                print(f"Tiles left: {tiles_left}")


if __name__ == '__main__':
    main()
