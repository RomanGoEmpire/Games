# Website https://minesweeper.online/de
# size 38
import pyautogui as p
import random
import time

blank = (198, 198, 198)
flag = (0, 0, 0)
white = (255, 255, 255)

one = (0, 0, 255)
two = (0, 128, 0)
three = (255, 0, 0)
four = (0, 0, 128)
five = (128, 0, 0)
bomb = (198, 198, 198)

start_x = 521
start_y = 406

x, y = p.position()
offset = 38
o = 18

done = [[False] * 16 for i in range(30)]
indexX = 0
indexY = 0


def get_color(x, y):
    return p.pixel(x, y)


def update_position():
    global x, y
    x, y = p.position()


def count_flags():
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


def reveal():
    if get_color(x - offset, y - offset) == blank and get_color(x - offset - o, y - offset - o) == white:
        p.moveTo(x - offset, y - offset)
        p.leftClick()
    if get_color(x - offset, y) == blank and get_color(x - offset - o, y - o) == white:
        p.moveTo(x - offset, y)
        p.leftClick()
    if get_color(x, y - offset) == blank and get_color(x - o, y - offset - o) == white:
        p.moveTo(x, y - offset)
        p.leftClick()
    if get_color(x - offset, y + offset) == blank and get_color(x - offset - o, y + offset - o) == white:
        p.moveTo(x - offset, y + offset)
        p.leftClick()
    if get_color(x, y + offset) == blank and get_color(x - o, y + offset - o) == white:
        p.moveTo(x, y + offset)
        p.leftClick()
    if get_color(x + offset, y + offset) == blank and get_color(x + offset - o, y + offset - o) == white:
        p.moveTo(x + offset, y + offset)
        p.leftClick()
    if get_color(x + offset, y) == blank and get_color(x - o + offset, y - o) == white:
        p.moveTo(x + offset, y)
        p.leftClick()
    if get_color(x + offset, y - offset) == blank and get_color(x + offset - o, y - offset - o) == white:
        p.moveTo(x + offset, y - offset)
        p.leftClick()
    p.moveTo(x, y)


def count_hidden():
    result = 0
    if get_color(x - offset, y - offset) == blank and get_color(x - offset - o, y - offset - o) == white:
        result += 1
    if get_color(x - offset, y) == blank and get_color(x - offset - o, y - o) == white:
        result += 1
    if get_color(x, y - offset) == blank and get_color(x - o, y - offset - o) == white:
        result += 1
    if get_color(x - offset, y + offset) == blank and get_color(x - offset - o, y + offset - o) == white:
        result += 1
    if get_color(x, y + offset) == blank and get_color(x - o, y + offset - o) == white:
        result += 1
    if get_color(x + offset, y + offset) == blank and get_color(x + offset - o, y + offset - o) == white:
        result += 1
    if get_color(x + offset, y) == blank and get_color(x - o + offset, y - o) == white:
        result += 1
    if get_color(x + offset, y - offset) == blank and get_color(x + offset - o, y - offset - o) == white:
        result += 1
    return result


def mark_hidden():
    if get_color(x - offset, y - offset) == blank and get_color(x - offset - o, y - offset - o) == white:
        p.moveTo(x - offset, y - offset)
        p.rightClick()
    if get_color(x - offset, y) == blank and get_color(x - offset - o, y - o) == white:
        p.moveTo(x - offset, y)
        p.rightClick()
    if get_color(x, y - offset) == blank and get_color(x - o, y - offset - o) == white:
        p.moveTo(x, y - offset)
        p.rightClick()
    if get_color(x - offset, y + offset) == blank and get_color(x - offset - o, y + offset - o) == white:
        p.moveTo(x - offset, y + offset)
        p.rightClick()
    if get_color(x, y + offset) == blank and get_color(x - o, y + offset - o) == white:
        p.moveTo(x, y + offset)
        p.rightClick()
    if get_color(x + offset, y + offset) == blank and get_color(x + offset - o, y + offset - o) == white:
        p.moveTo(x + offset, y + offset)
        p.rightClick()
    if get_color(x + offset, y) == blank and get_color(x - o + offset, y - o) == white:
        p.moveTo(x + offset, y)
        p.rightClick()
    if get_color(x + offset, y - offset) == blank and get_color(x + offset - o, y - offset - o) == white:
        p.moveTo(x + offset, y - offset)
        p.rightClick()
    p.moveTo(x, y)


def done_tile():
    if get_color(x - offset, y - offset) == blank and get_color(x - offset - o, y - offset - o) == white:
        return False
    if get_color(x - offset, y) == blank and get_color(x - offset - o, y - o) == white:
        return False
    if get_color(x, y - offset) == blank and get_color(x - o, y - offset - o) == white:
        return False
    if get_color(x - offset, y + offset) == blank and get_color(x - offset - o, y + offset - o) == white:
        return False
    if get_color(x, y + offset) == blank and get_color(x - o, y + offset - o) == white:
        return False
    if get_color(x + offset, y + offset) == blank and get_color(x + offset - o, y + offset - o) == white:
        return False
    if get_color(x + offset, y) == blank and get_color(x - o + offset, y - o) == white:
        return False
    if get_color(x + offset, y - offset) == blank and get_color(x + offset - o, y - offset - o) == white:
        return False
    return True


def solve():
    if get_color(x + offset, y) != blank and get_color(x + offset, y) != flag:
        p.moveTo(x + offset, y)
    elif get_color(x, y + offset) != blank and get_color(x, y + offset) != flag:
        p.moveTo(x, y + offset)
    elif get_color(x - offset, y) != blank and get_color(x - offset, y) != flag:
        p.moveTo(x - offset, y)
    elif get_color(x, y - offset) != blank and get_color(x, y - offset) != flag:
        p.moveTo(x, y - offset)
    else:
        if (x + offset) > 1623:
            p.moveTo(start_x, y + offset)
        elif (y + offset) > 978:
            p.moveTo(start_x, start_y)
        else:
         p.move(offset, 0)
    update_position()
    #if done[indexX][indexY]:
    #   return False
    if get_color(x, y) == blank or get_color(x, y) == flag:
        return False
    elif get_color(x, y) == bomb:
        return True
    else:
        if get_color(x, y) == one:
            number = 1
        elif get_color(x, y) == two:
            number = 2
        elif get_color(x, y) == three:
            number = 3
        elif get_color(x, y) == four:
            number = 4
        elif get_color(x, y) == five:
            number = 5
        else:
            return True
    flag_counted = count_flags()
    hidden_count = count_hidden()
    # print(f"number: {number},flags: {flag_counted},hidden:  {hidden_count}")
    if flag_counted == number:
        reveal()
    if hidden_count + flag_counted == number:
        mark_hidden()
    if done_tile():
        done[indexX][indexY] = True
    return False


def main():
    time.sleep(2)
    #for i in range(5):
    #    p.moveTo(random.randint(start_x, 1605), random.randint(start_y, 996))
    #    p.leftClick()
    p.moveTo(start_x, start_y)
    p.leftClick()
    update_position()
    free = True
    while free:
        if solve():
            free = False


if __name__ == '__main__':
    main()
