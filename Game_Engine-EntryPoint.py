from Main_Game_Screen import *


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

    def run_main_screen(self):
        run = True
        primary_screen = GameScreen(self.board_size, self.win_cond)
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
            primary_screen.draw_components()
            primary_screen.move()
            pg.display.update()
            if primary_screen.check_if_win('x'):
                run = False
                pg.time.delay(500)
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
            maintain_button((WINDOW_WIDTH*0.75, WINDOW_HEIGHT*0.65), 200, 150, WHITE, 'START', BLACK, self.run_main_screen)
            pg.display.update()


if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()


