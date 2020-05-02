"""
Utility functions for sudoku solver
"""
from collections import defaultdict


class SudokuUtils:
    def __init__(self, rows='ABCDEFGHI', cols='123456789', history={}):
        self.rows = rows
        self.cols = cols
        self.history = history
        self.boxes = self.cross(self.rows, self.cols)

    def display(self, values):
        """Display the values as a 2-D grid.

        Parameters
        ----------
            values(dict): The sudoku in dictionary form
        """
        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for row in self.rows:
            print(''.join(
                values[row + col].center(width) + ('|' if col in '36' else '')
                for col in self.cols
            ))

            if row in 'CF':
                print(line)
        print()

    def assign_value(self, values, box, value):
        """You must use this function to update your values dictionary if you want to
        try using the provided visualization tool. This function records each assignment
        (in order) for later reconstruction.

        Parameters
        ----------
        values(dict)
            a dictionary of the form {'box_name': '123456789', ...}

        Returns
        -------
        dict
            The values dictionary with the naked twins eliminated from peers
        """
        # Don't waste memory appending actions that don't actually change any values
        if values[box] == value:
            return values

        prev = self.values2grid(values)
        values[box] = value
        if len(value) == 1:
            self.history[self.values2grid(values)] = (prev, (box, value))
        return values

    def values2grid(self, values):
        """Convert the dictionary board representation to as string

        Parameters
        ----------
        values(dict)
            a dictionary of the form {'box_name': '123456789', ...}

        Returns
        -------
        a string representing a sudoku grid.

            Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        """
        res = []
        for row in self.rows:
            for col in self.cols:
                fill_value = values[row + col]
                res.append(fill_value if len(fill_value) == 1 else '.')
        return ''.join(res)

    def grid2values(self, grid):
        """Convert grid into a dict of {square: char} with '123456789' for empties.

        Parameters
        ----------
        grid(string)
            a string representing a sudoku grid.

            Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

        Returns
        -------
            A grid in dictionary form
                Keys: The boxes, e.g., 'A1'
                Values: The value in each box, e.g., '8'. If the box has no value,
                then the value will be '123456789'.
        """
        sudoku_grid = {}
        for val, key in zip(grid, self.boxes):
            if val == '.':
                sudoku_grid[key] = '123456789'
            else:
                sudoku_grid[key] = val
        return sudoku_grid

    def reconstruct(self, values, history):
        """Returns the solution as a sequence of value assignments

        Parameters
        ----------
        values(dict)
            a dictionary of the form {'box_name': '123456789', ...}

        history(dict)
            a dictionary of the form {key: (key, (box, value))} encoding a linked
            list where each element points to the parent and identifies the value
            assignment that connects from the parent to the current state

        Returns
        -------
        list
            a list of (box, value) assignments that can be applied in order to the
            starting Sudoku puzzle to reach the solution
        """
        path = []
        prev = self.values2grid(values)
        while prev in history:
            prev, step = history[prev]
            path.append(step)
        return path[::-1]

    def get_unit_list(self):
        row_units = [self.cross(r, self.cols) for r in self.rows]
        column_units = [self.cross(self.rows, c) for c in self.cols]
        square_units = [
            self.cross(rs, cs)
            for rs in ('ABC', 'DEF', 'GHI')
            for cs in ('123', '456', '789')
        ]
        diagonal_units = (
            [[row + col for row, col in zip(self.rows, self.cols)]] +
            [[row + col for row, col in zip(self.rows, self.cols[::-1])]]
        )

        unitlist = row_units + column_units + square_units + diagonal_units

        return unitlist

    @staticmethod
    def extract_units(unitlist, boxes):
        """Initialize a mapping from box names to the units that the boxes belong to

        Parameters
        ----------
        unitlist(list)
            a list containing "units" (rows, columns, diagonals, etc.) of boxes

        boxes(list)
            a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

        Returns
        -------
        dict
            a dictionary with a key for each box (string) whose value is a list
            containing the units that the box belongs to (i.e., the "member units")
        """
        # the value for keys that aren't in the dictionary are initialized as an empty list
        units = defaultdict(list)
        for current_box in boxes:
            for unit in unitlist:
                if current_box in unit:
                    # defaultdict avoids this raising a KeyError when new keys are added
                    units[current_box].append(unit)
        return units

    @staticmethod
    def extract_peers(units, boxes):
        """Initialize a mapping from box names to a list of peer boxes (i.e., a flat list
        of boxes that are in a unit together with the key box)

        Parameters
        ----------
        units(dict)
            a dictionary with a key for each box (string) whose value is a list
            containing the units that the box belongs to (i.e., the "member units")

        boxes(list)
            a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

        Returns
        -------
        dict
            a dictionary with a key for each box (string) whose value is a set
            containing all boxes that are peers of the key box (boxes that are in a unit
            together with the key box)
        """
        # the value for keys that aren't in the dictionary are initialized as an empty list
        peers = defaultdict(set)  # set avoids duplicates
        for key_box in boxes:
            for unit in units[key_box]:
                for peer_box in unit:
                    if peer_box != key_box:
                        # defaultdict avoids this raising a KeyError when new keys are added
                        peers[key_box].add(peer_box)
        return peers

    @staticmethod
    def cross(A, B):
        """Cross product of elements in A and elements in B """
        return [x + y for x in A for y in B]
