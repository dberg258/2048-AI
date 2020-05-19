import time
import math


U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
smoothness_calculations = dict()
smoothness_calculations[(0, 0)] = (R, D)
smoothness_calculations[(3, 3)] = (L, U)
smoothness_calculations[(1, 1)] = (U, D, L, R)
smoothness_calculations[(2, 2)] = (U, D, L, R)
smoothness_calculations[(2, 0)] = (U, D, R)
smoothness_calculations[(0, 2)] = (L, D, R)
smoothness_calculations[(1, 3)] = (U, D, L)
smoothness_calculations[(3, 1)] = (L, U, R)

weighted_matrix = [
    [4 ** 15, 4 ** 14, 4 ** 13, 4 ** 12],
    [4 ** 8, 4 ** 9, 4 ** 10, 4 ** 11],
    [4 ** 7, 4 ** 6, 4 ** 5, 4 ** 4],
    [4 ** 0, 4 ** 1, 4 ** 2, 4 ** 13]
]


class IntelligentAgent:

    def get_move(self, grid):
        return self.search(grid)

    def search(self, grid):
        start = time.process_time()
        return self.max_value(grid, -10, 10, 0, start)

    def max_value(self, state, alpha, beta, depth, start):
        utility = self.get_utility(state)

        if self.is_terminal(state, depth) or time.process_time()-start > .15:
            return utility

        best_val = -10
        best_move = None
        for move in state.getAvailableMoves():

            result = self.chance(move[1], alpha, beta, depth + 1, start)

            if result > best_val:
                best_val = result
                best_move = move[0]
            if best_val >= beta:
                return best_val
            alpha = max(alpha, best_val)

        if depth == 0:
            return best_move
        return best_val

    def chance(self, state, alpha, beta, depth, start):
        return .9 * self.min_value(state, alpha, beta, depth, 2, start) + .1 * self.min_value(state, alpha, beta, depth, 4, start)

    def min_value(self, state, alpha, beta, depth, tile, start):
        utility = self.get_utility(state)

        if self.is_terminal(state, depth) or time.process_time()-start > .15:
            return utility

        best_val = 10
        for spawn in state.getAvailableCells():
            state.setCellValue(spawn, tile)

            result = self.max_value(state, alpha, beta, depth + 1, start)
            state.setCellValue(spawn, 0)
            best_val = min(best_val, result)
            if best_val <= alpha:
                return best_val
            beta = min(beta, best_val)
        return best_val

    @staticmethod
    def is_terminal(state, depth):
        if depth == 4:
            return True
        return not state.canMove()

    def get_utility(self, state):
        board = state.map

        tile_weight_score = self.get_weighted_tile_score(board)
        smoothness_score = self.get_smoothness_score(board)
        empty_cell_score = self.get_empty_cell_score(state)

        tile_weight_score = math.log2(tile_weight_score)/15
        smoothness_score = math.log(smoothness_score + 1)/3
        empty_cell_score = math.log2(empty_cell_score + 1)

        return 0.4*tile_weight_score - 0.9*smoothness_score + 0.1*empty_cell_score

    @staticmethod
    def get_weighted_tile_score(board):
        tile_weight_sum = 0
        for i in range(4):
            for j in range(4):
                tile_weight_sum += board[i][j] * weighted_matrix[i][j]

        return tile_weight_sum

    @staticmethod
    def get_smoothness_score(board):
        score = 0
        for cell, directions in smoothness_calculations.items():
            cell_value = board[cell[0]][cell[1]]
            if cell_value:
                for direction in directions:
                    neighbor_value = board[cell[0] + direction[0]][cell[1] + direction[1]]
                    difference = abs(cell_value - neighbor_value)
                    if neighbor_value:
                        score += difference
        return score

    @staticmethod
    def get_empty_cell_score(state):
        return len(state.getAvailableCells())