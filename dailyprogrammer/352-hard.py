# -*- coding: utf-8 -*-

import re

class Well:
    """See https://www.reddit.com/r/dailyprogrammer/

    [2018-02-23] Challenge #352 [Hard] Well, Well, Well

    A square well is dug with a peculiar shape: each 1x1 section has varying
    heights above some floor. You wish to fill the well with water, filling
    from a hose above the square marked 1. Square 1 is the lowest (think of 
    this as a heightmap in units from the bottom). Water flows at 1 cubic 
    unit per unit time (e.g. 1 liter per minute if you want specific units).
    You wish to know when you fill a specific square.

    You can assume water behaves like it does in the real world - it 
    immediately disperses, evenly, to all accessible regions, and it cannot
    spontaneously leak from one square to another if there is no path.
    
    Assume a constant flow rate for the water.
    
    Today's question is - writing a program, can you tell at what time the
    well's target square is under a cubic unit of water? 
    """

    def __init__(self, args):
        self.cols = 0
        self.rows = 0
        self.squares = []
        self.target = 0 # The target square "M"
        self.time = 0
        self.parse_input(args)
        # Calculate this initially to avoid repetitive work:
        self.neighbours = self.get_neighbours(self.cols, self.rows)

    def parse_input(self, args):
        """You'll be given a row with two numbers, N and N, telling you the
        dimensions of the well. Then you'll be given N rows of N colums of
        unique numbers. Then you'll get one row with one number, M, telling
        you the target square to cover with one cubic unit of water.
        """
        self.squares = [int(v) for v in re.split('[ \n\r]+', args.strip())]
        (self.cols, self.rows, self.target) = (self.squares.pop(0), self.squares.pop(0), self.squares.index(self.squares.pop()))

    def get_neighbours(self, cols, rows):
        """Assuming realistic model, water can only flow through sides of
        squares, not diagonals.
        """
        neighbours = []
        cardinals = [(0, -1), (-1, 0), (0, 1), (1, 0)] # N/W/S/E
        for i in range(0, cols*rows):
            (x, y) = (i % cols, int(i / rows))
            coords = [(p[0] + x, p[1] + y) for p in cardinals] # Some might be out of bounds, so filter:
            neighbours.append([n[0] + n[1] * cols for n in coords if 0 <= n[0] < cols and 0 <= n[1] < rows])
        return neighbours

    def fill(self, square, min_square, visited):
        """Check neighbours that are not higher than the current square. 
        Return deepest square reached.
        """
        visited.add(square)

        for n in self.neighbours[square]:
            if self.squares[n] <= self.squares[square] and n not in visited:
                min_square = self.fill(n, min_square, visited)

        return square if self.squares[square] < self.squares[min_square] else min_square

    def solve(self):
        """Keep adding one unit of water to square 1 until the target square
        is incremented and there are no other squares to fill at that depth.
        In real life the squares will fill proportionally, but our model
        matches it at this iteration point.
        Return number of iterations ('time').
        """
        target_level = self.squares[self.target] + 1

        for self.time in range(0, 999_999): # Avoid infinite loop
            square = self.fill(0, 0, set())
            if self.squares[square] + 1 > target_level and self.squares[self.target] >= target_level:
                return self.time # Done!
            self.squares[square] += 1

        raise Exception('Iteration limit exceeded')

well_1 = Well("""
3 3
1 9 6
2 8 5
3 7 4
4
""") # 16

well_2 = Well("""
7 7
  38  33  11  48  19  45  22
  47  30  24  15  46  28   3
  14  13   2  34   8  21  17
  10   9   5  16  27  36  39
  18  32  20   1  35  49  12
  43  29   4  41  26  31  37
  25   6  23  44   7  42  40
35
""") # 589 

well_3 = Well("""
7 7
  15  16  46   1  38  43  44
  25  10   7   6  34  42  14
   8  19   9  21  13  23  22
  32  11  29  36   3   5  47
  31  33  45  24  12  18  28
  40  41  20  26  39  48   2
  49  35  27   4  37  30  17
26
""") # 316

print('Well 1 = {}'.format(well_1.solve()))
assert(well_1.time == 16)
print('Well 2 = {}'.format(well_2.solve()))
assert(well_2.time == 589)
print('Well 3 = {}'.format(well_3.solve()))
assert(well_3.time == 316)

# ----------------------------------------------------------------------------

def print_squares(well):
    """Pretty print a well.
    """
    print('')
    for r in range(0, well.rows):
        row = []
        for c in range(0, well.cols):
            i = r * well.cols + c
            row.append('{}{}  '.format(well.squares[i], '!' if i == well.target else '')[0:3])
        print(' '.join(row))
    print('Fill iterations: {}\n'.format(well.time))

# print_squares(well_1)
# print_squares(well_2)
# print_squares(well_3)
