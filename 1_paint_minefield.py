import curses
import random

def sweeper(stdscr):

    # set 0 to hide the cursor.
    curses.curs_set(0)

    # get the size of the windown.
    sh, sw = stdscr.getmaxyx()
    # set the center. [y-axis, x-axis]
    center = [sh // 2, sw // 2]

    # define the char for cell ◼ is 9724
    cell_ch = chr(9724)

    # paint the minefield.
    # set size of the field.
    field_size = 10
    # the initial mine field with 2 cells in the first row.
    field = []
    # using row (r) and column (c) for index.
    r, c = 0, 0
    # we paint the row (y-axis) one after another.
    for y in range(center[0] - field_size, center[0] + field_size):
        # we paint the column (x-axis) with one cell empty
        field.append([[0,0]] * field_size * 2)
        for x in range(center[1] - field_size * 2, center[1] + field_size * 2, 2):
            field[r][c] = [y, x]
            stdscr.addstr(y, x, cell_ch)
            # increase the column index.
            c = c + 1
        # increase the row.
        r = r + 1
        # reset the column index.
        c = 0

    # paint the reverse cell for the first cell.
    stdscr.addstr(field[0][0][0], field[0][0][1], cell_ch, curses.A_REVERSE)

    # try move the cursors
    while True:

        user_key = stdscr.getch()

    stdscr.getch()

curses.wrapper(sweeper)
