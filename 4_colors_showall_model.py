import curses
import random
import math

"""
utility function to initialize color pairs.
return the color set in a dictionary
"""
def colordict():

    # initialize the color pair
    curses.start_color()
    curses.use_default_colors()
    color_perrow = 16

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        # pair number, foreground color, background color
        curses.init_pair(i + 1, i, -1)

    # black on red background
    curses.init_pair(300, 0, 9)

    return {
        "cover": curses.color_pair(9), # grey
        "flag": curses.color_pair(12), # yellow
        "blasted": curses.color_pair(300),
        #"-1": curses.color_pair(16),
        "-1": curses.color_pair(53),
        "0": curses.color_pair(1), 
        "1": curses.color_pair(13), # blue
        "2": curses.color_pair(48), # Green
        "3": curses.color_pair(10), # red
        "4": curses.color_pair(52), # 
        "5": curses.color_pair(94), # 
        "6": curses.color_pair(203), # 
        "7": curses.color_pair(90), # 
        "8": curses.color_pair(178), # 
    }

"""
this function will paint the cell based on the number of bombs
and the cell status: covered, revealed, flagged.

hare are list of characters we can use.
 ✸ 10040 ❂ 10050 ✹ 10041
 █ 9608 ◼ 9724
 ⚑ 9873
"""
def paintcell(stdscr, cell, colors, reverse=False, show=False):

    # check if need show all
    if show:
        status = "revealed"
    else:
        status = cell[3]

    # get the character for the cell based on the cell's status.
    # cell's status stored as the 3rd item.
    if status == 'covered':
        cell_ch = chr(9608)
        cell_color = colors['cover']
    elif status == 'flagged':
        cell_ch = chr(9873)
        cell_color = colors['flag']
    elif status == 'blasted':
        cell_ch = chr(10041)
        cell_color = colors['blasted']
    else:
        if cell[2] < 0:
            cell_ch = chr(10041)
            cell_color = colors["-1"]
        else:
            cell_ch = str(cell[2])
            cell_color = colors[cell_ch]

    if reverse:
        stdscr.addstr(cell[0], cell[1], cell_ch, curses.A_REVERSE)
    else:
        stdscr.addstr(cell[0], cell[1], cell_ch, cell_color)

# the main function
def sweeper(stdscr):

    # set 0 to hide the cursor.
    curses.curs_set(0)

    colors = colordict()

    # get the size of the windown.
    sh, sw = stdscr.getmaxyx()
    # set the center. [y-axis, x-axis]
    center = [sh // 2, sw // 2]

    # paint the minefield.
    # set size of the field, by row x column
    field_size = [20, 36] # [16, 30]
    # the initial minefield with 2 cells in the first row.
    field = []
    # using row (r) and column (c) for index.
    r, c = 0, 0
    # paint the row (y-axis) one after another.
    for y in range(center[0] - field_size[0] // 2, 
                   center[0] + field_size[0] // 2):
        # paint the column (x-axis) with one cell empty
        # so it will be step in 2 instead of 1
        field.append([[0, 0, 0, 0]] * field_size[1])
        for x in range(center[1] - field_size[1],
                       center[1] + field_size[1], 2):
            field[r][c] = [y, x, 0, 'covered']
            #stdscr.addstr(y, x, cell_ch, colors["cover"])
            paintcell(stdscr, field[r][c], colors)
            # increase the column index.
            c = c + 1
        # increase the row.
        r = r + 1
        # reset the column index.
        c = 0

    # Generate values for the minefield:
    # number of bombs 
    # - -1 bomb cell
    # - 0 - 8 bomb-free cell, the number will tell the total number of mines
    #   in the surrounding cells.
    # decide how many mines we will burry into the field.
    # 20% of total cells will be an expert level.
    # so we start with 12%, which is 1/8 of the total cells.
    # set variable i to count mines
    i = 0
    while i < math.prod(field_size) // 7:
        # generate a random number less than the total number of cells
        index = random.randint(0, math.prod(field_size) - 1)
        # calculate the row by divide the column size
        r = index // field_size[1]
        c = index - r * field_size[1]
        if field[r][c][2] == -1:
            # there is already a bomb in this cell.
            continue
        else:
            field[r][c][2] = -1
            # increase the bomb count.
            i = i + 1

    # calcute the number of bombs in surrounding cells.
    for y in range(0, field_size[0]):
        for x in range(0, field_size[1]):
            if field[y][x][2] == -1:
                # this cell al ready filled with bomb.
                paintcell(stdscr, field[y][x], colors, False, True)
                continue # skip...

            # looking for the surrounding cells.
            for sy in range(y - 1, y + 1 + 1):
                for sx in range(x - 1, x + 1 + 1):
                    if (sy < 0 or sy >= field_size[0] or
                        sx < 0 or sx >= field_size[1]):
                        # out of field.
                        continue # just skip
                    elif sy == y and sx == x:
                        # this is itself
                        continue # just skip
                    else:
                        if field[sy][sx][2] == -1:
                            # this cell filled with mine.
                            field[y][x][2] = field[y][x][2] + 1

            # Paint the number for quick test.
            paintcell(stdscr, field[y][x], colors, False, True)
            #n = str(field[y][x][2])
            #stdscr.addstr(field[y][x][0], field[y][x][1], n, colors[n])

    # paint the reverse cell to show the cursor!
    # set current row and column.
    r, c = 0, 0
    # paint the reverse cell for the first cell.
    #stdscr.addstr(field[r][c][0], field[r][c][1], cell_ch, curses.A_REVERSE)
    paintcell(stdscr, field[r][c], colors, True, True)
    nr, nc = 0, 0

    # try move the cursors
    while True:
        # collect user's input.
        user_key = stdscr.getch()

        # exit when user press ESC
        if user_key == 27:
            break;

        # decide the new head based on the direction
        if user_key in [curses.KEY_UP, 107]:
            # k (107) for up
            if r > 0:
                nr = r - 1
        elif user_key in [curses.KEY_DOWN, 106]:
            # j (106) for down
            if r < field_size[0] - 1:
                nr = r + 1
        elif user_key in [curses.KEY_RIGHT, 108]:
            # l (108) for right
            if c < field_size[1] - 1:
                nc = c + 1
        elif user_key in [curses.KEY_LEFT, 104]:
            # h (104) for left
            if c > 0:
                nc = c - 1

        if nr == r and nc == c:
            # nothing change,
            continue
        else:
            # paint current spot normally
            #stdscr.addstr(field[r][c][0], field[r][c][1], cell_ch)
            paintcell(stdscr, field[r][c], colors, False, True)
            # paint the new spot reverse.
            #stdscr.addstr(field[nr][nc][0], field[nr][nc][1], cell_ch, curses.A_REVERSE)
            paintcell(stdscr, field[nr][nc], colors, True, True)
            # set the current spot to new spot.
            r, c = nr, nc

    #stdscr.getch()

curses.wrapper(sweeper)
