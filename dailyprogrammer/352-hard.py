# -*- coding: utf-8 -*-

import re

class Well:
    """See https://www.reddit.com/r/dailyprogrammer/comments/7zriir/20180223_challenge_352_hard_well_well_well/

    A square well is dug with a peculiar shape: each 1x1 section has varying heights above some floor. You wish to fill the well with water, filling from a hose above the square marked 1. Square 1 is the lowest (think of this as a heightmap in units from the bottom). Water flows at 1 cubic unit per unit time (e.g. 1 liter per minute if you want specific units). You wish to know when you fill a specific square.

    You can assume water behaves like it does in the real world - it immediately disperses, evenly, to all accessible regions, and it cannot spontaneously leak from one square to another if there is no path.
    
    Assume a constant flow rate for the water.
    
    Today's question is - writing a program, can you tell at what time the well's target square is under a cubic unit of water? 
    """

    def __init__(self, args):
        self.cols = 0
        self.rows = 0
        self.squares = []
        self.target = 0 # The target square "M"
        self.neighbours = []
        self.visited = set()
        self.time = 0
        self.parse_input(args)

    def parse_input(self, args):
        for i, line in enumerate(args.strip().splitlines()):
            line = line.strip()
            if not line == '':
                if i == 0:
                    (self.cols , self.rows) = [int(x) for x in line.split(' ')]
                elif i <= self.rows:
                    self.squares.extend([int(x) for x in re.split('[ ]+', line)])
                else:
                    self.target = self.squares.index(int(line))

    def get_neighbours(self, cols, rows):
        neighbours = [] # Cardinal points: N/E/S/W
        for i in range(0, cols*rows):
            (row, col) = ((int)(i / rows), i % cols)
            n = set()
            if row > 0:
                n.add((row - 1) * cols + col)
            if row < rows - 1:
                n.add((row + 1) * cols + col)
            if col > 0:
                n.add(row * cols + col - 1)
            if col < cols - 1:
                n.add(row * cols + col + 1)
            neighbours.append(n)
        return neighbours

    def fill(self, square = 0, min_square = 0, last_square = 0):
        self.visited.add(square)

        for n in self.neighbours[square]:
            # Can't walk squares higher than this square is
            if self.squares[n] <= self.squares[square] and n not in self.visited :
                min_square = self.fill(n, min_square, square)

        return square if self.squares[square] < self.squares[min_square] else min_square

    def solve(self):
        self.neighbours = self.get_neighbours(self.cols, self.rows)
        self.debug = False
        target_level = self.squares[self.target] + 1
        for self.time in range(1, 9999): # Avoid infinite loops
            self.visited = set()
            square = self.fill()
            if self.squares[square] + 1 > target_level and self.squares[self.target] >= target_level:
                self.time -= 1 # Reached the target level on the last iteration
                return self.time
            self.squares[square] = self.squares[square] + 1
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
print('Well 2 = {}'.format(well_2.solve()))
print('Well 3 = {}'.format(well_3.solve()))

# ----------------------------------------------------------------------------

def print_squares(well):
    print('')
    for r in range(0, well.rows):
        row = []
        for c in range(0, well.cols):
            i = r * well.cols + c
            row.append('{}{}  '.format(well.squares[i], '!' if i == well.target else '')[0:3])
        print(' '.join(row))
    print('Fill iterations: {}\n'.format(well.time))

print_squares(well_1)
print_squares(well_2)
print_squares(well_3)
