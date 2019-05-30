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

# images
angryRobot = pg.image.load('angry_robot.png')

pg.init()

displayWindow = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Win or Die Deluxe')


def display_message(size: int, message: str, color: tuple, position: tuple) -> None:
    """
    Display message of desired size and color at desired position

    Parameters:
        size(int): the size of message. The bigger size, the bigger text will be displayed
        message(str): content of message. String that will be displayed
        color(tuple): color defined by the 3 - RGB - tuple
        position(tuple): x and y coordinated of the displayed text
    """
    text = pg.font.Font(None, size)
    text_surf = text.render(message, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = position
    displayWindow.blit(text_surf, text_rect)


def maintain_button(position: tuple, width: int, height: int, rect_color: tuple, message: str,
                    mess_color: tuple, desired_action=None) -> None:
    """
    Display button at desired position. Also calls chosen function after it was clicked.

    Parameters:
        desired_action: function that will be called after button click
        height(int): height of button
        width(int): width of button
        message(str): text that will be displayed on the button
        mess_color(tuple): color of text, displayed on the button
        rect_color(tuple): color of the button
        position(tuple): x and y coordinated of the button
    """
    mouse_pos = pg.mouse.get_pos()
    mouse_clicked = pg.mouse.get_pressed()

    if (position[0] - width/2) < mouse_pos[0] < (position[0] + width/2) and \
            position[1] < mouse_pos[1] < (position[1] + height):
        if mouse_clicked[0] == 1 and desired_action is not None:
            pg.time.delay(200)
            if desired_action():
                return
    pg.draw.rect(displayWindow, rect_color, ((position[0]-(width/2), position[1]), (width, height)))
    display_message(int(height/2), message, mess_color, (position[0], position[1] + height/2))


class GameScreen:
    def __init__(self, size, win_condition):
        self.size = size
        self.win_condition = win_condition
        self.box_size = WINDOW_WIDTH / (1.1 * self.size + 0.1)
        self.gap_size = 0.1 * self.box_size
        self.markers = [[None for x in range(self.size)] for y in range(self.size)]

    def draw_grid(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                pg.draw.rect(displayWindow, GRAY, [j*self.gap_size+(j-1)*self.box_size,
                                                   i*self.gap_size+(i-1)*self.box_size, self.box_size, self.box_size])

   # def draw_tags(self):

    def draw_components(self):
        displayWindow.fill(YELLOW)
        self.draw_grid()
       # self.draw_tags()


class GameEngine:
    board_size = 3
    win_cond = 3

    def increment_board(self):
        if self.board_size < 7:
            self.board_size += 1

    def increment_win_con(self):
        if self.win_cond < 7 and self.win_cond < self.board_size:
            self.win_cond += 1

    def decrement_board(self):
        if self.board_size > 3:
            self.board_size += -1
            if self.win_cond > self.board_size:
                self.win_cond += -1

    def decrement_win_con(self):
        if self.win_cond > 3:
            self.win_cond += -1

    def run_game(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
            primary_screen = GameScreen(self.board_size, self.win_cond)
            primary_screen.draw_components()
            pg.display.update()
        return 1

    def run_first_screen(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()

            displayWindow.fill(YELLOW)
            display_message(120, 'Tic-Tac-Toe', BLACK, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.06))
            display_message(60, 'Win or Die Deluxe Edition', RED, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.135))
            display_message(60, 'Check if you can defeat', MIGHTY_BLUE, (WINDOW_WIDTH * 0.32, WINDOW_HEIGHT*0.31))
            display_message(60, 'the mighty AI', MIGHTY_BLUE, (WINDOW_WIDTH*0.32, WINDOW_HEIGHT*0.38))
            displayWindow.blit(angryRobot, (WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.22))
            display_message(40, 'Size of the board', OLIVE, (WINDOW_WIDTH*0.265, WINDOW_HEIGHT * 0.5))
            maintain_button((WINDOW_WIDTH*0.14, WINDOW_HEIGHT*0.58), 50, 50, GRAY, "-", BLACK, self.decrement_board)
            maintain_button((WINDOW_WIDTH*0.39, WINDOW_HEIGHT*0.58), 50, 50, GRAY, "+", BLACK, self.increment_board)
            maintain_button((WINDOW_WIDTH*0.266, WINDOW_HEIGHT*0.545), 150, 100, WHITE, str(self.board_size), BLACK)
            display_message(40, 'In-Line figures required to win', OLIVE, (WINDOW_WIDTH*0.29, WINDOW_HEIGHT*0.76))
            maintain_button((WINDOW_WIDTH*0.14, WINDOW_HEIGHT*0.835), 50, 50, GRAY, "-", BLACK, self.decrement_win_con)
            maintain_button((WINDOW_WIDTH*0.39, WINDOW_HEIGHT*0.835), 50, 50, GRAY, "+", BLACK, self.increment_win_con)
            maintain_button((WINDOW_WIDTH*0.266, WINDOW_HEIGHT*0.8), 150, 100, WHITE, str(self.win_cond), BLACK)
            maintain_button((WINDOW_WIDTH*0.75, WINDOW_HEIGHT*0.65), 200, 150, WHITE, 'START', BLACK, self.run_game)
            pg.display.update()


if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()


