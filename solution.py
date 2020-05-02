"""
Sudoku solver
"""
from utils import SudokuUtils

# Initialise
sudoku = SudokuUtils()
unitlist = sudoku.get_unit_list()
units = sudoku.extract_units(unitlist, sudoku.boxes)
peers = sudoku.extract_peers(units, sudoku.boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    """
    # Find boxes with only 2 unfilled squares
    candidates = [box for box in values.keys() if len(values[box]) == 2]

    # Collect boxes having the same elements
    twins = [
        [box1, box2]
        for box1 in candidates
        for box2 in peers[box1]
        if set(values[box1]) == set(values[box2])
    ]

    # Find the 2 boxes with common peers
    for box1, box2 in twins:
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        common_peers = peers1.intersection(peers2)

        # delete the two digits from the above boxes
        for peer in common_peers:
            for rm_val in values[box1]:
                values = sudoku.assign_value(values, peer, values[peer].replace(rm_val, ''))

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            sudoku.assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in '123456789':
            digit_place = [box for box in unit if digit in values[box]]
            if len(digit_place) == 1:
                sudoku.assign_value(values, digit_place[0], digit)

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False

    while not stalled:
        # Get the number of boxes with solved square
        before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply the 2 strategies
        values = eliminate(values)
        values = only_choice(values)

        # Check if there's any new solved square
        after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = before == after

        # Check if there's a box with all unsolved squares
        if [box for box in values.keys() if not values[box]]:
            return False

    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    # Apply the above strategies to fill values in as much as possible
    values = reduce_puzzle(values)

    if not values:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    unfilled = [(len(v), k) for k, v in values.items() if len(v) > 1]

    # Return current board if all cells are filled
    if not unfilled:
        return values

    min_box = min(unfilled)[1]

    # Apply recursion to solve each one of the resulting sudokus
    original = values.copy()

    for element in values[min_box]:
        values = original.copy()
        values[min_box] = element
        values = search(values)

        # if one returns a value (not False), return it which is also the answer
        if values:
            return values


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = sudoku.grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    DIAG_SUDOKU_GRID = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku.display(sudoku.grid2values(DIAG_SUDOKU_GRID))
    result = solve(DIAG_SUDOKU_GRID)
    sudoku.display(result)

    try:
        import pysudoku
        pysudoku.play(sudoku.grid2values(DIAG_SUDOKU_GRID), result, sudoku.history)

    except SystemExit:
        pass
