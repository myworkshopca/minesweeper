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

    # set current row and column.
    r, c = 0, 0
    # paint the reverse cell for the first cell.
    stdscr.addstr(field[r][c][0], field[r][c][1], cell_ch, curses.A_REVERSE)
    nr, nc = 0, 0

    # try move the cursors
    while True:
        # collect user's input.
        user_key = stdscr.getch()

        # exit when user press ESC
        if user_key == 27:
            break;

        # decide the new head based on the direction
        if user_key == curses.KEY_UP:
            if r > 0:
                nr = r - 1
        elif user_key == curses.KEY_DOWN:
            if r < field_size * 2 - 1:
                nr = r + 1
        elif user_key == curses.KEY_RIGHT:
            if c < field_size * 2 - 1:
                nc = c + 1
        elif user_key == curses.KEY_LEFT:
            if c > 0:
                nc = c - 1

        if nr == r and nc == c:
            # nothing change,
            continue
        else:
            # paint current spot normally
            stdscr.addstr(field[r][c][0], field[r][c][1], cell_ch)
            # paint the new spot reverse.
            stdscr.addstr(field[nr][nc][0], field[nr][nc][1], cell_ch, curses.A_REVERSE)
            # set the current spot to new spot.
            r, c = nr, nc

    #stdscr.getch()

curses.wrapper(sweeper)
