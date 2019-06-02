from Display import *

INFINITY = 1e10  # represents infinity


class Bot(GameScreenDisplay):
    """
    Represents the AI and it's logic. Also implements algorithms that check the current state of the board.
    """
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

    def full_board(self) -> bool:
        """
        Checks if the board is fully packed with figures, which in practice means => if the tags array is full.
        :return: Bool deciding whether the board is fully packed or not
        """
        counter = 0
        for column in self.tags:
            if None in column:
                counter += 1
        return counter == 0

    def check_for_moves(self) -> list:
        """
        Checks for empty spaces in the tags list. If the empty space is found it's coordinates are being packed into
        tuple and into new list.
        :return: List of empty(available) spaces
        """
        avail_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.tags[x][y] is None:
                    avail_moves.append((x, y))
        return avail_moves

    def bot_handle_move(self) -> None:
        """
        Function mashes together classes functionality and performs the AI's move.
        It recursively calls the minimax algorithm and after finding the best move it adds tag into the tags list.
        """
        best_value = -INFINITY  # default best value for maximizing player (bot in this app is a maximizing player)
        available_moves = self.check_for_moves()                      # for more info check the minimax algorithm theory
        depth = int(1.4*self.size - self.win_condition)  # (depth) decides of how deep into recursion the algorithm will
        best_move = None                                 # get. 1.4 seems to be the best consensus between time of
                                                         # execution and accuracy of moves
        for move in available_moves:
            self.tags[move[0]][move[1]] = 'o'
            move_value = self.minimax(depth, -INFINITY, INFINITY, False)
            self.tags[move[0]][move[1]] = None
            if move_value > best_value:
                best_value = move_value
                best_move = move

        self.tags[best_move[0]][best_move[1]] = 'o'

    def minimax(self, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        """
        Minimax algorithm equipped in prunning functionality and wrapped into Tick-tac-toe game environment.

        :param depth: The recursion depth.
        :param alpha: One of the prunning factors.
        :param beta: One of the prunning factors.
        :param maximizing_player: Bool deciding which player is now taking turn (maximizing or minimizing)
        :return: Depends really when the function is called. When the fucntion is called recursively downwards the heap
        it returns {0, 1, -10, 10} (so-called static evaluation). When upwards, it returns the compared best value.
        """
        if self.check_if_win('x' if maximizing_player is True else 'o'):
            return -10 if maximizing_player else 10
        if self.full_board():
            return 1
        if depth == 0:
            return 0

        available_moves = self.check_for_moves()

        if maximizing_player:
            max_eval = -INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'o'
                evaluation = self.minimax(depth - 1, alpha, beta, False)
                self.tags[move[0]][move[1]] = None
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = INFINITY
            for move in available_moves:
                self.tags[move[0]][move[1]] = 'x'
                evaluation = self.minimax(depth - 1, alpha, beta, True)
                self.tags[move[0]][move[1]] = None
                min_eval = min(min_eval, evaluation)
                alpha = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval



