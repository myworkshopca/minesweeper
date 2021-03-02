import curses
import random
import math

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
    # set size of the field, by row x column
    field_size = [16, 30]
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
            field[r][c] = [y, x, 0, 0]
            stdscr.addstr(y, x, cell_ch)
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
            stdscr.addstr(field[y][x][0], field[y][x][1], str(field[y][x][2]))

    # paint the reverse cell to show the cursor!
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
            if r < field_size[0] - 1:
                nr = r + 1
        elif user_key == curses.KEY_RIGHT:
            if c < field_size[1] - 1:
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
