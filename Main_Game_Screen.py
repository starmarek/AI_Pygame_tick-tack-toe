from Player import *


class GameScreen:
    """
    Presents the second screen of app where the actual game is taking place. User is able to get to this screen by
    clicking the start button on the welcome screen.

    Class is equipped in the following functionality:
    - Printing the up-to-date components of game screen
    - Calling the Player class to handle it's move
    - Checking if the actual state of board is a winning one
    """
    def __init__(self, size, win_condition):
        self.size = size
        self.win_condition = win_condition
        self.box_size = WINDOW_WIDTH / (1.1 * self.size + 0.1)
        self.gap_size = 0.1 * self.box_size
        self.tags = [[None for x in range(self.size)] for y in range(self.size)]
        self.cross = resize_image(cross, self.size, True)
        self.circle = resize_image(circle, self.size, False)

    def draw_grid(self) -> None:
        """
        Prints the squares/fields where the 'o's and 'x's will be put. Basically prints the Games grid.
        """
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                pg.draw.rect(displayWindow, GRAY, [j*self.gap_size+(j-1)*self.box_size,
                                                   i*self.gap_size+(i-1)*self.box_size, self.box_size, self.box_size])

    def draw_tags(self) -> None:
        """
        Prints actual state of board into the screen, which means it prints all the 'o's and 'x's that
        were put by player/bot.
        """
        for i in range(1, self.size + 1):
            y = i * self.gap_size + (i - 1) * self.box_size
            for j in range(1, self.size + 1):
                x = j * self.gap_size + (j - 1) * self.box_size
                if self.tags[i-1][j-1] == 'x':
                    displayWindow.blit(self.cross, (x, y))
                elif self.tags[i-1][j-1] == 'o':
                    displayWindow.blit(self.circle, (x, y))

    def draw_components(self) -> None:
        """
        Prints all the components of game screen.
        """
        displayWindow.fill(YELLOW)
        self.draw_grid()
        self.draw_tags()

    def move(self) -> None:
        """
        Calls the static method of Player class that is responsible for handling the player move.
        """
        Player.handle_move(self.size, self.box_size, self.gap_size, self.tags, self.cross)

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


