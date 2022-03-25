import sys
from sets import Set

def parse_cols(line):
  cols = []
  item = ""
  for c in "".join(line.split()):
    if c == "[":
      pass
    elif c == "]":
      cols.append(item)
      item = ""
    else:
      item = c

  return cols

class Cell():
  def __init__(self, values, x, y):
    self.values = Set(values)
    self.x = x
    self.y = y

  def __len__(self):
    return len(self.values)

  def remove_solution(self, cell):
    self.values = self.values.difference(cell.values)

  def __str__(self):
    return ",".join([str(i) for i in self.values])

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return hash((x,y,))

class Matrix():
  def __init__(self):
    # fill all the solutions with 1..9
    self.rows = [[Cell(range(1,9), x, y) for x in range(9)] for y in range(9)]
    
    # calculate cols
    self.columns = [[] for c in range(9)]
    for y, row in enumerate(self.rows):
      for x, cell in enumerate(row):
        self.columns[x].append(cell)

    # calculate groups
    self.groups = [[] for c in range(9)]
    for y, row in enumerate(self.rows):
      for x, cell in enumerate(row):
        group_index = int(x/3) + (int(y/3) * 3)
        self.groups[group_index].append(cell)

  def set_value_at(self, x, y, value):
      cell = self.rows[y][x]
      cell.values = Set([int(value)])


  def is_solved(self):
    for row in self.rows:
      for cell in row:
        if len(cell.values) > 1:
          return False
    
    return True

def parse_input(game):
  matrix = Matrix()
  line_number = -1

  for line in game:
    if not line.isspace():
      line_number += 1
      for col_number, c in enumerate(parse_cols(line)):
        if c.isdigit():
          matrix.set_value_at(col_number, line_number, c)

  return matrix

def remove_digits_found_in(cell, collection):
  if len(cell) == 1:
    for other_cell in collection:
      if cell is not other_cell and len(other_cell) > 1:
        other_cell.remove_solution(cell)

def solve_sudoku(matrix, tries = 0):
  for y, row in enumerate(matrix.rows):
    for x, cell in enumerate(row):
      remove_digits_found_in(cell, row)

  for x, column in enumerate(matrix.columns):
    for y, cell in enumerate(column):
     remove_digits_found_in(cell, column)

  for group in matrix.groups:
    for index, cell in enumerate(group):
      remove_digits_found_in(cell, group)

  if matrix.is_solved():
    return matrix

  if tries > 500:
    print "Could not solve Matrix!!"
    return matrix

  return solve_sudoku(matrix, tries + 1)

def print_matrix(matrix):
  for row in matrix.rows:
    row_strs = []
    for col in row:
      row_strs.append(",".join([str(col)]))
    print "|%s|" % "|".join(row_strs)


solutions = solve_sudoku(parse_input(sys.stdin))

print_matrix(solutions)