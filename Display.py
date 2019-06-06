import pygame as pg

# resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
MIGHTY_BLUE = (79, 153, 209)
OLIVE = (102, 102, 0)
GRAY = (204, 204, 204)
BLUE = (0, 0, 255)

# images
angryRobot = pg.image.load('images/angry_robot.png')
cross = pg.image.load('images/cross.png')
circle = pg.image.load('images/circle.png')

pg.init()

# the display handle and text on the caption bar
displayWindow = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Win or Die Deluxe')


class EntryScreenDisplay:
    """
    Representing the entry's screen display that user interacts with when the game is launched and when the single
    game is ended.
    """
    board_size = 3 # default board size
    win_cond = 3 # default winning condition that must ba achieved in order to win the game

    def increment_board(self) -> None:
        """
        In order to speed up the AI, the winning_con defaultly increment along with board_size.
        """
        if self.board_size < 7:
            self.board_size += 1
            self.win_cond += 1

    def increment_win(self) -> None:
        if self.win_cond < 7 and self.win_cond < self.board_size:
            self.win_cond += 1

    def decrement_board(self) -> None:
        """
        Because win_con can't be bigger than board_size, it decrements as well, when this situation occurs.
        """
        if self.board_size > 3:
            self.board_size += -1
            if self.win_cond > self.board_size:
                self.win_cond += -1

    def decrement_win(self) -> None:
        if self.win_cond > 3:
            self.win_cond += -1

    def display_message(self, size: int, message: str, color: tuple, position: tuple) -> None:
        """
        Display message of desired size and color at desired position.

        :param size : the size of message. The bigger size, the bigger text will be displayed
        :param message: content of message. String that will be displayed
        :param color: color defined by the 3 - RGB - tuple
        :param position: x and y coordinated of the displayed text
        """
        text = pg.font.Font(None, size)
        text_surf = text.render(message, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = position
        displayWindow.blit(text_surf, text_rect)

    def maintain_button(self, position: tuple, width: int, height: int, rect_color: tuple, message: str,
                        mess_color: tuple, desired_action=None) -> None:
        """
        Display button at desired position. Also calls chosen function after it was clicked.

        :param desired_action: function that will be called after button click
        :param height: height of button
        :param width: width of button
        :param message: text that will be displayed on the button
        :param mess_color: color of text, displayed on the button
        :param rect_color: color of the button
        :param position: x and y coordinated of the button
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_clicked = pg.mouse.get_pressed()

        if (position[0] - width / 2) < mouse_pos[0] < (position[0] + width / 2) and \
                position[1] < mouse_pos[1] < (position[1] + height):
            if mouse_clicked[0] == 1 and desired_action is not None:
                pg.time.delay(200)
                if desired_action():  # this statement is only true when game has ended. It protects START button from
                    return            # being printed out too early
        pg.draw.rect(displayWindow, rect_color, ((position[0] - (width / 2), position[1]), (width, height)))
        self.display_message(int(height / 2), message, mess_color, (position[0], position[1] + height / 2))

    def print_components(self, run_main):
        """
        Prints out the whole layout of start screen.

        :param run_main: Function that starts the game
        """
        displayWindow.fill(YELLOW)
        self.display_message(120, 'Tic-Tac-Toe', BLACK, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.06))
        self.display_message(60, 'Win or Die Deluxe Edition', RED, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.135))
        self.display_message(60, 'Check if you can defeat', MIGHTY_BLUE, (WINDOW_WIDTH * 0.32, WINDOW_HEIGHT * 0.31))
        self.display_message(60, 'the mighty AI', MIGHTY_BLUE, (WINDOW_WIDTH * 0.32, WINDOW_HEIGHT * 0.38))
        displayWindow.blit(angryRobot, (WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.22))
        self.display_message(40, 'Size of the board', OLIVE, (WINDOW_WIDTH * 0.265, WINDOW_HEIGHT * 0.5))
        self.maintain_button((WINDOW_WIDTH * 0.14, WINDOW_HEIGHT*0.58), 50, 50, GRAY, "-", BLACK, self.decrement_board)
        self.maintain_button((WINDOW_WIDTH * 0.39, WINDOW_HEIGHT*0.58), 50, 50, GRAY, "+", BLACK, self.increment_board)
        self.maintain_button((WINDOW_WIDTH * 0.266, WINDOW_HEIGHT*0.545), 150, 100, WHITE, str(self.board_size), BLACK)
        self.display_message(40, 'In-Line figures required to win', OLIVE, (WINDOW_WIDTH * 0.29, WINDOW_HEIGHT * 0.76))
        self.maintain_button((WINDOW_WIDTH * 0.14, WINDOW_HEIGHT * 0.835), 50, 50, GRAY, "-", BLACK, self.decrement_win)
        self.maintain_button((WINDOW_WIDTH * 0.39, WINDOW_HEIGHT * 0.835), 50, 50, GRAY, "+", BLACK, self.increment_win)
        self.maintain_button((WINDOW_WIDTH * 0.266, WINDOW_HEIGHT * 0.8), 150, 100, WHITE, str(self.win_cond), BLACK)
        self.maintain_button((WINDOW_WIDTH * 0.75, WINDOW_HEIGHT * 0.65), 200, 150, WHITE, 'START', BLACK, run_main)


class GameScreenDisplay:
    """
    Represents the second screen's display (game screen). Also, it holds all the needed size informations and actual
    state of the board.
    """
    def __init__(self, size, win_condition):
        self.size = size
        self.win_condition = win_condition
        self.box_size = WINDOW_WIDTH / (1.1 * self.size + 0.1)   # size of grid's box (box where tags are placed)
        self.gap_size = 0.1 * self.box_size  # gap between grid boxes
        self.tags = [[None for x in range(self.size)] for y in range(self.size)]  # main state of the board
        self.cross = self.resize_tags(cross, True)  # resized image considering size of the board as a scale
        self.circle = self.resize_tags(circle, False)  # -||-

    def resize_tags(self, image: pg.SurfaceType, is_cross: bool) -> pg.SurfaceType:
        """
        Function that is responsible for resizing the passed image. The app is build the way, that only cross or circle
        are possible to be passed.

        :param image: This is the pygames class, that represents image
        :param size: Size of game board
        :param is_cross: Deciding which image is passed
        :return: Resized image
        """
        if is_cross:
            x = 1.38
            y = 1.38
        else:
            x = 1.87
            y = 1.87

        image_rect = image.get_rect()
        image = pg.transform.scale(image, (int(x / self.size * image_rect.width), int(y / self.size * image_rect.height)))
        return image

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
            x = i * self.gap_size + (i - 1) * self.box_size
            for j in range(1, self.size + 1):
                y = j * self.gap_size + (j - 1) * self.box_size
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
