assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins. Here we are solving only for twins, not for triplets or quads
    from collections import Counter
    for unit in unitlist:
        val_l = []
        for y in unit:
            if len(values[y]) == 2:
                val_l += [values[y]]
        a = [k for k, v in Counter(val_l).items() if v == 2]
        # Eliminate the naked twins as possibilities for their peers
        for y in unit:
            for z in a:
                ##Deparce twins into simple numbers
                for yy in z:
                    # Eliminate the naked twins
                    if yy in values[y] and len(values[y])>2:
                        values[y] = values[y].replace(yy,'')
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units =  [[boxes[i] for i in range(0,81,10)] ,  [boxes[i] for i in range(8,80,8)]] # add additional constraints
unitlist = row_units + column_units + square_units + diag_units # including the diagonals constr here
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    for i, j in values.items():
        if len(j) ==1:
            key_list =peers[i]
            for x in key_list:
                values[x]=values[x].replace(j,'')
    return values

def only_choice(values):
    from collections import Counter
    for unit in unitlist:
        val_l = []
        a = []
        for y in unit:
            # Calculate Nb of occurrences of each value inside unit
            val_l += values[y]
        #Create list of Nb there are unique
        a = [k for k, v in Counter(val_l).items() if v == 1]
        for y in unit:
            for z in a:
                #replace number in boxes where is unique value by this value
                if z in values[y]:
                    values[y] = z
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        # Your code here: Use the Naked Twins Strategy
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    vlen = 0
    for ivalue in values.values():
        vlen += len(ivalue)
    if vlen == 81:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    min_length=9
    for key,value in values.items():
            if len(value)<=min_length and len(value)>1 :
                min_key = key
                min_length = len(value)
    # Recursion to try to solve it by tree searching
    for value in values[min_key]:
        new_values = values.copy()
        new_values[min_key]=value
        solvef = search(new_values)
        if solvef:
            return solvef

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #translate from string representation to dict to solve it further
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
