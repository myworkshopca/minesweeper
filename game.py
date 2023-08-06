import curses
import random
import math

"""
"""
def initfield(center, field_size):

    field = []
    # using row (r) and column (c) for index.
    r, c = 0, 0
    # paint the row (y-axis) one after another.
    for y in range(center[0] - field_size[0] // 2, 
                   center[0] + field_size[0] // 2):
        # paint the column (x-axis) with one cell empty
        # so it will be step in 2 instead of 1
        #field.append([[0, 0, 0, 0]] * field_size[1])
        field.append([])
        for x in range(center[1] - field_size[1],
                       center[1] + field_size[1], 2):
            #field[r][c] = [y, x, 0, 'covered']
            field[r].append([y, x, 0, 'covered'])
            #stdscr.addstr(y, x, cell_ch, colors["cover"])
            #paintcell(stdscr, field[r][c], colors)
            # increase the column index.
            #c = c + 1
        # increase the row.
        r = r + 1
        # reset the column index.
        #c = 0

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
                # paint in showall mode to debug
                #paintcell(stdscr, field[y][x], colors, False, True)
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
            #paintcell(stdscr, field[y][x], colors, False, True)

    return field

"""
paint the whole field.
"""
def paintfield(stdscr, field, size, colors, show=False):

    for r in range(0, size[0]):
        for c in range(0, size[1]):
            paintcell(stdscr, field[r][c], colors, False, show)
            #stdscr.addstr(field[r][c][0], field[r][c][1], chr(9608), colors['cover'])
            #if field[r][c][2] == -1:
            #    stdscr.addstr(field[r][c][0], field[r][c][1], chr(10041))
            #else:
            #    stdscr.addstr(field[r][c][0], field[r][c][1], str(field[r][c][2]))

"""
utility function to initialize color pairs.
return the color set in a dictionary
"""
def colordict():

    # initialize the color pair
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
    #for i in range(0, 20):
        # pair number, foreground color, background color
        if i == 232:
            # black on red background
            curses.init_pair(i + 1, i, curses.COLOR_RED)
        else:
            curses.init_pair(i + 1, i, -1)
            #curses.init_pair(i + 1, i, 241)

    return {
        "cover": curses.color_pair(16), # 9: grey, 16:white
        "flag": curses.color_pair(227), # 12, 227, yellow
        "blasted": curses.color_pair(233),
        #"-1": curses.color_pair(16),
        "-1": curses.color_pair(53),
        "0": curses.color_pair(239), # 1, 190
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
 ✸ 10040 ❂ 10050 ✹ 10041 ❄ 10052 ❋ 10059
 █ 9608 ◼ 9724
 ⚑ 9873 ☂ 9730
"""
def paintcell(stdscr, cell, colors, reverse=False, show=False):

    # check if need show all
    if show and cell[3] == 'covered':
        # set the status to revealed for all covered cells.
        #status = "revealed"
        # update cell status to revealed.
        cell[3] = "revealed"

    status = cell[3]

    # get the character for the cell based on the cell's status.
    # cell's status stored as the 3rd item.
    if status == 'covered':
        cell_ch = chr(9608)
        cell_color = colors['cover']
    elif status == 'flagged':
        #cell_ch = chr(9873)
        cell_ch = chr(9730)
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

"""
dig a cell
"""
def digcell(cell):

    if cell[3] in ['flagged', 'revealed']:
        # do nothing if cell is flagged or revealed!
        return

    # check if this cell is a bomb
    if cell[2] < 0:
        # set the cell's status to blasted!
        cell[3] = "blasted"
    else:
        cell[3] = "revealed"

"""
flag a cell
"""
def flagcell(cell):

    # check and flip cell's status.
    if cell[3] == 'covered':
        cell[3] = 'flagged'
    elif cell[3] == 'flagged':
        cell[3] = 'covered'
    # we will NOT do anything for other status.

"""
open surrounding cells except the flagged cell.
"""
def opensurrounding(stdscr, colors, field, field_size, y, x):

    # TODO: check if there are correct flagged cells currounding.
    # if the number of bombs for the current cell is NOT match
    # the flagged cells we will not reveal any!
    flagged = 0
    for sy in [y - 1, y, y + 1]:
        for sx in [x - 1, x, x + 1]:
            if (sy < 0 or sy >= field_size[0] or
                sx < 0 or sx >= field_size[1]):
                # out of field.
                continue # just skip
            elif sy == y and sx == x:
                # this is itself
                continue # just skip
            elif field[sy][sx][3] == "flagged":
                flagged = flagged + 1

    if field[y][x][2] != flagged:
        return

    # looping through the surrounding cells.
    for sy in range(y - 1, y + 1 + 1):
        for sx in range(x - 1, x + 1 + 1):
            if (sy < 0 or sy >= field_size[0] or
                sx < 0 or sx >= field_size[1]):
                # out of field.
                continue # just skip
            elif sy == y and sx == x:
                # this is itself
                continue # just skip
            elif field[sy][sx][3] == "flagged":
                # this cell is flagged, skip
                continue
            elif field[sy][sx][3] == "revealed":
                # this cell is revealed, skip
                continue
            elif field[sy][sx][2] == -1:
                # blasted. set status.
                field[sy][sx][3] = 'blasted'
                # call game over.
                gameover(stdscr, field, field_size, colors)
            elif field[sy][sx][2] == 0:
                # update status first
                field[sy][sx][3] = 'revealed'
                # number of bombs surrounding is 0
                # tells there is no bombs around.
                # So we open all surroundings.
                # call itself again.
                opensurrounding(stdscr, colors, field, field_size, sy, sx)
            else:
                # set status to revealed.
                field[sy][sx][3] = 'revealed'

            # repaint this surrounding cell normally
            paintcell(stdscr, field[sy][sx], colors)

"""
Game over logic
"""
def gameover(stdscr, field, size, colors):

    # TODO: set all cells revealed

    # show the field with all cells revealed!
    paintfield(stdscr, field, size, colors, True)
    return

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
    field_size = [16, 30] # [16, 30]

    # the initial minefield with 2 cells in the first row.
    field = initfield(center, field_size)

    # paint the whole field covered.
    paintfield(stdscr, field, field_size, colors)

    # paint the reverse cell to show the cursor!
    # set current row and column.
    r, c = 0, 0
    # paint the reverse cell for the first cell.
    #stdscr.addstr(field[r][c][0], field[r][c][1], cell_ch, curses.A_REVERSE)
    paintcell(stdscr, field[r][c], colors, True)
    nr, nc = 0, 0

    # try move the cursors
    while True:
        # collect user's input.
        user_key = stdscr.getch()

        # exit when user press ESC q or Q
        if user_key in [27, 113, 81]:
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
        elif user_key in [100, 110, 117]:
            # letter d (100) or n (110), u (117) will do dig.
            digcell(field[r][c])
            # repaint after dig!
            paintcell(stdscr, field[r][c], colors, True)
            if field[r][c][3] == 'blasted':
                # game over
                gameover(stdscr, field, field_size, colors)
            elif field[r][c][3] == 'revealed' and field[r][c][2] == 0:
                opensurrounding(stdscr, colors, field, field_size, r, c)
        elif user_key in [102, 105]:
            # letter f (102) or i (105) flag / unflag cell.
            flagcell(field[r][c])
            # repaint after flag!
            paintcell(stdscr, field[r][c], colors, True)
        elif user_key == 32:
            # white space (32) reveal all surrounding cells.
            if field[r][c][3] == 'revealed':
                # only open the revealed cell.
                opensurrounding(stdscr, colors, field, field_size, r, c)

        if nr == r and nc == c:
            # nothing change,
            continue
        else:
            # paint current spot normally
            paintcell(stdscr, field[r][c], colors, False)
            # paint the new spot reverse.
            paintcell(stdscr, field[nr][nc], colors, True)
            # set the current spot to new spot.
            r, c = nr, nc

    #stdscr.getch()

curses.wrapper(sweeper)
# the simple way to check the field value we generated.
#field = initfield([10, 10], [2, 2])
#print(field)
