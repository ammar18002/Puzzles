# pylint: disable=missing-docstring

# def sudoku_solver(grid):
"""Sudoku solver"""

len_grid = 9

def sudoku_validator(grid):
    """Sudoku solver"""
    valid_set = set(list(range(1, 10)))
    for row in grid:
        if set(row) != valid_set:
            return False

    for i in range(0,9):
        l_n = []
        for j in range(0,9):
            l_n.append(grid[i][j])
        if set(l_n) != valid_set:
                return False

# The first part (l_n = [...]) → collects the 3 rows of the sub-square (nested lists). #

    indexes = list(range(0, 9, 3))
    Len_rows = []
    for row in indexes:  # row = 0, 3, 6
        for col in indexes: # col = 0, 3, 6
             # I don't know why I wrote this
# Take 3 rows at a time (a horizontal band), then loop through each row inside it
            for item in grid[0 +row:3 +row]: #item = one row from the band of sudoku grid
                items = []
                for value in item[col:3 + col]: # <-- value = one number inside that row slice
                    items.append(value)
                Len_rows.append(items) # add the whole row-slice into the list

#The second part (concat_len = [...]) → flattens those 3 lists into 1 list of 9 values. #

    concat_len = [] # start empty
    for i in Len_rows: # i = one sublist
        for j in i: #j = one number inside that sublist
            concat_len.append(j)

    if set(concat_len) != valid_set:
        return False

    return True

def find_empty_cell(grid):
    for i in range(len_grid):
        for j in range(len_grid):
            if grid[i][j]==0:
                return (i, j)
    return None

def valid(grid, num, pos):  #pos(col, row)
    # Check row
    for i in range(len_grid):
        if grid[pos[0]][i] == num and pos[1] != i: # skip current cell
            # if the same number is found somewhere else in that row
            return False

     # Check column
    for i in range(len_grid):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box --- Converting nine by nine grid to 3 by 3 ---
    box_x = pos[1] // 3  # col band
    box_y = pos[0] // 3  # row band


    for i in range(box_y*3, box_y*3+3):  # ×3 jumps to the start of the 3×3 box
        for j in range(box_x*3, box_x*3+3):
            if grid[i][j] == num and (i, j) != pos: # pos is the tuple (row, col) of the cell we’re trying to fill.
                return False
    return True

def solve(grid):
    """Recursive call to solve until done"""
    # “Function calls itself on the next empty cell until the grid is solved or fails.”
    find = find_empty_cell(grid)
    if not find:
        return True

    row, col = find
    for i in range(1, 10):
        if valid(grid, i, (row, col)):
            grid[row][col] = i
            if solve(grid):
                return True
            grid[row][col] = 0
    return False

def sudoku_solver(grid):
    if not isinstance(grid, list):
        return 'invalid grid'

    for row in grid:
        if len(row) != len_grid:
            return 'invalid grid'
    if len(grid) != len_grid:
            return 'invalid grid'

    solve(grid) # Recursive call to solve until done
    return grid

### Wrapper ###

def sudoku_check_or_solve(grid):
    has_empty = any(0 in row for row in grid)
    if has_empty:
        print("🟡 Incomplete Sudoku detected")
        solved = sudoku_solver(grid)
        return solved
    else:
        print("🟢 Complete Sudoku detected")
        if sudoku_validator(grid):
            return "This Sudoku is valid ✅"
        else:
            return "This Sudoku is invalid ❌"

if __name__ == "__main__":
    print("Sudoku solver is running ✅")
