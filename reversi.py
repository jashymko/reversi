import copy

class Reversi:
    def __init__(self):
        self.GRID_W = 8
        self.grid = [[0] * self.GRID_W for _ in range(self.GRID_W)]

        self.grid[3][3], self.grid[3][4],       \
        self.grid[4][3], self.grid[4][4] = 2, 1,\
                                           1, 2     # My bad

        self.turn = 1

    def opp(self, turn):
        return 3 - turn

    def scan(self, opp_row, opp_column, direction, grid, turn):
        row_change, column_change = direction[0], direction[1]
        row, column = opp_row + row_change, opp_column + column_change

        opp_found = False
        while 0 <= row <= self.GRID_W-1 and 0 <= column <= self.GRID_W-1:   # Search in given direction for valid move
            if grid[row][column] == turn:
                break
            elif grid[row][column] == 0 and not opp_found:
                break
            elif grid[row][column] == 0 and opp_found:
                return (column, row), direction
            elif grid[row][column] == self.opp(turn):
                opp_found = True
            row += row_change
            column += column_change
        return

    def count_score(self, grid):
        count = [0, 0, 0]
        for row in grid:
            for cell in row:
                count[cell] += 1
        return count

    def find_moves(self, grid, turn):
        moves = []
        for row in range(self.GRID_W):
            for column in range(self.GRID_W):  # Check every direction on each of player's pieces for potential connection
                if grid[row][column] == turn:
                    dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                    for direction in dirs:
                        move = self.scan(row, column, direction, grid, turn)
                        if move:
                            moves.append(move)
        return moves


    def full_turn(self, x, y):
        possible_moves = self.find_moves(self.grid, self.turn)
        grid = copy.deepcopy(self.grid)
        if possible_moves:  # If there are moves possible:
            grid = self.move(x, y, grid, self.turn)

            if grid != self.grid:
                self.grid = grid
                self.change_turn()
        else:                   # Skip turn if no moves are possible
            self.change_turn()
            if not self.find_moves(self.grid, self.turn):
                self.game_over()


    def move(self, x, y, grid, turn):
        possible_moves = self.find_moves(grid, turn)
        overlapping_moves = []
        for move in possible_moves:     # Add all moves at clicked location to overlapping_moves
            if move[0] == (x, y):
                overlapping_moves.append(move)
        for move in overlapping_moves:  # Read move tuple to fill in cells with player's chips
            row_change, column_change = move[1][0], move[1][1]
            column, row = x, y
            while grid[row][column] != turn:
                grid[row][column] = turn
                row -= row_change
                column -= column_change
            grid[y][x] = 0
        if overlapping_moves:
            grid[y][x] = turn
        return grid

    def change_turn(self):
        self.turn = self.opp(self.turn)

    def game_over(self):
        count = self.count_score(self.grid)
        players = ["Black", "White"]
        if count[1] != count[2]:
            print players[count.index(max(count[2], count[1])) - 1], "wins!"
            print "White:", count[2], ", Black:", count[1]
        else:
            print "Tie!"
