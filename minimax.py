import random
import copy

INFINITY = float("inf")
N_INFINITY = float("-inf")

class Minimax:
    def __init__(self):
        self.max_depth = 2

    def best_move(self, game):
        best_score = N_INFINITY
        best_move = None
        depth = 0
        grid = game.grid
        turn = game.turn
        if game.find_moves(grid, turn):
            for move in game.find_moves(grid, turn):
                score = self.minimax(game, copy.deepcopy(grid), turn, depth)
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_move = [[None, None], None]
        return best_move


    def random_move(self, game):
        moves = game.find_moves(game.grid, game.turn)
        if moves:
            move = random.choice(moves)
        else:
            move = [[None, None], None]
        return move


    def minimax(self, game, grid, turn, depth):
        best_score = N_INFINITY
        depth += 1
        if depth < self.max_depth and game.find_moves(grid, turn):
            for move in game.find_moves(grid, turn):
                grid = game.move(move[0][0], move[0][1], grid, turn)
                score = self.minimax(game, copy.deepcopy(grid), turn, depth)
                if turn == game.P_TURN:
                    score *= -1
                if score > best_score:
                    best_score = score
        else:
            best_score = self.eval_grid(game, grid)
        return best_score


    def eval_grid(self, game, grid):
        count = game.count_score(grid)
        score = count[1] - count[0]
        return score
