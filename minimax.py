import random
import copy

INFINITY = float("inf")
N_INFINITY = float("-inf")

class Minimax:
    def best_move(self, game, depth):
        best_score = N_INFINITY
        best_moves = []
        best_move = None
        turn = game.turn
        if game.find_moves(game.grid, turn):
            for move in game.find_moves(game.grid, turn):
                grid = game.move(move[0][0], move[0][1], copy.deepcopy(game.grid), turn)
                score = self.minimax(game, grid, turn, depth-1, False, N_INFINITY, INFINITY)
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
            best_move = random.choice(best_moves)
        else:
            best_move = [[None, None], None]
        return best_move


    def random_move(self, game):
        moves = game.find_moves(game.grid, game.turn)
        if moves:
            move = random.choice(moves)
        else:
            move = [[None, None], [None, None]]
        return move


    def minimax(self, game, grid, turn, depth, maximizing, alpha, beta):
        current_turn = turn
        if not maximizing:
            current_turn = game.opp(turn)
        if depth == 0 or not game.find_moves(grid, current_turn):
            best_score = self.eval_grid(game, grid, turn)
            return best_score
        elif maximizing:
            best_score = N_INFINITY
            for move in game.find_moves(grid, current_turn):
                grid = game.move(move[0][0], move[0][1], grid, current_turn)
                score = self.minimax(game, copy.deepcopy(grid), turn, depth - 1, False, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = INFINITY
            for move in game.find_moves(grid, current_turn):
                grid = game.move(move[0][0], move[0][1], grid, current_turn)
                score = self.minimax(game, copy.deepcopy(grid), turn, depth - 1, True, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score


    def eval_grid(self, game, grid, turn):
        count = game.count_score(grid)
        score = count[turn]
        return score
