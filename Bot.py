from Display import *

INFINITY = 1e10


class Bot(GameScreenDisplay):

    def check_columns(self, win: list) -> bool:
        """
        Searches for winning sequence in columns.
        :param win: Go to "Check diagonals' method for explanation.
        :return: True, if winning sequence was found.
        """
        for row in range(self.size):
            column = [self.tags[x][row] for x in range(self.size)]
            for j in range(len(column) - len(win) + 1):
                if win == column[j:j+self.win_condition]:
                    return True

    def check_rows(self, win: list) -> bool:
        """
        Searches for winning sequence in rows.
        :param win: Go to 'check_diagonals' method for explanation.
        :return: True, if winning sequence was found.
        """
        for row in self.tags:
            for j in range(len(row) - len(win) + 1):
                if win == row[j:j+self.win_condition]:
                    return True

    def check_diagonals(self, win: list) -> bool:
        """
        Check for winning sequence in all possible diagonals that are at least as long as winning condition.
        :param win: List that represent winning sequence. For example, when win_con = 3 -> win = ['x', 'x', 'x']
        (for human player; for bot there would be bunch of 'o's).
        :return: Function returns boolean value if found winning sequence in one of the diagonals.
        """
        for i in range(self.size - self.win_condition + 1):
            # [x x    ]
            # [  x x  ]
            # [    x x]
            # [      x]
            diagonal = []
            x = i
            y = 0
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x += 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True
            # [x      ]
            # [x x    ]
            # [  x x  ]
            # [    x x]
            diagonal = []
            x = 0
            y = i
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x += 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True

            # [    x x]
            # [  x x  ]
            # [x x    ]
            # [x      ]
            diagonal = []
            x = self.size - 1 - i
            y = 0
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x -= 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True
            # [      x]
            # [    x x]
            # [  x x  ]
            # [x x    ]
            diagonal = []
            x = self.size - 1
            y = 0 + i
            for j in range(self.size - i):
                diagonal.append(self.tags[x][y])
                x -= 1
                y += 1
            for j in range(len(diagonal) - len(win) + 1):
                if win == diagonal[j:j + self.win_condition]:
                    return True

    def check_if_win(self, tag: str) -> bool:
        """
        Checks if in any dimension the winning line is achieved.
        :param tag: Symbol, based on which, the win_line-list will be build -> {'x', 'o'}.
        :return: Returns true if the winning line was found.
        """
        win_line = [tag]*self.win_condition
        return self.check_rows(win_line) or self.check_columns(win_line) or self.check_diagonals(win_line)

    def full_board(self):
        counter = 0
        for column in self.tags:
            if None in column:
                counter += 1
        return counter == 0

    def check_for_moves(self):
        aval_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.tags[x][y] is None:
                    aval_moves.append((x, y))
        return aval_moves

    def bot_handle_move(self):
        best_value = -INFINITY
        available_moves = self.check_for_moves()
        depth = int(1.4*self.size - self.win_condition)
        best_move = None

        for move in available_moves:
            self.tags[move[0]][move[1]] = 'o'
            move_value = self.minimax(depth, -INFINITY, INFINITY, False)
            self.tags[move[0]][move[1]] = None
            if move_value > best_value:
                print(move)
                best_value = move_value
                best_move = move

        self.tags[best_move[0]][best_move[1]] = 'o'

    def minimax(self, depth, alpha, beta, max_player):
        if self.check_if_win('x' if max_player is True else 'o'):
            return -10 if max_player else 10
        if self.full_board():
            return 1
        if depth == 0:
            return 0

        available_moves = self.check_for_moves()

        if max_player:
            max_eval = -INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'o'
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.tags[move[0]][move[1]] = None
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'x'
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.tags[move[0]][move[1]] = None
                min_eval = min(min_eval, eval)
                alpha = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval



