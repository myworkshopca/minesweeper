
center = [60, 20]
# set size of the field.
field_size = 2 
# the initial mine field with 2 cells in the first row.
field = []
#print(field)
# using row (r) and column (c) for index.
r = 0
c = 0
# we paint the row (y-axis) one after another.
for y in range(center[0] - field_size, center[0] + field_size):
    # append new row
    #field.append([])
    field.append([[0,0]] * field_size * 2)
    print(field)
    # we paint the column (x-axis) with one cell empty
    for x in range(center[1] - field_size * 2,
                   center[1] + field_size * 2, 2):
        print('r={}, c={}, y={}, x={}'.format(r, c, y, x))
        field[r][c]= [y, x]
        print(field)
        # increase the column index.
        c = c + 1
    # increase the row.
    r = r + 1
    # reset column.
    c = 0
