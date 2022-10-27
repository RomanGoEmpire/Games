# Website https://minesweeper.online/de
# size 38
import collections
import random
import time

import pyautogui as p

# minesweeper.online
blank = (198, 198, 198)
flag = (0, 0, 0)
white = (255, 255, 255)

one = (0, 0, 255)
two = (0, 128, 0)
three = (255, 0, 0)
four = (0, 0, 128)
five = (128, 0, 0)
bomb = (37, 41, 36)

start_x = 521
start_y = 406
end_x = 1623
end_y = 996
offset = 38
o = 18
rows = 30
cols = 16

current_row = 0
current_col = 0

tiles_x = collections.deque()
tiles_y = collections.deque()
tiles_to_solve = []

running = True


def initialize_tiles():
    global tiles_x, tiles_y
    tiles_x = collections.deque()
    tiles_y = collections.deque()
    for j in range(cols):
        tiles_y.append(start_y + j * offset)
    for i in range(rows):
        tiles_x.append(start_x + i * offset)


def initialize_tiles_to_solve():
    global tiles_to_solve
    tiles_to_solve = []
    for i in range(rows):
        tiles_to_solve.append([])
        for j in range(cols):
            tiles_to_solve[i].append(True)


initialize_tiles()
initialize_tiles_to_solve()


def get_color(x, y):
    return p.pixel(x, y)


def get_name(row, col):
    color = get_color(tiles_x[row], tiles_y[col])
    if color == blank:
        if get_color(tiles_x[row] - o, tiles_y[col] - o) == white:
            return "hidden"
        return "blank"
    elif color == one:
        return "one"
    elif color == two:
        return "two"
    elif color == three:
        return "three"
    elif color == four:
        return "four"
    elif color == five:
        return "five"
    elif color == bomb:
        return "bomb"
    elif color == flag:
        return "flag"
    else:
        return "unknown"


def get_neighbors(row, col):
    neighbors = []
    if row - 1 >= 0:
        if col - 1 >= 0:
            neighbors.append(get_name(row - 1, col - 1))
        else:
            neighbors.append("Null")
        neighbors.append(get_name(row - 1, col))
    else:
        neighbors.append("Null")
        neighbors.append("Null")
    if col + 1 < cols - 1:
        if row - 1 >= 0:
            neighbors.append(get_name(row - 1, col + 1))
        neighbors.append(get_name(row, col + 1))
    if row + 1 < rows - 1:
        if col + 1 < cols - 1:
            neighbors.append(get_name(row + 1, col + 1))
        neighbors.append(get_name(row + 1, col))

    if col - 1 >= 0:
        if row + 1 < rows - 1:
            neighbors.append(get_name(row + 1, col - 1))
        else:
            neighbors.append("Null")
        neighbors.append(get_name(row, col - 1))
    else:
        neighbors.append("Null")
        neighbors.append("Null")
    return neighbors


def flag_tiles(row, col, neighbors):
    for i in range(len(neighbors)):
        if neighbors[i] == "hidden":
            row_offset = 0
            col_offset = 0
            if i == 0:
                row_offset = -1
                col_offset = -1
            elif i == 1:
                row_offset = -1
                col_offset = 0
            elif i == 2:
                row_offset = -1
                col_offset = 1
            elif i == 3:
                row_offset = 0
                col_offset = 1
            elif i == 4:
                row_offset = 1
                col_offset = 1
            elif i == 5:
                row_offset = 1
                col_offset = 0
            elif i == 6:
                row_offset = 1
                col_offset = -1
            elif i == 7:
                row_offset = 0
                col_offset = -1
            if row + offset > 0 and col + offset > 0:
                p.moveTo(tiles_x[row + row_offset], tiles_y[col + col_offset])
                p.rightClick()
                tiles_to_solve[row + row_offset][col + col_offset] = False


def flag_or_reveal(new_number, row, col):
    neighbors = get_neighbors(row, col)
    flags = neighbors.count("flag")
    hidden_tiles = neighbors.count("hidden")
    if hidden_tiles + flags == new_number:
        flag_tiles(row, col, neighbors)
        tiles_to_solve[row][col] = False
        check_neighbors(col, neighbors, new_number, row)
    elif flags == new_number and hidden_tiles > 0:
        p.moveTo(tiles_x[row], tiles_y[col])
        p.leftClick()
        tiles_to_solve[row][col] = False
        # flag or reveal for adjacent tiles
        check_neighbors(col, neighbors, new_number, row)


def check_neighbors(col, neighbors, new_number, row):
    for i in range(len(neighbors)):
        if neighbors[i] == "hidden" or neighbors[i] == "blank" or neighbors[i] == "flag":
            continue
        elif neighbors[i] == "one":
            new_number = 1
        elif neighbors[i] == "two":
            new_number = 2
        elif neighbors[i] == "three":
            new_number = 3
        elif neighbors[i] == "four":
            new_number = 4
        elif neighbors[i] == "five":
            new_number = 5
        row_offset = 0
        col_offset = 0
        if i == 0:
            row_offset = -1
            col_offset = -1
        elif i == 1:
            row_offset = -1
            col_offset = 0
        elif i == 2:
            row_offset = -1
            col_offset = 1
        elif i == 3:
            row_offset = 0
            col_offset = 1
        elif i == 4:
            row_offset = 1
            col_offset = 1
        elif i == 5:
            row_offset = 1
            col_offset = 0
        elif i == 6:
            row_offset = 1
            col_offset = -1
        elif i == 7:
            row_offset = 0
            col_offset = -1
        if row + offset > 0 and col + offset > 0:
            flag_or_reveal(new_number, row + row_offset, col + col_offset)


def solve():
    # If there are no more tiles to solve, then we are done
    need_to_solve = rows * cols
    for row in tiles_to_solve:
        need_to_solve -= row.count(False)
    if need_to_solve <= 0:
        global running
        running = False
        return
    # is this tile solved yet? If not, then solve it
    global current_row, current_col
    if tiles_to_solve[current_row][current_col]:
        p.moveTo(tiles_x[current_row], tiles_y[current_col])
        name = get_name(current_row, current_col)
        if name == "one":
            flag_or_reveal(1, current_row, current_col)
        elif name == "two":
            flag_or_reveal(2, current_row, current_col)
        elif name == "three":
            flag_or_reveal(3, current_row, current_col)
        elif name == "four":
            flag_or_reveal(4, current_row, current_col)
        elif name == "five":
            flag_or_reveal(5, current_row, current_col)
        elif name == "bomb":
            print(current_row, current_col)
            print("BOOM!")
            running = False
            return
        elif name == "blank":
            tiles_to_solve[current_row][current_col] = False
        elif name == "flag":
            tiles_to_solve[current_row][current_col] = False
        # move to the next tile
    if current_row + 1 < rows:
        current_row += 1
    elif current_col + 1 < cols:
        current_row = 0
        current_col += 1
    else:
        current_row = 0
        current_col = 0


def main():
    # time.sleep(2)
    for i in range(5):
        x, y = random.randint(0, len(tiles_x) - 1), random.randint(0, len(tiles_y) - 1)
        p.moveTo(tiles_x[x], tiles_y[y])
        p.leftClick()
        if get_name(x, y) == "bomb":
            p.moveTo(1050, 350)
            p.leftClick()
            main()
            break
    while running:
        solve()


if __name__ == '__main__':
    main()
