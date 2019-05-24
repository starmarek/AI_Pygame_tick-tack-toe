import pygame as pg

# resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

pg.init()

displayWindow = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Win or Die')


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
    """
    mouse_pos = pg.mouse.get_pos()
    mouse_clicked = pg.mouse.get_pressed()

    if (position[0] - width/2) < mouse_pos[0] < (position[0] + width/2) and \
            position[1] < mouse_pos[1] < (position[1] + height):
        if mouse_clicked[0] == 1 and desired_action is not None:
            pg.time.delay(50)
            desired_action()
    pg.draw.rect(displayWindow, rect_color, ((position[0]-(width/2), position[1]), (width, height)))
    display_message(int(height/3), message, mess_color, (position[0], position[1] + height/2))


class GameEngine:
    board_size = 3
    win_cond = 3

    def increment_size(self):
        self.board_size += 1

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
            display_message(100, 'Elo typie', BLACK, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.1))
            maintain_button((WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.2), 300, 150, WHITE, str(self.board_size), BLACK, self.increment_size)
            pg.display.update()


if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()


